from collections import OrderedDict
import copy
import numpy as np
from sklearn.cluster import DBSCAN


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


def sort_labels(db_labels, data, reducer=np.mean, decending=False):
    labels = np.array(list(set(db_labels)))
    avg = [reducer(data[db_labels == l]) for l in labels]
    sdx = np.argsort(avg)
    if decending:
        sdx = sdx[::-1]
    return labels[sdx]


def cluster_by_word(word_line, xy_line, text_line, kwargs_cluster, kwargs_dbscan):
    db_words = DBSCAN(eps=kwargs_cluster['eps_word'], metric=kwargs_cluster['metric'], **kwargs_dbscan).fit(word_line)
    word_labels = sort_labels(db_words.labels_, word_line)
    clusters_x = []
    clusters_y = []
    clusters_text = []
    for word_label in word_labels:
        if word_label > -1:
            wdx = db_words.labels_ == word_label
            word_x, word_y = xy_line[wdx].mean(axis=0)
            word_list = [w for w in text_line[wdx] if w]
            clusters_x.append(word_x)
            clusters_y.append(word_y)
            clusters_text.append(word_list)
    return clusters_x, clusters_y, clusters_text


def cluster_by_line(xy_slope, text_slope, kwargs_cluster, kwargs_dbscan):
    c = np.cos(np.deg2rad(-kwargs_cluster['avg_slope']))
    s = np.sin(np.deg2rad(-kwargs_cluster['avg_slope']))
    R = np.array([[c, -s], [s, c]])
    xy_rotate = np.dot(xy_slope, R.T)
    lines = xy_rotate[:, 1].reshape(-1, 1)
    words = xy_rotate[:, 0].reshape(-1, 1)
    db_lines = DBSCAN(eps=kwargs_cluster['eps_line'], metric=kwargs_cluster['metric'], **kwargs_dbscan).fit(lines)
    line_labels = sort_labels(db_lines.labels_, lines)
    frame_lines = []
    for line_label in line_labels:
        if line_label > -1:
            ldx = db_lines.labels_ == line_label
            if kwargs_cluster['dot_freq'] == 'word':
                clusters_x, clusters_y, clusters_text = cluster_by_word(words[ldx], xy_slope[ldx], text_slope[ldx], kwargs_cluster, kwargs_dbscan)
            elif kwargs_cluster['dot_freq'] == 'line':
                raise Exception('`dot_freq="line"` not implimented yet')
            else:
                raise Exception('Not a valid `dot_freq` keyword')
            line_dict = {
                'clusters_x': clusters_x,
                'clusters_y': clusters_y,
                'clusters_text': clusters_text,
                'line_slope': kwargs_cluster['avg_slope'],
                'slope_label': kwargs_cluster['slope_label'],
                'gutter_label': kwargs_cluster['gutter_label']
            }
            frame_lines.append(line_dict)
    return frame_lines


def cluster_by_slope(x, y, text, slope, kwargs_cluster, kwargs_dbscan):
    db_slope = DBSCAN(eps=kwargs_cluster['eps_slope'], metric=angle_metric, **kwargs_dbscan).fit(slope)
    slope_labels = sort_labels(db_slope.labels_, slope, reducer=avg_angle, decending=True)
    frame_slope = []
    for slope_label in slope_labels:
        if slope_label > -1:
            sdx = db_slope.labels_ == slope_label
            xy_slope = np.array(list(zip(np.hstack(x[sdx]), np.hstack(y[sdx]))))
            text_slope = np.hstack(text[sdx])
            avg_slope = avg_angle(slope[sdx])
            kwargs_cluster['avg_slope'] = avg_slope
            kwargs_cluster['slope_label'] = slope_label
            frame_lines = cluster_by_line(xy_slope, text_slope, kwargs_cluster, kwargs_dbscan)
            frame_slope += frame_lines
    return frame_slope


def cluster_by_gutter(x_frame, y_frame, text_frame, slope_frame, kwargs_cluster, kwargs_dbscan):
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
