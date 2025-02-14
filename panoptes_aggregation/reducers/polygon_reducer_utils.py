'''
Utilities for `polygon_reducer`
----------------------------------------
This module provides utilities used to reduce the polygon extractions
for :mod:`panoptes_aggregation.reducers.polygon_reducer`.
'''
import numpy as np
import shapely
import datetime
from scipy.linalg import issymmetric
from pandas._libs.tslibs.timestamps import Timestamp as pdtimestamp

# Might use later
def polygon_gap_ratio(polygon_xy):
    polygon_length = np.sum([((polygon_xy[i+1, 0] - polygon_xy[i, 0])**2 +
                              (polygon_xy[i+1, 1] - polygon_xy[i, 1])**2)**0.5
                             for i in range(len(polygon_xy)-1)])
    gap_length = ((polygon_xy[-1, 0] - polygon_xy[0, 0])**2 +
                  (polygon_xy[-1, 1] - polygon_xy[0, 1])**2)**0.5
    return gap_length/polygon_length


def _polygons_unify(polygons):
    # Internal function to unify the polygons in a cluster, even for cases with
    # disconnected clusters or if individual polygons are not connected by are
    # connected by another polygon.

    all_unified = False
    i = 0
    safety = 0
    while all_unified is False:
        if i > len(polygons)-2:  # Once first interation is done
            # Find all of the possible intersections
            intersections = []
            for j in range(len(polygons)):
                for k in range(j+1, len(polygons)):
                    intersections.append(polygons[j].intersects(polygons[k]))
            if any(intersections) is False:
                all_unified = True
                break
            else:  # Restart the unification
                i = 0

        indices_included = []
        for j in range(i+1, len(polygons)):
            if polygons[i].intersects(polygons[j]):
                polygons[i] = polygons[i].union(polygons[j])
                # If there are any holes, close them
                if len(polygons[i].interiors) > 0:
                    for hole in polygons[i].interiors:
                        hole = shapely.Polygon(hole)
                        polygons[i] = polygons[i].union(hole)
                indices_included.append(j)
        # Remove polygons that have been unified into the others
        for j in sorted(indices_included, reverse=True):
            del polygons[j]
        # If only one polygon, we are finished
        if len(polygons) == 1:
            all_unified = True
            break
        i += 1
        safety += 1
        if safety > 10:
            all_unified = True
            break
    areas = [polygons[i].area for i in range(len(polygons))]
    largest_polygon_index = np.argmax(areas)
    return polygons[largest_polygon_index]


# This needs a list of shapely objects to work!
def IoU_metric_polygon(a, b, data_in=[]):
    '''Find the Intersection of Union distance between two polygons. This is
    based on the `Jaccard metric <https://en.wikipedia.org/wiki/Jaccard_index>`_

    To use this metric within the clustering code without having to
    precompute the full distance matrix `a` and `b` are index mappings to
    the data contained in `data_in`.  `a` and `b` also contain the user
    information that is used to help prevent self-clustering. The polygons are
    contained in `data_in`, along with the timestamp of creation.

    Parameters
    ----------
    a : list
        A two element list containing [index mapping to data, index mapping to user]
    b : list
        A two element list containing [index mapping to data, index mapping to user]
        A list of the parameters for shape 2 (as defined by PFE)
    data_in : list
        A list of dicts that take the form
        {`polygon`: shapely.geometry.polygon.Polygon, 'time': float, 'gold_standard', bool}
        There is one element in this list for each classification made. The
        time should be a Unix timestamp float.

    Returns
    -------
    distance : float
        The IoU distance between the two polygons. 0 means the polygons are the
        same, 1 means the polygons don't overlap, values in the middle mean
        partial overlap.
    '''
    if a[0] == b[0]:
        # The same data point, the distance is zero
        return 0
    if a[1] == b[1]:
        # The same users, distance is inf
        return np.inf

    # Now need to find the actual data
    geo1 = data_in[int(a[0])]['polygon']
    geo2 = data_in[int(b[0])]['polygon']

    # The two shapes need to intersect and be simple for the intersection area
    # to be found
    if geo1.intersects(geo2) and (shapely.is_simple(geo1) and shapely.is_simple(geo2)):
        intersection = geo1.intersection(geo2).area
    else:  # No intersection, so distance is 1
        return 1

    union = geo1.union(geo2).area

    if union == 0:
        # catch divide by zero (i.e. cases when neither shape has an area)
        return np.inf

    return 1 - intersection / union


def IoU_distance_matrix_of_cluster(cdx, X, data):
    '''Find distance matrix using `IoU_metric_polygon` for a cluster.

    The `cdx` argument is used to define the cluster.

    Parameters
    ----------
    cdx : numpy.ndarray
        A 1D array of booleans, corresponding to the polygons in `X` and `data`
        which are in the cluster. `True` if in the cluster, `False` otherwise.
    X : numpy.ndarray
        A 2D array with each row mapping to the data held in `data`. The first
        column contains row indices and the second column is an index assigned
        to each user.
    data_cluster : list
        A list of dicts that take the form
        {`polygon`: shapely.geometry.polygon.Polygon, 'time': float, 'gold_standard', bool}
        There is one element in this list for each member of the cluster.

    Returns
    -------
    distances_matrix : numpy.ndarray
        A symmetric-square array, with the off-diagonal elements containing the
        IoU distance between the cluster members. The diagonal elements are all
        zero.
    '''
    cluster_X = X[cdx]
    num_in_cluster = np.shape(cluster_X)[0]
    distances_matrix = np.zeros((num_in_cluster, num_in_cluster))
    for i in range(num_in_cluster):
        a = cluster_X[i]
        for j in range(i+1, num_in_cluster):
            b = cluster_X[j]
            distance = IoU_metric_polygon(a, b, data_in=data)
            distances_matrix[i, j] = distance
            distances_matrix[j, i] = distance
    return distances_matrix


def IoU_cluster_mean_distance(distances_matrix):
    '''The mean `IoU_metric_polygon` distance between the polygons of the
    cluster 

    Parameters
    ----------
    distances_matrix : numpy.ndarray
        A symmetric-square array, with the off-diagonal elements containing the
        `IoU_metric_polygon` distance between the cluster members. The diagonal
        elements are all zero. This is found using `IoU_distance_matrix_of_cluster`.

    Returns
    -------
    distances_mean : float
        The mean of the `IoU_metric_polygon` defined distance between the
        polygons of the cluster.
    '''
    # first check if it is symmetric
    if not issymmetric(distances_matrix):
        raise ValueError('`distances_matrix` must be a symmetric-square array')
    # Check the diagonals are all 0, as the distance between an object and its self is always zero
    if np.sum(np.diagonal(distances_matrix)) != 0:
        raise ValueError('`distances_matrix` must have zero diagonal elements, as distance between the object and itself is zero')

    # Find the unigue distances from the off diagonal components
    unique_distances = np.array([distances_matrix[i,j] for i in range(len(distances_matrix)) for j in range(i+1, len(distances_matrix))])
    # Set any infinities to 1, otherwise the mean cannot be calculated
    unique_distances[unique_distances==np.inf] = 1
    # As IoU distances are akways positive, this mean will always be positive
    distances_mean = np.mean(unique_distances)
    return distances_mean


def cluster_average_last(data, **kwargs):
    '''Find the last created polygon of provided cluster data

    Parameters
    ----------
    data : list
        A list of dicts that take the form
        {`polygon`: shapely.geometry.polygon.Polygon, 'gold_standard', bool}
        There is one element in this list for each classification made. The
        time should be a Unix timestamp float.
    kwargs :
        * `created_at` : A list of when the classifcations was made.
        * `distance_matrix` : A symmetric-square array, with the off-diagonal elements containing the `IoU_metric_polygon` distance between the cluster members. The diagonal elements are all zero. This is found using `IoU_distance_matrix_of_cluster`. Not used in this average.
        * `n_polygons` : the minimum number of intersections. Not used in this average.


    Returns
    -------
    last : shapely.geometry.polygon.Polygon
        The last created shapely polygon in the cluster.
    '''
    created_at = np.array(kwargs.pop('created_at'))
    # Make sure `cteared_at` is a list or array
    if not (isinstance(created_at, list) or isinstance(created_at, np.ndarray)):
        raise ValueError('`created_at` must be a list or array')

    # Change to datatime format
    created_at_list = []
    if isinstance(created_at[0], str):  # If in original format
        for time in created_at:
            created_at_list.append(datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S UTC"))
    elif isinstance(created_at[0], pdtimestamp):
        for time in created_at:
            created_at_list.append(time.to_pydatetime())
    elif isinstance(created_at[0], datetime.datetime):  # If already correct
        created_at_list = created_at
    else:
        raise ValueError('`created_at` needs to contain either UTC strings, pandas timestamps or datetime objects')
    # sort in time order
    order_logic = np.argsort(created_at_list)
    # Select the last polygon to be created
    last = data[order_logic[-1]]['polygon']
    return last


def cluster_average_median(data, **kwargs):
    '''Find the 'median' of provided cluster data,
    i.e. the polygon of the cluster with the minimum total
    distance to the other polygons.

    Parameters
    ----------
    data : list
        A list of dicts that take the form
        {`polygon`: shapely.geometry.polygon.Polygon, 'gold_standard', bool}
        There is one element in this list for each classification made.
    kwargs :
        * `created_at` : A list when the classifcation was made. Not used in this average.
        * `distance_matrix` : A symmetric-square array, with the off-diagonal elements containing the `IoU_metric_polygon` distance between the cluster members. The diagonal elements are all zero. This is found using `IoU_distance_matrix_of_cluster`.
        * `n_polygons` : the minimum number of intersections. Not used in this average.

    Returns
    -------
    median : shapely.geometry.polygon.Polygon
        The 'median' polygon in the cluster.
    '''
    distance_matrix = kwargs.pop('distance_matrix')
    # first check if it is symmetric
    if not issymmetric(distance_matrix):
        raise ValueError('`distances_matrix` must be a symmetric-square array')
    # Check the diagonals are all 0, as the distance between an object and its self is always zero
    if np.sum(np.diagonal(distance_matrix)) != 0:
        raise ValueError('`distances_matrix` must have zero diagonal elements, as distance between the object and itself is zero')
    # Set infinities to 1 to avoid user self clustering
    distance_matrix[distance_matrix==np.inf] = 1
    # Find the total mutual distance to each polygon
    sums_of_distances = np.sum(distance_matrix, axis=0)
    median_polygon_index = np.argmin(sums_of_distances)
    median_polygon = data[median_polygon_index]['polygon']
    return median_polygon


def cluster_average_intersection(data, **kwargs):
    '''Find the intersection of provided cluster data

    Parameters
    ----------
    data : list
        A list of dicts that take the form
        {`polygon`: shapely.geometry.polygon.Polygon, 'gold_standard', bool}
        There is one element in this list for each classification made.
    kwargs :
        * `created_at` : A list of when the classifcations was made. Not used in this average.
        * `distance_matrix` : A symmetric-square array, with the off-diagonal elements containing the `IoU_metric_polygon` distance between the cluster members. The diagonal elements are all zero. This is found using `IoU_distance_matrix_of_cluster`. Not used in this average.
        * `n_polygons` : the minimum number of intersections. Not used in this average.

    Returns
    -------
    intersection_all : shapely.geometry.polygon.Polygon
        The `shapely` intersection of the shapely polygons in the cluster.
    '''
    polygon_list = [data[i]['polygon'] for i in range(len(data))]
    # Just one object, so return it as it is its own average
    if isinstance(polygon_list, shapely.geometry.polygon.Polygon) or len(polygon_list) == 1:
        return polygon_list
    # There must now be tw polygons to average
    intersection_all = polygon_list[0].intersection(polygon_list[1])
    # If there are any other
    if len(polygon_list) > 2:
        for i in range(2, len(polygon_list)):
            intersection_all = intersection_all.intersection(polygon_list[i])
    if isinstance(intersection_all, shapely.geometry.collection.GeometryCollection):
        for geo in intersection_all.geoms:
            if isinstance(geo, shapely.geometry.polygon.Polygon):
                intersection_all = geo
    return intersection_all


def cluster_average_intersection_n_polygons(data, **kwargs):
    '''Find the largest area, i.e. a polygon of intersections,
    where at least n polygons intersect.

    The algorithm used is as follows. First every intersection of two polygons
    is found, and made into new `shapely` polygons. These polygons may overlap.
    If 'n_polygons' = 2, then these regions are unified into a single polygon,
    `intersection_n_polygons`, and returned. This is the polygon of at least 2
    intersections (i.e. area where at least 2 volunteers agree).

    If 'n_polygons' > 2, then the intersections polygons have their
    intersection found, producing a new list of polygons. Each of these
    polygons will be, by construction, the intersection of at least 3 of the
    original polygons.

    If 'n_polygons' = 3, these polygons are then unified as for
    'n_polygons' = 2 and returned. If however 'n_polygons' > 3, the process is
    simply repeated until each of the intersection polygons is constructed
    from at least 'n_polygons' of the original polygons.

    If a polygon of at least 'n_polygons' intersections cannot be found, then
    an empty list is returned. Such a case can occur when the cluster is
    spread out or if the number of samples in the cluster is less than.

    Parameters
    ----------
    data : list
        A list of dicts that take the form
        {`polygon`: shapely.geometry.polygon.Polygon, 'gold_standard', bool}
        There is one element in this list for each classification made.
    kwargs :
        * `created_at` : A list when the classifcation was made. Not used in this average.
        * `distance_matrix` : A symmetric-square array, with the off-diagonal elements containing the `IoU_metric_polygon` distance between the cluster members. The diagonal elements are all zero. This is found using `IoU_distance_matrix_of_cluster`. Not used in this average.
        * `n_polygons` : the minimum number of intersections. Should be an integer.

    Returns
    -------
    intersection_n_polygons : shapely.geometry.polygon.Polygon or []
        The largest `shapely` intersection of at least n polygons. Is an empty
        list if no such area can be found
    '''
    n_polygons = int(kwargs.pop('n_polygons', 2))
    polygons = [data[i]['polygon'] for i in range(len(data))]

    def polygon_list_simplify(polygons):
        individual_polygons = []
        for polygon in polygons:
            if isinstance(polygon, shapely.geometry.polygon.Polygon):
                individual_polygons.append(polygon)
            elif isinstance(polygon, shapely.geometry.collection.GeometryCollection)\
                                or isinstance(polygon, shapely.geometry.multipolygon.MultiPolygon):
                for p in polygon.geoms:
                    individual_polygons.append(p)
            else:
                raise ValueError('Provided data could not be made into shapely polygon data type')
        return individual_polygons

    # Need each item in the polygon list to be a polygon, not a list of polygons
    # This list of polygons will be updated to just be the intersections of polygons
    polygons = polygon_list_simplify(polygons)
    # Need to keep track of the polygons which are in each intersection
    polygon_indices = [[i] for i in range(len(polygons))]

    # This is a function which takes a list of polygons, and returns a list
    # of the unique intersections of these polygons, along with the indices
    # of the cluster polygons in each intersection
    def polygon_intersection_list(polygons, polygon_indices):
        num_polygons = len(polygons)
        polygon_connections = []
        polygon_connections_indices = []
        for i in range(num_polygons):
            for j in range(i+1, num_polygons):
                if (polygons[i].intersects(polygons[j])==True):
                    # The indices of the polygons in this intersection
                    polygon_connection_index = list(set(polygon_indices[i] + polygon_indices[j]))
                    # Want it in order so comparison can be made
                    polygon_connection_index.sort()
                    if polygon_connection_index not in polygon_connections_indices:
                        polygon_connections.append(polygons[i].intersection(polygons[j]))
                        polygon_connections_indices.append(polygon_connection_index)
        return polygon_connections, polygon_connections_indices
    num_agreement = 1
    while num_agreement<n_polygons:
        # If there is only one polygon left, but more intersections are required, check if this already has enough
        # intersections. If not, return nothing
        if len(polygons)==1:
            if len(polygon_indices[0]) >= n_polygons:
                break
            else:
                return []
        else:
            # Find the intersection of the provided polygons, and the contributing indices
            polygons, polygon_indices = polygon_intersection_list(polygons, polygon_indices)
            # Each time the intersection polygons are found, the number of agreement increases by 1
            num_agreement += 1

    # Now we have the individual polygons of at least n_polygons overlap/agreement/intersection
    # we can try to unify (if they each intersect) these regions into (hopefully one) larger polygon. If there are several polygons,
    # the largest is chosen.
    intersection_n_polygons = _polygons_unify(polygons)
    return intersection_n_polygons


def cluster_average_union(data, **kwargs):
    '''Find the union of provided cluster data

    Parameters
    ----------
    data : list
        A list of dicts that take the form
        {`polygon`: shapely.geometry.polygon.Polygon, 'gold_standard', bool}
        There is one element in this list for each classification made.
    kwargs :
        * `created_at` : A list when the classifcation was made. Not used in this average.
        * `distance_matrix` : A symmetric-square array, with the off-diagonal elements containing the `IoU_metric_polygon` distance between the cluster members. The diagonal elements are all zero. This is found using `IoU_distance_matrix_of_cluster`. Not used in this average.
        * `n_polygons` : the minimum number of intersections. Not used in this average.

    Returns
    -------
    union_all : shapely.geometry.polygon.Polygon
        The shapely union of the shapely polygons in the cluster.
    '''
    polygon_list = [data[i]['polygon'] for i in range(len(data))]
    # Just one object, so return it as it is its own average
    if isinstance(polygon_list, shapely.geometry.polygon.Polygon) or len(polygon_list) == 1:
        return polygon_list
    # There must now be two polygons to average
    union_all =  _polygons_unify(polygon_list)
    return union_all
