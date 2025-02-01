'''
Polygon/Freehand Tool Reducer Using DBSCAN
------------------------------------------
This module provides functions to reduce the polygon extractions from
:mod:`panoptes_aggregation.extractors.polygon_extractor` using the
algorithm DBSCAN.
'''
from sklearn.cluster import DBSCAN
import numpy as np
from collections import OrderedDict
from .reducer_wrapper import reducer_wrapper
from .polygon_reducer_utils import IoU_metric_polygon, cluster_average_last, cluster_average_intersection, cluster_average_union
from .text_utils import tokenize
import warnings
import shapely

with warnings.catch_warnings():
    # collatex is a bit old, we can safely ignore this message as the display
    # functions are optional and never used in this code
    warnings.filterwarnings('ignore', category=DeprecationWarning, message='Importing display')
    import collatex as col

DEFAULTS = {
    'min_samples': {'default': 2, 'type': int},
    'eps': {'default': 0.5, 'type': float},
    'average_type': {'default': 'last', 'type': str}
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
        dictionaries of the form `{'polygon': shapely.geometry.polygon.Polygon,
        'gold_standard': bool}`.
    '''
    data_by_frame = {}
    row_ct = {}
    user_ct = 0
    for user_ct, data in enumerate(data_list):
        for frame, value in data.items():
            data_by_frame.setdefault(frame, {'X': [], 'data': []})
            row_ct.setdefault(frame, 0)
            gs = value.get('gold_standard', False)
            for x, y in zip(value['points']['x'], value['points']['y']):
                xy = np.array([x, y]).T
                # Find the timestamp
                data_by_frame[frame]['data'].append({
                    'polygon': shapely.Polygon(xy),
                    'gold_standard': gs
                })
                data_by_frame[frame]['X'].append([row_ct[frame], user_ct])
                row_ct[frame] += 1
    return data_by_frame


@reducer_wrapper(
    process_data=process_data,
    defaults_data=DEFAULTS,
    user_id=False,
    created_at=True,
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
        * `See DBSCAN <http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html>`_
        * `created_at` : A list of when the classifcations were made.

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
    created_at = np.array(kwargs_dbscan.pop('created_at'))
    average_type = kwargs_dbscan.pop('average_type', 'last')
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
            # Create a list of when the different polygons were created, assuming the order X matches the order of created_at_array.
            # The cteaed_at list originally provided is when all of the classifications per user were added
            created_at_full_array = np.array([created_at[int(user_id)] for user_id in X[:, 1]])
            # Looping through each cluster
            for label in set(labels_array):
                if label > -1:
                    cdx = labels_array == label
                    # number of points in the cluster
                    clusters[frame].setdefault('clusters_count', []).append(int(cdx.sum()))
                    # Now find the "average" of this cluster, using the provided average choice
                    cluster_average = avg(data[cdx], created_at=created_at_full_array[cdx])
                    # Find the x and y values of this polygon
                    average_polygon = np.array(list(cluster_average.boundary.coords))
                    # Add to the dictionary
                    clusters[frame].setdefault('clusters_x', []).append(average_polygon[:, 0].tolist())
                    clusters[frame].setdefault('clusters_y', []).append(average_polygon[:, 1].tolist())
    return clusters
