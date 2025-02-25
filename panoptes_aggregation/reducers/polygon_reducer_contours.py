'''
Polygon/Freehand Tool Reducer Using DBSCAN - Contours
-----------------------------------------------------
This module is an extension of :mod:`panoptes_aggregation.reducers.polygon_reducer`
to provide the contours of intersection. These can be used to estimate the
cluster average. 

Note, this reduction is one cluster per row.
'''
from sklearn.cluster import DBSCAN
import numpy as np
from collections import OrderedDict
from .reducer_wrapper import reducer_wrapper
from .polygon_reducer_utils import IoU_metric_polygon,\
    IoU_distance_matrix_of_cluster, IoU_cluster_mean_distance,\
    cluster_average_intersection_contours
from .polygon_reducer import process_data
from .text_utils import tokenize
import warnings

with warnings.catch_warnings():
    # collatex is a bit old, we can safely ignore this message as the display
    # functions are optional and never used in this code
    warnings.filterwarnings('ignore', category=DeprecationWarning, message='Importing display')
    import collatex as col

DEFAULTS = {
    'min_samples': {'default': 2, 'type': int},
    'eps': {'default': 0.5, 'type': float}
}

# override the built-in tokenize
col.core_classes.WordPunctuationTokenizer.tokenize = tokenize


# Non public function to make sure the list is returned in the correct order
# While this order may have issues if there is more than 9 of either frame,
# task or tool, or if '_cluster_label_for_contours' does not exist, hopefully
# it should at least return the same order each time
def _order_clusters_list(clusters):
    list_of_numbered_clusters = []
    order = np.arange(len(clusters))
    for cluster in clusters:
        frame = [k for k in cluster.keys()][0]
        column_labels = [k for k in cluster.get(frame, {}).keys()]
        task = column_labels[0].split('_')[0]
        tool = column_labels[0].split('_')[1]
        # Find the label for the cluster, default to 0 if unavailable
        cluster_label = cluster[frame].get(task+'_'+tool+'_cluster_label_for_contours', 0)
        number = int('1' + frame[-1] + task[-1] + tool[-1] + str(cluster_label))
        list_of_numbered_clusters.append(number)

    order = np.argsort(list_of_numbered_clusters)
    clusters = [clusters[i] for i in order]
    return clusters


@reducer_wrapper(
    process_data=process_data,
    defaults_data=DEFAULTS,
    user_id=False,
    created_at=True,
    output_kwargs=True
)
def polygon_reducer_contours(data_by_tool, **kwargs_dbscan):
    '''Cluster a polygon or freehand tool using DBSCAN, then find the contours
    of this cluster.

    The contours are defined by the overlap/intersection of the polygons. Each
    contour is the union of the at least the number of intersections of its
    position in the list. E.g. the second contour is the largest polygon/area
    of at least two volunteers agreeing, the third is at least three vilunteers
    etc.

    A custom "IoU" metric type is used.

    Thus takes approximately four times longer than
    :mod:`panoptes_aggregation.reducers.polygon_reducer`

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
    min_samples = max(2, kwargs_dbscan.pop('min_samples', 2))
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
                            kwargs_cluster = {}
                            cluster = OrderedDict()
                            cluster[frame] = OrderedDict()
                            # The distance matrix is used to find the consensus and is sometimes used in the average
                            distance_matrix = IoU_distance_matrix_of_cluster(cdx, X, data)
                            # Find the consensus of this cluster and add its data
                            consensus = 1 - IoU_cluster_mean_distance(distance_matrix)
                            # Now find the "average" of this cluster, using the provided average choice
                            contours = cluster_average_intersection_contours(data[cdx], **kwargs_cluster)
                            # Extract the x and y values of these contours
                            contours_x_values = []
                            contours_y_values = []
                            for contour in contours:
                                xy = np.array(list(contour.boundary.coords))
                                contours_x_values.append(xy[:, 0].tolist())
                                contours_y_values.append(xy[:, 1].tolist())
                            # Store the contours etc
                            cluster[frame]['{0}_cluster_label_for_contours'.format(tool)] = label
                            cluster[frame]['{0}_number_of_contours'.format(tool)] = len(contours)
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

    clusters = _order_clusters_list(clusters)
    return clusters