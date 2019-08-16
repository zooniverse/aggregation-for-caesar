'''
Utilities for `optics_line_text_reducer`
----------------------------------------
This module provides utilities used to reduce the polygon-text extractions
for :mod:`panoptes_aggregation.reducers.optics_line_text_reducer`.  It
assumes that all extracts are full lines of text in the document.
'''
import numpy as np
import Levenshtein
import collections
import copy
import re
from sklearn.cluster import DBSCAN
from .shape_metric import angle_distance, avg_angle


def strip_tags(s):
    '''Remove square bracket tags from text and consolidating whitespace

    Parameters
    ----------
    s : string
        The input string

    Returns
    -------
    clean_s : string
        The cleaned string
    '''
    no_brackets = re.sub('[\[].*?[\]]', '', s)  # noqa: W605
    unify_space = ' '.join(no_brackets.split())
    return unify_space


def metric(a, b, data_in=[]):
    '''Calculate the distance between two drawn lines that have text
    associated with them.  This distance is found by summing the euclidean
    distance between the start points of each line, the euclidean distance
    between the end poitns of each line, and the Levenshtein distance
    of the text for each line.  The Levenshtein distance is done after
    stripping text tags and consolidating whitespace.

    To use this metric within the clustering code without haveing to
    precompute the full distance matrix `a` and `b` are index mappings to
    the data contained in `data_in`.  `a` and `b` also contain the user
    information that is used to help prevent self-clustering.

    Parameters
    ----------
    a : list
        A two element list containing [index mapping to data, index mapping to user]
    b : list
        A two element list containing [index mapping to data, index mapping to user]
    data_in : list
        A list of dicts that take the form
        {`x`: [start_x, end_x], `y`: [start_y, end_y], 'text': ['text for line'], 'gold_standard', bool}
        There is one element in this list for each classification made.

    Returns
    -------
    distance: float
        The distance between `a` and `b`
    '''
    if a[0] == b[0]:
        # The same data point, the distance is zero
        return 0
    if a[1] == b[1]:
        # The same users, distance is inf
        return np.inf
    data_a = data_in[int(a[0])]
    data_b = data_in[int(b[0])]
    dx = (np.array(data_a['x']) - np.array(data_b['x']))**2
    dy = (np.array(data_a['y']) - np.array(data_b['y']))**2
    dt = Levenshtein.distance(
        strip_tags(data_a['text'][0]),
        strip_tags(data_b['text'][0])
    )
    return np.sqrt(dx + dy).sum() + dt


def get_min_samples(N):
    '''Get the `min_samples` attribute based on the number of
    users who have transcribed the subject.  These values were
    found based on example data from ASM.

    Parameters
    ----------
    N : integer
        The number of users who have see the subject

    Returns
    -------
    min_samples : integer
        The value to use for the min_samples keyword in OPTICS
    '''
    if N <= 6:
        return 2
    elif N <= 10:
        return 3
    elif N <= 15:
        return 4
    elif N <= 20:
        return 5
    else:
        return int(0.25 * N)


def remove_user_duplication(labels_, core_distances_, users):
    '''Make sure a users only shows up in a cluster at most once.
    If a user does show up more than once in a cluster take the point
    with the smallest core distance, all others are assigned as noise (-1).

    Parameters
    ----------
    labels_ : numpy.array
        A list containing the cluster labels for each data point
    core_distances_ : numpy.array
        A list of core distance for each data point
    users : numpy.array
        A list of indices that map to users, one for each data point

    Returns
    -------
    clean_labels_ : numpy.array
        A list containing the new cluster labels.
    '''
    clean_labels = copy.deepcopy(labels_)
    unique_labels = np.unique(labels_)
    gdx = unique_labels > -1
    for l in unique_labels[gdx]:
        cdx = labels_ == l
        user_counts = collections.Counter(users[cdx]).most_common()
        if user_counts[0][1] > 1:
            clean_labels_cdx = clean_labels[cdx]
            for user_count in user_counts:
                udx = users[cdx] == user_count[0]
                clean_labels_cdx_udx = clean_labels_cdx[udx]
                if user_count[1] > 1:
                    min_idx = core_distances_[cdx][udx].argmin()
                    mask = np.ones(udx.sum(), dtype=bool)
                    mask[min_idx] = False
                    clean_labels_cdx_udx[mask] = -1
                else:
                    break
                clean_labels_cdx[udx] = clean_labels_cdx_udx
            clean_labels[cdx] = clean_labels_cdx
    return clean_labels


def remove_nans(input):
    '''Remove numpy nan's from a list and replace them with `None`'''
    return [i if np.isfinite(i) else None for i in input]


def cluster_of_one(X, data, user_ids, extract_index):
    '''Create "clusters of one" out of the data passed in. Lines of text
    identified as noise are kept around as clusters of one so they can be
    displayed in the front-end to the next user.

    Parameters
    ----------
    X : list
        A nx2 list with each row containing [index mapping to data, index mapping to user]
    data: list
        A list containing dictionaries with the original data that X maps to, of the form
        `{'x': [start_x, end_x], 'y': [start_y, end_y], 'text': ['text for line'], 'gold_standard': bool}`.
    user_ids: list
        A list of user_ids (The second column of X maps to this list)
    extract_index: list
        A list of n values with the extract index for each of rows in X

    Returns
    -------
    clusters: list
        A list with n clusters each containing only one calssification
    '''
    clusters = []
    for rdx, row in enumerate(X):
        index = int(row[0])
        user_index = int(row[1])
        line = data[index]
        dx = line['x'][-1] - line['x'][0]
        dy = line['y'][-1] - line['y'][0]
        slope = np.rad2deg(np.arctan2(dy, dx)) % 360
        value = {
            'clusters_x': line['x'],
            'clusters_y': line['y'],
            'clusters_text': [[w] for w in line['text'][0].split()],
            'number_views': 1,
            'line_slope': slope,
            'consensus_score': 1.0,
            'user_ids': remove_nans([user_ids[user_index]]),
            'extract_index': [extract_index[rdx]],
            'gold_standard': [line['gold_standard']]
        }
        clusters.append(value)
    return clusters


def order_lines(frame_in, angle_eps=30, gutter_eps=150):
    '''Place the identified lines within a single frame in reading order

    Parameters
    ----------
    frame : list
        A list of identified transcribed lines (one frame from
        panoptes_aggregation.reducers.optics_line_text_reducer.optics_line_text_reducer)
    angle_eps : float
        The DBSCAN `eps` value to use for the slope clustering
    gutter_eps : float
        The DBSCAN `eps` value to use for the column clustering

    Returns
    -------
    frame_ordered : list
        The identified transcribed lines in reading order. The `slope_label` and
        `gutter_label` values are added to each line to indicate what cluster it
        belongs to.
    '''
    if len(frame_in) == 0:
        return frame_in
    xy_start = np.array([[l['clusters_x'][0], l['clusters_y'][0]] for l in frame_in])
    xy_end = np.array([[l['clusters_x'][1], l['clusters_y'][1]] for l in frame_in])
    slope = np.array([l['line_slope'] for l in frame_in])
    frame = np.array(frame_in)
    frame_ordered = []
    # cluster by angle
    db_angle = DBSCAN(min_samples=1, eps=angle_eps, metric=angle_distance)
    db_angle.fit(slope.reshape(-1, 1))

    # sort angle clusters
    distance_to_zero = []
    for l in np.unique(db_angle.labels_):
        cdx = db_angle.labels_ == l
        a = avg_angle(slope[cdx])
        distance_to_zero.append([l, a, angle_distance(a, 0)])
    distance_to_zero = np.array(distance_to_zero)
    distance_to_zero = distance_to_zero[distance_to_zero[:, 2].argsort()]
    slope_label = 0

    for angle_row in distance_to_zero:
        # find midpoints of each line in angle cluster
        cdx = db_angle.labels_ == angle_row[0]
        mid_points = (xy_end[cdx] + xy_start[cdx]) / 2
        mid_point = mid_points.mean(axis=0)

        # rotate by this angle
        c = np.cos(np.deg2rad(-angle_row[1]))
        s = np.sin(np.deg2rad(-angle_row[1]))
        R = np.array([[c, s], [-s, c]])
        start_points_rot = np.dot(xy_start[cdx] - mid_point, R) + mid_point

        # cluster in rotated `x` direction
        db_start = DBSCAN(min_samples=1, eps=gutter_eps)
        db_start.fit(start_points_rot[:, 0].reshape(-1, 1))

        # sort column clusters
        x_distance_to_zero = []
        for ml in np.unique(db_start.labels_):
            mdx = db_start.labels_ == ml
            x_distance_to_zero.append([ml, start_points_rot[mdx, 0].mean()])
        x_distance_to_zero = np.array(x_distance_to_zero)
        x_distance_to_zero = x_distance_to_zero[x_distance_to_zero[:, 1].argsort()]
        gutter_label = 0

        for x_row in x_distance_to_zero:
            mdx = db_start.labels_ == x_row[0]
            # for each column sort in `y` direction
            y_order = start_points_rot[mdx, 1].argsort()
            # append to final list
            new_frames = list(frame[cdx][mdx][y_order])
            for nf in new_frames:
                nf['line_slope'] = angle_row[1]
                nf['slope_label'] = slope_label
                nf['gutter_label'] = gutter_label
            frame_ordered += new_frames
            gutter_label += 1
        slope_label += 1
    return frame_ordered
