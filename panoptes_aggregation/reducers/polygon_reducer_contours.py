'''
Polygon/Freehand Tool Reducer Using DBSCAN - Contours
-----------------------------------------------------
This module is an extension of :mod:`panoptes_aggregation.reducers.polygon_reducer`
to provide the contours of intersection/overlap. These can be used to estimate the
cluster average and its uncertainty.

All polygons are assumed to be closed. Any unclosed polygons will be closed.

Note, this reduction is one cluster per row.
'''
from sklearn.cluster import DBSCAN
import numpy as np
from collections import OrderedDict
from .reducer_wrapper import reducer_wrapper
from .polygon_reducer_utils import IoU_metric_polygon, \
    IoU_distance_matrix_of_cluster, IoU_cluster_mean_distance, \
    cluster_average_intersection_contours, \
    cluster_average_intersection_contours_rasterisation
from .polygon_reducer import process_data

DEFAULTS = {
    'min_samples': {'default': 2, 'type': int},
    'eps': {'default': 0.5, 'type': float}
}


@reducer_wrapper(
    process_data=process_data,
    defaults_data=DEFAULTS,
    user_id=False,
    created_at=True,
    output_kwargs=True
)
def polygon_reducer_contours(data_by_tool, **kwargs_dbscan):
    '''Cluster a polygon/freehand/Bezier tools using DBSCAN, then find the
    contours of this cluster.

    The contours are defined by the overlap/intersection of the polygons in the
    cluster. Each contour is the union of at least the number of
    intersections of its position in the list. E.g. the second contour is the
    largest polygon/area of at least two volunteers agreeing, the third is at
    least three volunteers etc.

    A custom "IoU" metric type is used.

    This reduction will take much longer than
    :mod:`panoptes_aggregation.reducers.polygon_reducer`. As it retruns a list
    rather than a dictionary this may cause issues with any subsequent data
    processing with Caesar.

    The default method for finding the contours is slow but accurate. However,
    the algorithm time per cluster increases approximately exponentially with
    number of polygons in the cluster. Therefore, for cases with clusters of
    many polygons, a more effcient but less accurate rasterisation based
    approach is used. This can be used instead of the default setting the kwarg
    `rasterisation` to `True`.

    Parameters
    ----------
    data_by_tool : dict
        A dictionary returned by :mod:`panoptes_aggregation.reducers.process_data`
    average_type : str
        Either "union", which returns the union of the cluster, "intersection"
        which retruns the intersection of the cluster, "last", which returns
        the last polygon to be annotated in the cluster or "median", which
        returns the polygon with minimal IoU distance to the other polygons
        of the cluster.

    kwargs :
        * `rasterisation`/`rasterization`: String/boolean. If `True` the contours are found using rasterisation, if `False` intersections are used. Defaults to 'auto', which uses rasterisation if more than 9 in the cluster.
        * `num_grid_points`: An integer which defines the number of grid points per axis when rasterisation is `True`. A higher number results in more accuracy but also increases computational time. Defaults to 100.
        * `smoothing`: A string to choose the type of smoothing used for rasterisation (if used). If 'minimal_sides', the number of sides of the contour is minimised. If 'rounded', corners are rounded. If 'no_smoothing', no smoothing is done. Defaults to 'minimal_sides'.
        * `See DBSCAN <http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html>`_

    Returns
    -------
    reduction : list
        A list of dictionaries. Each dictionary has following keys for each frame, task and tool:

        * `tool*_cluster_labels` : A list of cluster labels for polygons provided. This is for all of the clusters for this frame and tool
        * `tool*_cluster_label_for_contours` : The index of the cluster whose contours are listed, corresponding to the labels in `tool*_cluster_labels`
        * `tool*_number_of_contours` : The number of contours of the cluster
        * `tool*_contours_x` : A list of the x values of each contour
        * `tool*_contours_y` : A list of the y values of each contour
        * `tool*_consensus` : A list of the the overall consensus of each cluster. A value of 1 is perfect agreement, a value of 0 is complete disagreement. This is found by subtracting`IoU_cluster_mean_distance` from 1
    '''
    min_samples = max(1, kwargs_dbscan.pop('min_samples', 2))
    rasterisation = kwargs_dbscan.pop('rasterisation', 'auto')
    smoothing = kwargs_dbscan.pop('rasterisation', 'minimal_sides')
    # In case American English is used
    try:
        rasterisation = kwargs_dbscan.pop('rasterization')
    except KeyError:
        pass
    num_grid_points = kwargs_dbscan.pop('num_grid_points', 100)
    # Remove created_at from kwargs, if it is provided
    _ = kwargs_dbscan.pop('created_at', [])
    clusters = []
    for frame, frame_data in data_by_tool.items():
        for tool, value in frame_data.items():
            X = np.array(value['X'])
            data = np.array(value['data'])
            num_polygons = len(data)

            if num_polygons >= min_samples:  # If clustering can be done
                db = DBSCAN(
                    metric=IoU_metric_polygon,
                    metric_params={'data_in': data},
                    min_samples=min_samples,
                    **kwargs_dbscan
                )
                db.fit(X)
                labels_array = db.labels_
                unique_labels = set(labels_array)
                # If there are no clusters, again return just the cluster labels
                if unique_labels == {-1}:
                    cluster = OrderedDict()
                    cluster[frame] = OrderedDict()
                    cluster[frame]['{0}_cluster_labels'.format(tool)] = [-1] * num_polygons
                    clusters.append(cluster)
                else:  # there are clusters
                    # Looping through each cluster
                    for label in unique_labels:
                        if label > -1:
                            cdx = labels_array == label
                            cluster = OrderedDict()
                            cluster[frame] = OrderedDict()
                            # The distance matrix is used to find the consensus and is sometimes used in the average
                            distance_matrix = IoU_distance_matrix_of_cluster(cdx, X, data)
                            # Find the consensus of this cluster and add it as float
                            consensus = float(1 - IoU_cluster_mean_distance(distance_matrix))
                            # Now find the "average" of this cluster, using the provided average choice
                            # Below is logic to choose rasterisation or the default approach
                            cluster_size = np.sum(cdx)
                            use_rastorisation = rasterisation
                            if use_rastorisation == 'auto':
                                if cluster_size > 9:
                                    use_rastorisation = True
                                else:
                                    use_rastorisation = False
                            if use_rastorisation is True:
                                contours = cluster_average_intersection_contours_rasterisation(data[cdx],
                                                                                               num_grid_points=num_grid_points,
                                                                                               smoothing=smoothing)
                            else:
                                contours = cluster_average_intersection_contours(data[cdx])

                            # Extract the x and y values of these contours
                            contours_x_values = []
                            contours_y_values = []
                            for contour in contours:
                                # exterior makes sure you ignore any interior holes
                                xy = np.array(list(contour.exterior.coords))
                                contours_x_values.append(xy[:, 0].tolist())
                                contours_y_values.append(xy[:, 1].tolist())
                            # Store the contours etc
                            cluster[frame]['{0}_cluster_label_for_contours'.format(tool)] = int(label)
                            cluster[frame]['{0}_number_of_contours'.format(tool)] = int(len(contours))
                            cluster[frame]['{0}_contours_x'.format(tool)] = contours_x_values
                            cluster[frame]['{0}_contours_y'.format(tool)] = contours_y_values
                            cluster[frame]['{0}_consensus'.format(tool)] = consensus
                            cluster[frame]['{0}_cluster_labels'.format(tool)] = labels_array.tolist()
                            # Add it to the list of clusters
                            clusters.append(cluster)
            else:
                cluster = OrderedDict()
                cluster[frame] = OrderedDict()
                cluster[frame]['{0}_cluster_labels'.format(tool)] = [-1] * num_polygons
                clusters.append(cluster)
    return clusters
