'''
Polygon/Freehand Tool Reducer Using DBSCAN
------------------------------------------
This module provides functions to reduce the polygon extractions from both
:mod:`panoptes_aggregation.extractors.polygon_extractor` and
:mod:`panoptes_aggregation.extractors.bezier_extractor` using the
algorithm DBSCAN.

All polygons are assumed to be closed. Any unclosed polygons will be closed.
'''
from sklearn.cluster import DBSCAN
import numpy as np
from collections import OrderedDict
from .reducer_wrapper import reducer_wrapper
from .polygon_reducer_utils import IoU_metric_polygon, cluster_average_last, \
    cluster_average_intersection, cluster_average_union, \
    cluster_average_median, IoU_distance_matrix_of_cluster, \
    IoU_cluster_mean_distance
import shapely

DEFAULTS = {
    'min_samples': {'default': 2, 'type': int},
    'eps': {'default': 0.5, 'type': float},
    'average_type': {'default': 'median', 'type': str}
}


def process_data(data):
    '''Process a list of extractions into a dictionary organized by `frame`, `Task` and `tool`.

    This also closes and simplifies the polygons.

    Parameters
    ----------
    data : list
        A list of extractions created by
        :meth:`panoptes_aggregation.extractors.polygon_extractor` or
        :meth:`panoptes_aggregation.extractors.bezier_extractor`

    Returns
    -------
    data_by_tool : dict
        A dictionary with one key for each frame of the subject and each tool used for the classification.
        The value for each key is a dictionary with two keys `X` and `data`. `X` is a 2D array with each row
        mapping to the data held in `data`.  The first column contains row indices
        and the second column is an index assigned to each user. `data` is a
        list of dictionaries, which contains the polygon data to be reduced. It
        is of the form
        `{'polygon': shapely.geometry.polygon.Polygon, 'gold_standard': bool}`.
    '''
    unique_frames = set(sum([[k for k in d.keys() if k.startswith('frame')] for d in data], []))
    data_by_tool = {}
    row_ct = {}
    user_ct = 0
    for frame in unique_frames:
        row_ct.setdefault(frame, {})
        data_by_tool[frame] = {}
        unique_tools = set(sum([['_'.join(k.split('_')[:-1]) for k in d.get(frame, {}).keys()] for d in data], []))
        for tool in unique_tools:
            # gold standard is not a tool
            if tool == 'gold':
                continue

            for user_ct, d in enumerate(data):
                if frame in d:
                    data_by_tool[frame].setdefault(tool, {'X': [], 'data': []})
                    if ('{0}_pathX'.format(tool) in d[frame]) and ('{0}_pathY'.format(tool) in d[frame]):
                        value = d[frame]
                        row_ct[frame].setdefault(tool, 0)
                        gs = value.get('gold_standard', False)
                        for x, y in zip(value['{0}_pathX'.format(tool)], value['{0}_pathY'.format(tool)]):
                            xy = np.array([x, y]).T
                            # Make into shapely object
                            polygon = shapely.Polygon(xy)
                            # If not simple polygon, use buffer to try to make simple
                            if not shapely.is_simple(polygon):
                                polygon = polygon.buffer(0)

                            # If part of multipolygon collection, choose largest polygon
                            if isinstance(polygon, shapely.geometry.collection.GeometryCollection)\
                                    or isinstance(polygon, shapely.geometry.multipolygon.MultiPolygon):
                                areas = [p.area for p in polygon.geoms]
                                polygon = polygon.geoms[np.argmax(areas)]

                            # Add this polygon to the dictionary only if it is a polygon
                            # It also must have a linear string as the boundary. This because the coords might need to be found later
                            if isinstance(polygon, shapely.geometry.polygon.Polygon) is True:
                                data_by_tool[frame][tool]['data'].append({
                                    'polygon': polygon,
                                    'gold_standard': gs
                                })
                                data_by_tool[frame][tool]['X'].append([row_ct[frame][tool], user_ct])
                                row_ct[frame][tool] += 1
    return data_by_tool


@reducer_wrapper(
    process_data=process_data,
    defaults_data=DEFAULTS,
    user_id=False,
    created_at=True,
    output_kwargs=True
)
def polygon_reducer(data_by_tool, **kwargs_dbscan):
    '''Cluster a polygon/freehand/Bezier tools using DBSCAN.

    There is a choice in how the cluster is averaged into a single cluster,
    with the varies choices listed below.

    A custom "IoU" metric type is used to measure the distance between the polygons.

    Parameters
    ----------
    data_by_tool : dict
        A dictionary returned by :meth:`process_data`

    kwargs :
        * `See DBSCAN <http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html>`_
        * `average_type` : Must be either "union", which returns the union of the cluster, "intersection" which returns the intersection of the cluster, "last", which returns the last polygon to be created in the cluster, or "median", which returns the polygon with the minimum total distance to the other polygons. Defaults to "median".
        * `created_at` : A list of when the classifcations were made.

    Returns
    -------
    reduction : dict
        A dictionary with the following keys for each frame, task and tool:

        * `tool*_cluster_labels` : A list of cluster labels for polygons provided for this frame and tool
        * `tool*_clusters_count` : The number of points in each **cluster** found for this frame and tool
        * `tool*_clusters_x` : A list of the x values of each cluster
        * `tool*_clusters_y` : A list of the y values of each cluster
        * `tool*_consensus` : A list of the the overall consensus of each cluster. A value of 1 is perfect agreement, a value of 0 is complete disagreement. This is found by subtracting`IoU_cluster_mean_distance` from 1

    '''
    average_type = kwargs_dbscan.pop('average_type', 'median')
    if average_type == "intersection":
        avg = cluster_average_intersection
    elif average_type == "last":
        avg = cluster_average_last
    elif average_type == "union":
        avg = cluster_average_union
    elif average_type == "median":
        avg = cluster_average_median
    else:
        raise Exception("`average_type` not valid. Should be either `intersection`, `union`, `median` or `last`.")

    min_samples = max(1, kwargs_dbscan.pop('min_samples', 2))
    created_at = np.array(kwargs_dbscan.pop('created_at'))

    clusters = OrderedDict()
    for frame, frame_data in data_by_tool.items():
        clusters[frame] = OrderedDict()
        for tool, value in frame_data.items():
            X = np.array(value['X'])
            data = np.array(value['data'])
            num_polygons = len(data)

            # default each polygon in no cluster
            clusters[frame]['{0}_cluster_labels'.format(tool)] = [-1] * num_polygons
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
                clusters[frame]['{0}_cluster_labels'.format(tool)] = labels_array.tolist()
                # Create a list of when the different polygons were created, assuming the order X matches the order of created_at_array.
                # The cteaed_at list originally provided is when all of the classifications per user were added
                created_at_full_array = np.array([created_at[int(user_id)] for user_id in X[:, 1]])
                # Looping through each cluster
                for label in set(labels_array):
                    if label > -1:
                        cdx = labels_array == label
                        kwargs_cluster = {}
                        kwargs_cluster['created_at'] = created_at_full_array[cdx]
                        # number of points in the cluster
                        clusters[frame].setdefault('{0}_clusters_count'.format(tool), []).append(int(cdx.sum()))
                        # The distance matrix is used to find the consensus and is sometimes used in the average
                        distance_matrix = IoU_distance_matrix_of_cluster(cdx, X, data)
                        kwargs_cluster['distance_matrix'] = distance_matrix
                        # Find the consensus of this cluster and add it as float
                        consensus = float(1 - IoU_cluster_mean_distance(distance_matrix))
                        # Now find the "average" of this cluster, using the provided average choice
                        cluster_average = avg(data[cdx], **kwargs_cluster)
                        # Find the x and y values of this polygon
                        if cluster_average.is_empty is True or cluster_average.area == 0.:
                            # If there is no overall intersection, return empty
                            average_polygon = np.array([[], []]).T
                        else:
                            # exterior makes sure you ignore any interior holes
                            average_polygon = np.array(list(cluster_average.exterior.coords))
                        # Add to the dictionary
                        clusters[frame].setdefault('{0}_clusters_x'.format(tool), []).append(average_polygon[:, 0].tolist())
                        clusters[frame].setdefault('{0}_clusters_y'.format(tool), []).append(average_polygon[:, 1].tolist())
                        clusters[frame].setdefault('{0}_consensus'.format(tool), []).append(consensus)

    return clusters
