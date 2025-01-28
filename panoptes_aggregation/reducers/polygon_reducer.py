'''
Polygon/freehand Tool Reducer using dbscan
------------------------------------------------
This module provides functions to reduce the polygon extractions from
:mod:`panoptes_aggregation.extractors.polygon_extractor` using the
algorithm DBSCAN.
'''
from sklearn.cluster import DBSCAN
import numpy as np
from collections import OrderedDict
from .reducer_wrapper import reducer_wrapper
from .text_utils import tokenize
import warnings
import shapely
import datetime
import time as time_module

with warnings.catch_warnings():
    # collatex is a bit old, we can safely ignore this message as the display
    # functions are optional and never used in this code
    warnings.filterwarnings('ignore', category=DeprecationWarning, message='Importing display')
    import collatex as col

DEFAULTS = {
    'min_samples': {'default': 2, 'type': int},
    'eps': {'default': 0.5, 'type': float},
    'average_type': {'default': 'union', 'type': str}
}

# override the built-in tokenize
col.core_classes.WordPunctuationTokenizer.tokenize = tokenize


def process_data(data_list):
    '''Process a list of extractions into a dictionary organized by `frame`

    Parameters
    ----------
    data_list : list
        A list of extractions created by
        :meth:`panoptes_aggregation.extractors.polygon_extractor`

    Returns
    -------
    processed_data : dict
        A dictionary with one key for each frame of the subject. The value for each key
        is a dictionary with two keys `X` and `data`. `X` is a 2D array with each row
        mapping to the data held in `data`.  The first column contains row indices
        and the second column is an index assigned to each user. `data` is a list of
        dictionaries of the form `{'polygon': shapely_polygon,
        'time': timestamp_of_extraction, 'gold_standard': bool}`.
    '''
    data_by_frame = {}
    row_ct = {}
    user_ct = 0
    for user_ct, data in enumerate(data_list):
        for frame, value in data.items():
            data_by_frame.setdefault(frame, {'X': [], 'data': []})
            row_ct.setdefault(frame, 0)
            gs = value.get('gold_standard', False)
            # Convert the UTC fomrta time string into a unix time stamp
            time = time_module.mktime(datetime.datetime.strptime(value.get('time'),"%Y-%m-%dT%X.%fZ").timetuple())
            for x, y in zip(value['points']['x'], value['points']['y']):
                xy = np.array([x, y]).T
                # Find the timestamp
                data_by_frame[frame]['data'].append({
                    'polygon': shapely.Polygon(xy),
                    'time': time,
                    'gold_standard': gs
                })
                data_by_frame[frame]['X'].append([row_ct[frame], user_ct])
                row_ct[frame] += 1
    return data_by_frame


def polygon_gap_ratio(polygon_xy):
    polygon_length = np.sum([((polygon_xy[i+1, 0] - polygon_xy[i, 0])**2 +
                              (polygon_xy[i+1, 1] - polygon_xy[i, 1])**2)**0.5
                             for i in range(len(polygon_xy)-1)])
    gap_length = ((polygon_xy[-1, 0] - polygon_xy[0, 0])**2 +
                  (polygon_xy[-1, 1] - polygon_xy[0, 1])**2)**0.5
    return gap_length/polygon_length


# This needs a list of shapely objects to work!
def IoU_metric_polygon(a, b, data_in=[]):
    if a[0] == b[0]:
        # The same data point, the distance is zero
        return 0
    if a[1] == b[1]:
        # The same users, distance is inf
        return np.inf

    # Now need to find the actual data
    geo1 = data_in[int(a[0])]['polygon']
    geo2 = data_in[int(b[0])]['polygon']

    intersection = 0
    if geo1.intersects(geo2):
        intersection = geo1.intersection(geo2).area

    union = geo1.union(geo2).area

    if union == 0:
        # catch divide by zero (i.e. cases when neither shape has an area)
        return np.inf

    return 1 - intersection / union


def cluster_average_last(data):
    times = [data[i]['time'] for i in range(len(data))]
    time_order = np.argsort(times)
    # Select the last polygon to be created
    last = data[time_order[-1]]['polygon']
    return last


def cluster_average_intersection(data):
    polygon_list = [data[i]['polygon'] for i in range(len(data))]
    # Just one object, so return it as it is its own average
    if isinstance(polygon_list, shapely.geometry.polygon.Polygon) or len(polygon_list)==1:
        return polygon_list
    # There must now be tw polygons to average
    intersection_average = polygon_list[0].intersection(polygon_list[1])
    # If there are any other
    if len(polygon_list) > 2:
        for i in range(2, len(polygon_list)):
            intersection_average = intersection_average.intersection(polygon_list[i])
    if isinstance(intersection_average, shapely.geometry.collection.GeometryCollection):
        for geo in intersection_average.geoms:
            if isinstance(geo, shapely.geometry.polygon.Polygon):
                intersection_average = geo
    return intersection_average


def cluster_average_union(data):
    polygon_list = [data[i]['polygon'] for i in range(len(data))]
    # Just one object, so return it as it is its own average
    if isinstance(polygon_list, shapely.geometry.polygon.Polygon) or len(polygon_list)==1:
        return polygon_list
    # There must now be tw polygons to average
    union_full = polygon_list[0].union(polygon_list[1])
    # If there are any other
    if len(polygon_list) > 2:
        for i in range(2, len(polygon_list)):
            union_full = union_full.union(polygon_list[i])
    if isinstance(union_full, shapely.geometry.collection.GeometryCollection):
        for geo in union_full.geoms:
            if isinstance(geo, shapely.geometry.polygon.Polygon):
                union_full = geo
    return union_full


@reducer_wrapper(
    process_data=process_data,
    defaults_data=DEFAULTS,
    user_id=False,
    output_kwargs=True
)
def polygon_reducer(data_by_frame, **kwargs_dbscan):
    '''Cluster a polygon or freehand tool using DBSCAN
    

    Parameters
    ----------
    data_by_tool : dict
        A dictionary returned by :meth:`process_data`
    average_type : str
        Either "union", which returns the union of the cluster, "intersection"
        which retruns the intersection of the cluster or "last", which returns
        the last polygon to be annotated in the cluster.

    kwargs :
        `See DBSCAN <http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html>`_

    Returns
    -------
    reduction : dict
        A dictionary with the following keys for each frame

        * `cluster_labels` : A list of cluster labels for **all** shapes
        * `clusters_count` : The number of points in each **cluster** found
        * `clusters_x` : A list of the x values of each cluster
        * `clusters_y` : A list of the y values of each cluster

        A custom "IoU" metric type is used.
    '''
    average_type = kwargs_dbscan.pop('average_type', 'union')
    if average_type == "intersection":
        avg = cluster_average_intersection
    elif average_type == "last":
        avg = cluster_average_last
    elif average_type == "union":
        avg = cluster_average_union
    else:
        raise ValueError("`average_type` not valid. Should be either `intersection`, `union` or `last`.")

    clusters = OrderedDict()
    for frame, value in data_by_frame.items():
        clusters[frame] = OrderedDict()
        X = np.array(value['X'])
        data = np.array(value['data'])
        num_polygons = len(data)

        min_samples = max(2, kwargs_dbscan.pop('min_samples'))

        # default each polygon in no cluster
        clusters[frame]['cluster_labels'] = [-1] * num_polygons
        if num_polygons >= min_samples:  # If clustering can be done
            db = DBSCAN(
                metric=IoU_metric_polygon,
                metric_params={'data_in': data},
                min_samples=min_samples,
                **kwargs_dbscan
            )
            db.fit(X)
            labels_array = db.labels_
            # Update the cluster labels of polygons
            clusters[frame]['cluster_labels'] = labels_array.tolist()
            # Looping through each cluster
            for label in set(labels_array):
                if label > -1:
                    cdx = labels_array == label
                    # number of points in the cluster
                    clusters[frame].setdefault('clusters_count', []).append(int(cdx.sum()))
                    # Now find the "average" of this cluster, using the provided average choice
                    cluster_average = avg(data[cdx])
                    # Find the x and y values of this polygon
                    average_polygon = np.array(list(cluster_average.boundary.coords))
                    # Add to the dictionary
                    clusters[frame].setdefault('clusters_x', []).append(average_polygon[:, 0].tolist())
                    clusters[frame].setdefault('clusters_y', []).append(average_polygon[:, 1].tolist())
    return clusters
