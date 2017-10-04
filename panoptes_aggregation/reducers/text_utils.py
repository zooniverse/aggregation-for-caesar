import collatex as col
from collections import OrderedDict, Counter
import copy
import numpy as np
from sklearn.cluster import DBSCAN


def tokenize(self, contents):
    '''tokenize only on space so angle bracket tags are not split'''
    return contents.split()


# override the built-in tokenize
col.core_classes.WordPunctuationTokenizer.tokenize = tokenize


def overlap(x, y):
    '''Check if two line segments overlap

    Parameters
    ----------
    x : list
        A list with the start and end point of the first line segment
    y : lits
        A list with the start and end point of the second line segment

    Returns
    -------
    overlap : bool
        True if the two line segments overlap, False otherwise
    '''
    return x[1] >= y[0] and y[1] >= x[0]


def gutter(lines_in):
    '''Cluster list of input line segments by what side of
    the page gutter they are on.

    Parameters
    ----------
    lines_in : list
        A list-of-lists containing one line segment per item. Each line
        segment should contain only the x-coordinate of each point on the line.

    Returns
    -------
    gutter_index : array
        A numpy array containing the cluster label for each input line. This label
        idicates what side of the gutter(s) the input line segment is on.
    '''
    lines = [[min(l), max(l)] for l in lines_in]
    overlap_lines = []
    for ldx, l in enumerate(lines):
        if ldx == 0:
            overlap_lines = np.array([l])
        else:
            o_lines = np.array([overlap(o, l) for o in overlap_lines])
            if o_lines.any():
                comp = np.vstack([overlap_lines[o_lines], l])
                overlap_lines[o_lines] = [comp.min(), comp.max()]
                overlap_lines = np.unique(overlap_lines).reshape(-1, 2)
            else:
                overlap_lines = np.vstack([overlap_lines, l])
    overlap_lines.sort(axis=0)
    gutter_label = -np.ones(len(lines), dtype=int)
    for odx, o in enumerate(overlap_lines):
        gdx = np.array([overlap(o, l) for l in lines])
        gutter_label[gdx] = odx
    return gutter_label


def angle_metric(t1, t2):
    '''A metric for the distance between angles in the [-180, 180] range

    Parameters
    ----------
    t1 : float
        Theta one in degrees
    t2 : float
        Theta two in degrees

    Returns
    -------
    distance : float
        The distance between the two input angles in degrees
    '''
    d = abs(t1 - t2)
    if d > 180:
        d = 360 - d
    return d


def avg_angle(theta):
    '''A function that finds the avage of an array of angles that are
    in the range [-180, 180].

    Parameters
    ----------
    theta : array
        An array of angles that are in the range [-180, 180] degrees

    Returns
    -------
    average : float
        The average angle
    '''
    if theta.max() - theta.min() > 180:
        theta[theta < 0] += 360
    return theta.mean()


def sort_labels(db_labels, data, reducer=np.mean, descending=False):
    '''A function that takes in the cluster lables for some data and returns
    a sorted (by the original data) list of the unique lables in.

    Parameters
    ----------
    db_labels : list
        A list of cluster lables, one labele for each data point.
    data : np.array
        The data the lables belong to
    reducer : function (optional)
        The function used to combine the data for each label.  Defualt: np.mean
    descending : bool (optional)
        A flag indicating if the lables should be sorted in descending order.
        Default: False

    Returns
    -------
    lables : list
        A list of unique cluster lables sorted in either ascending or descending order.
    '''
    all_labels = set(db_labels)
    if -1 in all_labels:
        all_labels.remove(-1)
    labels = np.array(list(all_labels))
    avg = [reducer(data[db_labels == l]) for l in labels]
    sdx = np.argsort(avg)
    if descending:
        sdx = sdx[::-1]
    return labels[sdx]


def consensus_score(clusters_text):
    '''A function to take clustered text data and return the consensus score

    Parameters
    ----------
    clusters_text : list
        A list-of-lists with length equal to the number of words in a line of text and each
        inner list contains the transcriptions for each word.

    Returns
    -------
    consensus_score : float
        A value indicating the average number of users that agree on the line of text.
    '''
    text_filter = [list(filter(('').__ne__, text)) for text in clusters_text if text]
    max_counts = [Counter(text).most_common(1)[0][1] for text in text_filter if text]
    return sum(max_counts) / len(max_counts)


def cluster_by_word(word_line, xy_line, text_line, annotation_labels, kwargs_cluster, kwargs_dbscan):
    '''A function to take the annotations for one line of text and cluster them
    based on the words in the line.

    Parameters
    ----------
    word_line : np.array
        An nx1 array with the x-position of each dot in the rotated coordiate frame.
    xy_line : np.array
        An nx2 array with the non-rotated (x, y) positions of each dot.
    text_line : np.array
        An nx1 array with the text for each dot.
    annotation_labels : np.array
        An nx1 array with a lable indicating what annotaiton each word belongs to.
    kwargs_cluster : dict
        A dictionary containing the `eps_*`, `metric`, and `dot_freq` keywords
    kwargs_dbscan : dict
        A dictionary containing all the other DBSCAN keywords

    Returns
    -------
    clusters_x : list
        A list with the x-position of each dot cluster found
    clusters_y : list
        A list with the y-position of each dot cluster found
    clusters_text : list
        A list-of-lists with the words transcribed at each dot cluster found. One
        list per cluster. Note: the empty strings that were added to each annotaiton are
        stripped before returning the words.
    '''
    db_words = DBSCAN(eps=kwargs_cluster['eps_word'], metric=kwargs_cluster['metric'], **kwargs_dbscan).fit(word_line)
    word_labels = sort_labels(db_words.labels_, word_line)
    clusters_x = []
    clusters_y = []
    unique_annotations = np.unique(annotation_labels)
    lower_annotaiton_labels = np.zeros(len(annotation_labels), dtype=int)
    for idx, i in enumerate(unique_annotations):
        jdx = annotation_labels == i
        lower_annotaiton_labels[jdx] = idx
    clusters_text = [['' for i in range(len(unique_annotations))] for j in range(len(word_labels))]
    for cdx, word_label in enumerate(word_labels):
        wdx = db_words.labels_ == word_label
        word_x, word_y = xy_line[wdx].mean(axis=0)
        for word, a_label in zip(text_line[wdx], lower_annotaiton_labels[wdx]):
            clusters_text[cdx][a_label] = word
        clusters_x.append(float(word_x))
        clusters_y.append(float(word_y))
    return clusters_x, clusters_y, clusters_text


def align_words(word_line, xy_line, text_line, kwargs_cluster, kwargs_dbscan):
    '''A function to take the annotations for one line of text, aligns the words,
    and finds the end-points for the line.

    Parameters
    ----------
    word_line : np.array
        An nx1 array with the x-position of each dot in the rotated coordiate frame.
    xy_line : np.array
        An nx2 array with the non-rotated (x, y) positions of each dot.
    text_line : np.array
        An nx1 array with the text for each dot.
    kwargs_cluster : dict
        A dictionary containing the `eps_*`, `metric`, and `dot_freq` keywords
    kwargs_dbscan : dict
        A dictionary containing all the other DBSCAN keywords

    Returns
    -------
    clusters_x : list
        A list with the start and end x-position of the line
    clusters_y : list
        A list with the start and end y-position of the line
    clusters_text : list
        A list-of-lists with the words transcribed at each dot cluster found. One
        list per cluster. Note: the empty strings that were added to each annotaiton are
        stripped before returning the words.
    '''
    clusters_x = []
    clusters_y = []
    clusters_text = []
    # ignore min_samples when trying to find the end points of a line
    min_samples = kwargs_dbscan.pop('min_samples', 1)
    db_words = DBSCAN(eps=kwargs_cluster['eps_word'], metric=kwargs_cluster['metric'], min_samples=1, **kwargs_dbscan).fit(word_line)
    # put min_samples back in
    kwargs_dbscan['min_samples'] = min_samples
    word_labels = sort_labels(db_words.labels_, word_line)
    if len(word_labels) > 1:
        word_labels = [word_labels[0], word_labels[-1]]
        for word_label in word_labels:
            wdx = db_words.labels_ == word_label
            word_x, word_y = xy_line[wdx].mean(axis=0)
            clusters_x.append(float(word_x))
            clusters_y.append(float(word_y))
        collation = col.Collation()
        witness_key = []
        for tdx, t in enumerate(text_line):
            if t != '':
                key = str(tdx)
                collation.add_plain_witness(key, t)
                witness_key.append(key)
        if len(collation.witnesses) > 0:
            alignment_table = col.collate(collation, near_match=True, segmentation=False)
            for cols in alignment_table.columns:
                word_dict = cols.tokens_per_witness
                word_list = []
                for key in witness_key:
                    word_list.append(str(word_dict.get(key, [''])[0]))
                clusters_text.append(word_list)
    return clusters_x, clusters_y, clusters_text


def cluster_by_line(xy_slope, text_slope, annotation_labels, kwargs_cluster, kwargs_dbscan):
    '''A function to take the annotations for one `slope_label` and cluster them
    based on perpendicular distance (e.g. lines of text).

    Parameters
    ----------
    xy_slope : np.array
        An array of shape nx2 containing the (x, y) positions for *each* dot drawn.
    text_slope : np.array
        An array of shape nx1 containing the text for *each* dot drawn. Note: each
        annotation has an empty string added to the end so this array has the same
        shape as `xy_slope`.
    annotation_labels : np.array
        An array of shape nx1 containing a unique lable indicating what annotation
        each position/text came from.  This information is used to ensure one annotation
        does not span multiple lines.
    kwargs_cluster : dict
        A dictionary containing the `eps_*`, `metric`, and `dot_freq` keywords
    kwargs_dbscan : dict
        A dictionary containing all the other DBSCAN keywords

    Returns
    -------
    frame_lines : list
        A list of reductions, one for each line. Each reduction is a dictionary
        containing the information for the line.
    '''
    c = np.cos(np.deg2rad(-kwargs_cluster['avg_slope']))
    s = np.sin(np.deg2rad(-kwargs_cluster['avg_slope']))
    R = np.array([[c, -s], [s, c]])
    xy_rotate = np.dot(xy_slope, R.T)
    lines = xy_rotate[:, 1].reshape(-1, 1)
    words = xy_rotate[:, 0].reshape(-1, 1)
    a_lables = np.unique(annotation_labels)
    avg_lines = np.array([lines[annotation_labels == a].mean() for a in a_lables]).reshape(-1, 1)
    db_lines = DBSCAN(eps=kwargs_cluster['eps_line'], metric=kwargs_cluster['metric'], **kwargs_dbscan).fit(avg_lines)
    line_labels = sort_labels(db_lines.labels_, avg_lines)
    frame_lines = []
    for line_label in line_labels:
        ldx = db_lines.labels_ == line_label
        # this ensures that full annotations stay together
        adx = np.zeros(len(lines), dtype=bool)
        for a_label in a_lables[ldx]:
            adx |= annotation_labels == a_label
        if kwargs_cluster['dot_freq'] == 'word':
            clusters_x, clusters_y, clusters_text = cluster_by_word(words[adx], xy_slope[adx], text_slope[adx], annotation_labels[adx], kwargs_cluster, kwargs_dbscan)
        elif kwargs_cluster['dot_freq'] == 'line':
            clusters_x, clusters_y, clusters_text = align_words(words[adx], xy_slope[adx], text_slope[adx], kwargs_cluster, kwargs_dbscan)
        else:
            raise Exception('Not a valid `dot_freq` keyword')
        line_dict = {
            'clusters_x': clusters_x,
            'clusters_y': clusters_y,
            'clusters_text': clusters_text,
            'number_views': ldx.sum(),
            'consensus_score': consensus_score(clusters_text),
            'line_slope': float(kwargs_cluster['avg_slope']),
            'slope_label': int(kwargs_cluster['slope_label']),
            'gutter_label': int(kwargs_cluster['gutter_label'])
        }
        if len(line_dict['clusters_x']) > 0:
            frame_lines.append(line_dict)
    return frame_lines


def cluster_by_slope(x, y, text, slope, kwargs_cluster, kwargs_dbscan):
    '''A function to take the annotations for one `gutter_label` and cluster them
    based on what slope the transcription is.

    Parameters
    ----------
    x : list
        A list-of-lists of the x values for each drawn dot. There is one item in the
        list for annotation made by the user.
    y : list
        A list-of-lists of the y values for each drawn dot. There is one item in the
        list for annotation made by the user.
    text_frame : list
        A list-of-lists of the text for each drawn dot. There is one item in the
        list for annotation made by the user. The inner text lists are padded with
        an empty string at the end so there is the same number of words as there are
        dots.
    slope_frame : list
        A list of the slopes (in deg) for each annotation
    kwargs_cluster : dict
        A dictionary containing the `eps_*`, `metric`, and `dot_freq` keywords
    kwargs_dbscan : dict
        A dictionary containing all the other DBSCAN keywords

    Returns
    -------
    frame_slope : list
        A list of the resulting extractions, one item per line of text found.
    '''
    db_slope = DBSCAN(eps=kwargs_cluster['eps_slope'], metric=angle_metric, **kwargs_dbscan).fit(slope)
    slope_labels = sort_labels(db_slope.labels_, slope, reducer=avg_angle, descending=True)
    frame_slope = []
    for slope_label in slope_labels:
        sdx = db_slope.labels_ == slope_label
        annotation_label = np.hstack([np.zeros(len(i)) + idx for idx, i in enumerate(x[sdx])])
        xy_slope = np.array(list(zip(np.hstack(x[sdx]), np.hstack(y[sdx]))))
        text_slope = np.hstack(text[sdx])
        avg_slope = avg_angle(slope[sdx])
        kwargs_cluster['avg_slope'] = avg_slope
        kwargs_cluster['slope_label'] = slope_label
        frame_lines = cluster_by_line(xy_slope, text_slope, annotation_label, kwargs_cluster, kwargs_dbscan)
        frame_slope += frame_lines
    return frame_slope


def cluster_by_gutter(x_frame, y_frame, text_frame, slope_frame, kwargs_cluster, kwargs_dbscan):
    '''A function to take the annotations for each frame of a subject and group them
    based on what side of the page gutter they are on.

    Parameters
    ----------
    x_frame : list
        A list-of-lists of the x values for each drawn dot. There is one item in the
        list for annotation made by the user.
    y_frame : list
        A list-of-lists of the y values for each drawn dot. There is one item in the
        list for annotation made by the user.
    text_frame : list
        A list-of-lists of the text for each drawn dot. There is one item in the
        list for annotation made by the user.
    slope_frame : list
        A list of the slopes (in deg) for each annotation
    kwargs_cluster : dict
        A dictionary containing the `eps_*`, `metric`, and `dot_freq` keywords
    kwargs_dbscan : dict
        A dictionary containing all the other DBSCAN keywords

    Returns
    -------
    frame_gutter : list
        A list of the resulting extractions, one item per line of text found.
    '''
    gutter_labels = gutter(x_frame)
    gutter_labels_sorted = sort_labels(np.array(gutter_labels), np.array([np.mean(x) for x in x_frame]))
    frame_gutter = []
    for gutter_label in gutter_labels_sorted:
        gdx = gutter_labels == gutter_label
        x = x_frame[gdx]
        y = y_frame[gdx]
        text = text_frame[gdx]
        slope = slope_frame[gdx]
        kwargs_cluster['gutter_label'] = gutter_label
        frame_slope = cluster_by_slope(x, y, text, slope, kwargs_cluster, kwargs_dbscan)
        frame_gutter += frame_slope
    return frame_gutter


def cluster_by_frame(data_by_frame, kwargs_cluster, kwargs_dbscan):
    reduced_data = OrderedDict()
    for frame, value in data_by_frame.items():
        reduced_data[frame] = []
        slope_frame = np.array(copy.deepcopy(value['slope'])).reshape(-1, 1)
        x_frame = np.array(copy.deepcopy(value['x']))
        y_frame = np.array(copy.deepcopy(value['y']))
        text_frame = copy.deepcopy(value['text'])
        # pad with empty strings to keep array sizes the same
        for t in text_frame:
            t.append('')
        text_frame = np.array(text_frame)
        frame_gutter = cluster_by_gutter(x_frame, y_frame, text_frame, slope_frame, kwargs_cluster, kwargs_dbscan)
        reduced_data[frame] += frame_gutter
    return reduced_data
