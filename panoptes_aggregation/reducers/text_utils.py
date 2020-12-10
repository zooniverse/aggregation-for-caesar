'''
Text aggregation utilities
--------------------------
This module provides utility functions used in the polyton-as-line-text-reducer code from
:mod:`panoptes_aggregation.reducers.poly_line_text_reducer`.
'''
import collatex as col
from collections import OrderedDict, Counter
import copy
import numpy as np
from sklearn.cluster import DBSCAN
import re


def tokenize(self, contents):
    '''Tokenize only on space so angle bracket tags are not split'''
    return re.findall(r'[^\s$]+|[$]', contents)


# override the built-in tokenize
col.core_classes.WordPunctuationTokenizer.tokenize = tokenize


def extractor_index(x):
    edx = []
    i_prev = None
    e_prev = -1
    for i in x:
        if i_prev is None:
            i_prev = i
        else:
            if i != i_prev:
                i_prev = i
                e_prev = -1
        e_prev += 1
        edx.append(e_prev)
    return edx


def overlap(x, y, tol=0):
    '''Check if two line segments overlap

    Parameters
    ----------
    x : list
        A list with the start and end point of the first line segment
    y : lits
        A list with the start and end point of the second line segment
    tol : float
        The tolerance to consider lines overlapping. Default 0, positive
        value indicate small overlaps are not considered, negative values
        indicate small gaps are not considered.

    Returns
    -------
    overlap : bool
        True if the two line segments overlap, False otherwise
    '''
    return (x[1] - tol) >= (y[0] + tol) and (y[1] - tol) >= (x[0] + tol)


def gutter(lines_in, tol=0):
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
        indicates what side of the gutter(s) the input line segment is on.
    '''
    if len(lines_in) > 0:
        lines = np.array([[min(l), max(l)] for l in lines_in])
        overlap_lines = []
        for ldx, l in enumerate(lines):
            if ldx == 0:
                overlap_lines = np.array([l])
            else:
                o_lines = np.array([overlap(o, l, tol=tol) for o in overlap_lines])
                if o_lines.any():
                    comp = np.vstack([overlap_lines[o_lines], l])
                    overlap_lines[o_lines] = [comp.min(), comp.max()]
                    overlap_lines = np.vstack(list({tuple(row) for row in overlap_lines}))
                else:
                    overlap_lines = np.vstack([overlap_lines, l])
        overlap_lines.sort(axis=0)
        gutter_label = -np.ones(len(lines), dtype=int)
        for odx, o in enumerate(overlap_lines):
            gdx = np.array([overlap(o, l, tol=tol) for l in lines])
            gutter_label[gdx] = odx
        # gutter_label[mask_out] = -1
        return gutter_label
    else:
        return np.array([])


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
    '''A function that finds the average of an array of angles that are
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
        A list of cluster lables, one label for each data point.
    data : np.array
        The data the lables belong to
    reducer : function (optional)
        The function used to combine the data for each label.  Default: np.mean
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
    consensus_text : str
        A string with the consensus sentence
    '''
    text_filter = [list(filter(('').__ne__, text)) for text in clusters_text if text]
    most_common = [Counter(text).most_common(1)[0] for text in text_filter if text]
    if len(most_common) == 0:
        return 0.0, ''
    else:
        common_text, max_counts = zip(*most_common)
        return sum(max_counts) / len(max_counts), ' '.join(common_text)


def cluster_by_word(
    word_line,
    xy_line,
    text_line,
    annotation_labels,
    kwargs_cluster,
    kwargs_dbscan
):
    '''A function to take the annotations for one line of text and cluster them
    based on the words in the line.

    Parameters
    ----------
    word_line : np.array
        An nx1 array with the x-position of each dot in the rotated coordinate frame.
    xy_line : np.array
        An nx2 array with the non-rotated (x, y) positions of each dot.
    text_line : np.array
        An nx1 array with the text for each dot.
    annotation_labels : np.array
        An nx1 array with a label indicating what annotaiton each word belongs to.
    kwargs_cluster : dict
        A dictionary containing the `eps_*` and `dot_freq` keywords
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
    db_words = DBSCAN(eps=kwargs_cluster['eps_word'], **kwargs_dbscan).fit(word_line)
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


def align_words(
    word_line,
    xy_line,
    text_line,
    kwargs_cluster,
    kwargs_dbscan
):
    '''A function to take the annotations for one line of text, aligns the words,
    and finds the end-points for the line.

    Parameters
    ----------
    word_line : np.array
        An nx1 array with the x-position of each dot in the rotated coordinate frame.
    xy_line : np.array
        An nx2 array with the non-rotated (x, y) positions of each dot.
    text_line : np.array
        An nx1 array with the text for each dot.
    gs_line : np.array
        An array of bools indicating if the annotation was made in gold standard mode
    kwargs_cluster : dict
        A dictionary containing the `eps_*` and `dot_freq` keywords
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
    db_words = DBSCAN(eps=kwargs_cluster['eps_word'], min_samples=1, **kwargs_dbscan).fit(word_line)
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
            if t.strip() != '':
                key = str(tdx)
                collation.add_plain_witness(key, t)
                witness_key.append(key)
        if len(collation.witnesses) > 0:
            alignment_table = col.collate(collation, near_match=True, segmentation=False)
            for cols in alignment_table.columns:
                word_dict = cols.tokens_per_witness
                word_list = []
                for key in witness_key:
                    if len(word_dict) >= kwargs_cluster['min_word_count']:
                        word_list.append(str(word_dict.get(key, [''])[0]))
                    else:
                        word_list.append('')
                clusters_text.append(word_list)
            # fix memory leak by deleting this
            del alignment_table
    return clusters_x, clusters_y, clusters_text


def cluster_by_line(
    xy_rotate,
    xy_gutter,
    text_gutter,
    annotation_labels,
    gs_gutter,
    data_index_gutter,
    ext_index_gutter,
    kwargs_cluster,
    kwargs_dbscan
):
    '''A function to take the annotations for one `slope_label` and cluster them
    based on perpendicular distance (e.g. lines of text).

    Parameters
    ----------
    xy_rotate : np.array
        An array of shape nx2 containing the (x, y) positions of *each* dot drawn in the
        rotate coordinate frame.
    xy_gutter : np.array
        An array of shape nx2 containing the (x, y) positions for *each* dot drawn.
    text_gutter : np.array
        An array of shape nx1 containing the text for *each* dot drawn. Note: each
        annotation has an empty string added to the end so this array has the same
        shape as `xy_slope`.
    annotation_labels : np.array
        An array of shape nx1 containing a unique label indicating what annotation
        each position/text came from.  This information is used to ensure one annotation
        does not span multiple lines.
    gs_gutter : np.array
        An array of bools indicating if the annotation was made in gold standard mode
    data_index_gutter : np.array
        An array of indices indicating what classification each classification came from
    ext_index_gutter : np.array
        A list of extractor indices used to map the reduction to the extract
    kwargs_cluster : dict
        A dictionary containing the `eps_*`, and `dot_freq` keywords
    kwargs_dbscan : dict
        A dictionary containing all the other DBSCAN keywords

    Returns
    -------
    frame_lines : list
        A list of reductions, one for each line. Each reduction is a dictionary
        containing the information for the line.
    '''
    if kwargs_cluster['dot_freq'] not in ['word', 'line']:
        raise ValueError('dot_freq needs to be either "word" or "line"')
    lines = xy_rotate[:, 1].reshape(-1, 1)
    words = xy_rotate[:, 0].reshape(-1, 1)
    a_lables = np.unique(annotation_labels)
    avg_lines = np.array([lines[annotation_labels == a].mean() for a in a_lables]).reshape(-1, 1)
    db_lines = DBSCAN(eps=kwargs_cluster['eps_line'], **kwargs_dbscan).fit(avg_lines)
    line_labels = sort_labels(db_lines.labels_, avg_lines)
    frame_lines = []
    for line_label in line_labels:
        ldx = db_lines.labels_ == line_label
        # this ensures that full annotations stay together
        adx = np.zeros(len(lines), dtype=bool)
        for a_label in a_lables[ldx]:
            adx |= annotation_labels == a_label
        if kwargs_cluster['dot_freq'] == 'word':
            clusters_x, clusters_y, clusters_text = cluster_by_word(
                words[adx],
                xy_gutter[adx],
                text_gutter[adx],
                annotation_labels[adx],
                kwargs_cluster,
                kwargs_dbscan
            )
        elif kwargs_cluster['dot_freq'] == 'line':
            clusters_x, clusters_y, clusters_text = align_words(
                words[adx],
                xy_gutter[adx],
                text_gutter[adx],
                kwargs_cluster,
                kwargs_dbscan
            )
        consensus_score_value, consensus_text = consensus_score(clusters_text)
        line_dict = {
            'clusters_x': clusters_x,
            'clusters_y': clusters_y,
            'clusters_text': clusters_text,
            'number_views': ldx.sum(),
            'consensus_score': consensus_score_value,
            'consensus_text': consensus_text,
            'line_slope': float(kwargs_cluster['avg_slope']),
            'slope_label': int(kwargs_cluster['slope_label']),
            'gutter_label': int(kwargs_cluster['gutter_label']),
            'gold_standard': gs_gutter[ldx].tolist(),
            'data_index': data_index_gutter[ldx].tolist(),
            'extract_index': ext_index_gutter[ldx].tolist()
        }
        if len(line_dict['clusters_x']) > 0:
            frame_lines.append(line_dict)
    return frame_lines


def cluster_by_gutter(
    x_slope,
    y_slope,
    text_slope,
    gs_slope,
    data_index_slope,
    ext_index_slope,
    kwargs_cluster,
    kwargs_dbscan
):
    '''A function to take the annotations for each frame of a subject and group them
    based on what side of the page gutter they are on.

    Parameters
    ----------
    x_slope : np.array
        A list-of-lists of the x values for each drawn dot. There is one item in the
        list for annotation made by the user.
    y_slope : np.array
        A list-of-lists of the y values for each drawn dot. There is one item in the
        list for annotation made by the user.
    text_slope : np.array
        A list-of-lists of the text for each drawn dot. There is one item in the
        list for annotation made by the user.
    gs_slope : np.array
        A list of bools indicating if the annotation was made in gold standard mode
    data_index_slope : np.array
        A list of indices indicating what classification each classification came from
    ext_index_slope : np.array
        A list of extractor indices used to map the reduction to the extract
    kwargs_cluster : dict
        A dictionary containing the `eps_*` and `dot_freq` keywords
    kwargs_dbscan : dict
        A dictionary containing all the other DBSCAN keywords

    Returns
    -------
    frame_gutter : list
        A list of the resulting extractions, one item per line of text found.
    '''
    c = np.cos(np.deg2rad(-kwargs_cluster['avg_slope']))
    s = np.sin(np.deg2rad(-kwargs_cluster['avg_slope']))
    x_rotate = np.array([np.array(x) * c - np.array(y) * s for x, y in zip(x_slope, y_slope)], dtype=object)
    y_rotate = np.array([np.array(y) * c + np.array(x) * s for x, y in zip(x_slope, y_slope)], dtype=object)
    gutter_labels = gutter(x_rotate, tol=kwargs_cluster['gutter_tol'])
    gutter_labels_sorted = sort_labels(np.array(gutter_labels), np.array([np.mean(x) for x in x_rotate]))
    frame_gutter = []
    for gutter_label in gutter_labels_sorted:
        gdx = gutter_labels == gutter_label
        annotation_label = np.hstack([np.zeros(len(i)) + idx for idx, i in enumerate(x_slope[gdx])])
        xy_rotate = np.array(list(zip(np.hstack(x_rotate[gdx]), np.hstack(y_rotate[gdx]))))
        xy_gutter = np.array(list(zip(np.hstack(x_slope[gdx]), np.hstack(y_slope[gdx]))))
        text_gutter = np.hstack(text_slope[gdx])
        kwargs_cluster['gutter_label'] = gutter_label
        frame_lines = cluster_by_line(
            xy_rotate,
            xy_gutter,
            text_gutter,
            annotation_label,
            gs_slope[gdx],
            data_index_slope[gdx],
            ext_index_slope[gdx],
            kwargs_cluster,
            kwargs_dbscan
        )
        frame_gutter += frame_lines
    return frame_gutter


def cluster_by_slope(
    x_frame,
    y_frame,
    text_frame,
    slope_frame,
    gs_frame,
    data_index_frame,
    ext_index_frame,
    kwargs_cluster,
    kwargs_dbscan
):
    '''A function to take the annotations for one `gutter_label` and cluster them
    based on what slope the transcription is.

    Parameters
    ----------
    x_frame : np.array
        A list-of-lists of the x values for each drawn dot. There is one item in the
        list for annotation made by the user.
    y_frame : np.array
        A list-of-lists of the y values for each drawn dot. There is one item in the
        list for annotation made by the user.
    text_frame : np.array
        A list-of-lists of the text for each drawn dot. There is one item in the
        list for annotation made by the user. The inner text lists are padded with
        an empty string at the end so there is the same number of words as there are
        dots.
    slope_frame : np.array
        A list of the slopes (in deg) for each annotation
    gs_frame : np.array
        A list of bools indicating if the annotation was made in gold standard mode
    data_index_frame : np.array
        A list of indices indicating what classification each classification came from
    ext_index_frame : np.array
        A list of extractor indices used to map the reduction to the extract
    kwargs_cluster : dict
        A dictionary containing the `eps_*` and `dot_freq` keywords
    kwargs_dbscan : dict
        A dictionary containing all the other DBSCAN keywords

    Returns
    -------
    frame_slope : list
        A list of the resulting extractions, one item per line of text found.
    '''
    frame_slope = []
    if len(slope_frame) >= 1:
        db_slope = DBSCAN(eps=kwargs_cluster['eps_slope'], metric=angle_metric, **kwargs_dbscan).fit(slope_frame)
        slope_labels = sort_labels(db_slope.labels_, slope_frame, reducer=avg_angle, descending=True)
        for slope_label in slope_labels:
            sdx = db_slope.labels_ == slope_label
            avg_slope = avg_angle(slope_frame[sdx])
            kwargs_cluster['avg_slope'] = avg_slope
            kwargs_cluster['slope_label'] = slope_label
            frame_gutter = cluster_by_gutter(
                x_frame[sdx],
                y_frame[sdx],
                text_frame[sdx],
                gs_frame[sdx],
                data_index_frame[sdx],
                ext_index_frame[sdx],
                kwargs_cluster,
                kwargs_dbscan
            )
            frame_slope += frame_gutter
    return frame_slope


def cluster_by_frame(
    data_by_frame,
    kwargs_cluster,
    kwargs_dbscan,
    user_ids_input,
    low_consensus_threshold
):
    reduced_data = OrderedDict()
    low_consensus_lines = 0
    number_of_lines = 0
    for frame, value in data_by_frame.items():
        reduced_data[frame] = []
        gs_frame = np.array(copy.deepcopy(value['gold_standard']))
        data_index_frame = np.array(copy.deepcopy(value['data_index']))
        slope_frame = np.array(copy.deepcopy(value['slope'])).reshape(-1, 1)
        x_frame = np.array(copy.deepcopy(value['x']), dtype=object)
        y_frame = np.array(copy.deepcopy(value['y']), dtype=object)
        text_frame = copy.deepcopy(value['text'])
        ext_index_frame = np.array(extractor_index(value['data_index']))
        # pad with empty strings to keep array sizes the same
        for t in text_frame:
            t.append('')
        text_frame = np.array(text_frame, dtype=object)
        frame_slope = cluster_by_slope(
            x_frame,
            y_frame,
            text_frame,
            slope_frame,
            gs_frame,
            data_index_frame,
            ext_index_frame,
            kwargs_cluster,
            kwargs_dbscan
        )
        number_of_lines += len(frame_slope)
        for line in frame_slope:
            data_index = line.pop('data_index')
            line['user_ids'] = [user_ids_input[di] for di in data_index]
            if line['consensus_score'] < low_consensus_threshold:
                line['low_consensus'] = True
                line['flagged'] = True
                low_consensus_lines += 1
            else:
                line['low_consensus'] = False
                line['flagged'] = False
        reduced_data[frame] += frame_slope
    reduced_data['low_consensus_lines'] = low_consensus_lines
    reduced_data['transcribed_lines'] = number_of_lines
    reduced_data['reducer'] = 'poly_line_text_reducer'
    return reduced_data
