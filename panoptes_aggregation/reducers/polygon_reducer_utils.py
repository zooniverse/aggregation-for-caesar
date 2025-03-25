'''
Utilities for `polygon_reducer`
-------------------------------
This module provides utilities used to reduce the polygon extractions
for :mod:`panoptes_aggregation.reducers.polygon_reducer`.
'''
import numpy as np
import shapely
import datetime
from scipy.linalg import issymmetric
from pandas._libs.tslibs.timestamps import Timestamp as pdtimestamp
from contourpy import contour_generator
from shapelysmooth import taubin_smooth


def _polygons_unify(polygons):
    '''Internal function to unify the polygons in a cluster, even for cases
    with disconnected clusters or if individual polygons are not connected by
    are connected by another polygon.'''
    polygons = np.array(polygons)
    union_all = shapely.unary_union(polygons)
    # If multipolygon data type, find the largest polygon
    if isinstance(union_all, shapely.geometry.collection.GeometryCollection)\
            or isinstance(union_all, shapely.geometry.multipolygon.MultiPolygon):
        areas = []
        for geometry in union_all.geoms:
            if isinstance(geometry, shapely.geometry.polygon.Polygon):
                areas.append(geometry.area)
            else:
                areas.append(0.)
        # Find the polygon with the largest area
        union = union_all.geoms[np.argmax(areas)]
    else:  # Else if only one polygon, this is the union by itself
        union = union_all
    # Now close any holes
    if len(union.interiors) > 0:
        for hole in union.interiors:
            hole = shapely.Polygon(hole)
            union = union.union(hole)
    # Simplfy
    union = union.buffer(0)
    return union


# This needs a list of shapely objects to work!
def IoU_metric_polygon(a, b, data_in=[]):
    '''Find the Intersection of Union distance between two polygons. This is
    based on the `Jaccard metric <https://en.wikipedia.org/wiki/Jaccard_index>`_

    To use this metric within the clustering code without having to
    precompute the full distance matrix `a` and `b` are index mappings to
    the data contained in `data_in`.  `a` and `b` also contain the user
    information that is used to help prevent self-clustering. The polygons
    used to calculate the IoU distance are contained in `data_in`, along with
    the timestamp of creation.

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

    return 1 - intersection / union


def IoU_distance_matrix_of_cluster(cdx, X, data):
    '''Find distance matrix using `IoU_metric_polygon` for a cluster.

    The `cdx` argument is used to define the cluster out of the full `X` and
    `data` data sets, which may also contain other polygons not in the cluster.

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
    # If a cluster of 1 is provided, this will correctly default to a distance of 0
    distances_matrix = np.zeros((num_in_cluster, num_in_cluster))
    for i in range(num_in_cluster):
        a = cluster_X[i]
        for j in range(i + 1, num_in_cluster):
            b = cluster_X[j]
            distance = IoU_metric_polygon(a, b, data_in=data)
            distances_matrix[i, j] = distance
            distances_matrix[j, i] = distance
    return distances_matrix


def IoU_cluster_mean_distance(distances_matrix):
    '''The mean `IoU_metric_polygon` distance between the polygons of the
    cluster.

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
        raise Exception('`distances_matrix` must be a symmetric-square array')
    # Check the diagonals are all 0, as the distance between an object and its self is always zero
    if np.sum(np.diagonal(distances_matrix)) != 0:
        raise ValueError('`distances_matrix` must have zero diagonal elements, as distance between the object and itself is zero')

    if np.shape(distances_matrix) == (1, 1):  # If cluster of one, include 0 distance to itself
        unique_distances = np.array([distances_matrix[0, 0]])
    else:
        # Find the unigue distances from the off diagonal components
        unique_distances = np.array([distances_matrix[i, j] for i in range(len(distances_matrix)) for j in range(i + 1, len(distances_matrix))])
    # Set any infinities to 1, otherwise the mean cannot be calculated
    unique_distances[unique_distances == np.inf] = 1
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


    Returns
    -------
    last : shapely.geometry.polygon.Polygon
        The last created shapely polygon in the cluster.
    '''
    created_at = np.array(kwargs.pop('created_at'))

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
        raise Exception('`created_at` needs to contain either UTC strings, pandas timestamps or datetime objects')
    # sort in time order
    order_logic = np.argmax(created_at_list)
    # Select the last polygon to be created
    last = data[order_logic]['polygon']
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
    distance_matrix[distance_matrix == np.inf] = 1
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

    Returns
    -------
    intersection_all : shapely.geometry.polygon.Polygon
        The `shapely` intersection of the shapely polygons in the cluster.
    '''
    polygon_list = [data[i]['polygon'] for i in range(len(data))]
    # Just one object, so return it as it is its own average
    if len(polygon_list) == 1:
        return polygon_list[0]
    # There must now be two polygons to average
    intersection_all = polygon_list[0].intersection(polygon_list[1])
    # If there are any other
    if len(polygon_list) > 2:
        for i in range(2, len(polygon_list)):
            intersection_all = intersection_all.intersection(polygon_list[i])

    return intersection_all


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
    Returns
    -------
    union_all : shapely.geometry.polygon.Polygon
        The shapely union of the shapely polygons in the cluster.
    '''
    polygon_list = [data[i]['polygon'] for i in range(len(data))]
    # Just one object, so return it as it is its own average
    if len(polygon_list) == 1:
        return polygon_list[0]
    # There must now be two polygons to average
    union_all = _polygons_unify(polygon_list)
    return union_all


def cluster_average_intersection_contours(data, **kwargs):
    '''Find contours of intersection as a list. Each item of the list will
    be the largest contour of `i` intersections, with the next item being the
    contour `i+1` intersection etc. The intersection is where the polygons
    overlap. This is useful for plotting the uncertainty in the cluster.

    The algorithm used is as follows. First find the largest simply-connected
    union polygon for the cluster and add it to the list
    `intersection_contours`. Next, every intersection of two polygons is found,
    and made into new `shapely` polygons. This makes a list of 'level-2'
    polygons. These polygons may overlap. Then, find the largest
    simply-connected union polygon of the level-2 polygons. This is the
    polygon of at least 2 intersections
    (i.e. area where at least 2 volunteers agree). Add it to list
    `intersection_contours`.

    If there is more than one level-2 polygons, which intersect, then the
    intersection of the level-2 polygons is found as a list. These are the
    level-3 polygons, as each polygon is made from at least three
    intersections. Then find the largest
    simply-connected union polygon of the level-3 polygons. This is the
    polygon of at least 3 intersections
    (i.e. area where at least 3 volunteers agree). Add it to list
    `intersection_contours`.

    Continue this process until either 10 iterations have been done, or only
    one unique intersection polygon remains.

    Parameters
    ----------
    data : list
        A list of dicts that take the form
        {`polygon`: shapely.geometry.polygon.Polygon, 'gold_standard', bool}
        There is one element in this list for each classification made.
    kwargs :
        * `created_at` : A list when the classifcation was made. Not used in this average.
        * `distance_matrix` : A symmetric-square array, with the off-diagonal elements containing the `IoU_metric_polygon` distance between the cluster members. The diagonal elements are all zero. This is found using `IoU_distance_matrix_of_cluster`. Not used in this average.

    Returns
    -------
    intersection_contours : list
        List of shapely objects. Each shape at position `i` in the list is the
        largest simply-connected contour of at least `i` intersections.
    '''
    # Want the list to just be simple polygons
    polygons = [data[i]['polygon'] for i in range(len(data))]

    def polygon_list_simplify(polygons):
        # First find all of the indivual polygons
        individual_polygons = []
        for polygon in polygons:
            if isinstance(polygon, shapely.geometry.polygon.Polygon):
                individual_polygons.append(polygon)
            elif isinstance(polygon, shapely.geometry.collection.GeometryCollection)\
                    or isinstance(polygon, shapely.geometry.multipolygon.MultiPolygon):
                for p in polygon.geoms:
                    if isinstance(p, shapely.geometry.polygon.Polygon):
                        individual_polygons.append(p)
        # Make sure all polygons are simple
        individual_polygons = shapely.buffer(individual_polygons, 0)
        return individual_polygons

    # Need each item in the polygon list to be a polygon, not a list of polygons
    # This list of polygons will be updated to just be the intersections of polygons
    polygons = polygon_list_simplify(polygons)
    # Need to keep track of the polygons which are in each intersection
    polygon_indices = [[i] for i in range(len(polygons))]

    def polygon_intersection_list(polygons, polygon_indices):
        # List of all of the intersections for these polygons
        tree = shapely.STRtree(polygons)
        intersection_array = tree.query(polygons, predicate='intersects').T
        num_polygons = len(polygons)
        polygon_connections = []
        polygon_connections_indices = []
        for i in range(num_polygons):
            intersects = intersection_array[intersection_array[:, 0] == i][:, 1]
            intersects = intersects[intersects != i]
            to_add_intersections = []
            for j in intersects:
                # The indices of the polygons in this intersection
                polygon_connection_index = list(set(polygon_indices[i] + polygon_indices[j]))
                # Want it in order so comparison can be made
                polygon_connection_index.sort()
                # If this connection has not already been made, add it to the list of 'to be added' and
                # make sure it won't be made again
                if polygon_connection_index not in polygon_connections_indices:
                    to_add_intersections.append(j)
                    polygon_connections_indices.append(polygon_connection_index)
            # Now make the connects and add them
            if len(to_add_intersections) > 0:
                polygons_to_intersect = [polygons[k] for k in to_add_intersections]
                # Find the intersections effcienctly
                polygon_intersection_list = list(shapely.intersection(polygons[i], polygons_to_intersect))
                polygon_connections += polygon_intersection_list

        return polygon_connections, polygon_connections_indices

    num_agreement = 1
    safety = 10
    intersection_contours = []
    # Start with the level 1 contours
    polygons_union = _polygons_unify(polygons)
    intersection_contours.append(polygons_union)
    while num_agreement < safety:
        # If there is only one polygon left, break
        if len(polygons) == 1:
            break
        else:
            # Find the intersection of the provided polygons, and the contributing indices
            polygons, polygon_indices = polygon_intersection_list(polygons, polygon_indices)
            polygons = polygon_list_simplify(polygons)
        # If there are intersection polygons, find their union. If not break as maximum level of intersection found
        # Now find the union of these contours and add it to the list of contours
        if len(polygons) > 0:
            polygons_union = _polygons_unify(polygons)
            intersection_contours.append(polygons_union)
            # Each time the intersection polygons are found, the number of agreement increases by 1
            num_agreement += 1
        else:
            break

    return intersection_contours


def cluster_average_intersection_contours_rasterisation(data, **kwargs):
    '''Find contours of intersection as a list. Each item of the list will
    be the largest contour of `i` intersections, with the next item being the
    contour `i+1` intersection etc. The intersection is where the polygons
    overlap. This is useful for plotting the uncertainty in the cluster.

    This approach uses rasterisation to find the contours. A square grid, with
    the number of grid points along each of the two axis given by
    `num_grid_points`, is placed over the cluster. Then the number of polygon
    intersections in each grid square are counted. Contours are then made from
    this 2D surface of intersection counts.

    This function has the advantage of being more efficient than
    :mod:`cluster_average_intersection_contours` when the number of polygons in
    the cluster is large (approximately when greater than 8). Equally if
    `num_grid_points` is small, say 10, then rasterisation is faster in most
    cases but gives poorer quality contours with increased risk of grid-spacing
    based artifacts.

    The resulting contours are smoothed by default.

    Parameters
    ----------
    data : list
        A list of dicts that take the form
        {`polygon`: shapely.geometry.polygon.Polygon, 'gold_standard', bool}
        There is one element in this list for each classification made.
    kwargs :
        * `num_grid_points`: The number of grid points per axis. A larger number means greater resolution, but takes longer. Default is 100.
        * `smoothing`: A string to choose the type of smoothing used. If 'minimal_sides', the number of sides of the contour is minimised. If 'rounded', corners are rounded. If 'no_smoothing', no smoothing is done. Defaults to 'minimal_sides'.
        * `created_at` : A list when the classifcation was made. Not used in this average.
        * `distance_matrix` : A symmetric-square array, with the off-diagonal elements containing the `IoU_metric_polygon` distance between the cluster members. The diagonal elements are all zero. This is found using `IoU_distance_matrix_of_cluster`. Not used in this average.

    Returns
    -------
    intersection_contours : list
        List of shapely objects. Each shape at position `i` in the list is the
        largest simply-connected contour of at least `i` intersections.
    '''
    # Want the list to just be simple polygons
    polygons = [data[i]['polygon'] for i in range(len(data))]
    num_grid_points = kwargs.pop('num_grid_points', 100)
    smoothing = kwargs.pop('smoothing', 'minimal_sides')

    polygons_bounds = shapely.bounds(polygons)
    x_min = np.min(polygons_bounds[:, 0])
    x_max = np.max(polygons_bounds[:, 2])
    y_min = np.min(polygons_bounds[:, 1])
    y_max = np.max(polygons_bounds[:, 3])

    x_values = np.linspace(x_min, x_max, num_grid_points)
    y_values = np.linspace(y_min, y_max, num_grid_points)
    x_grid, y_grid = np.meshgrid(x_values, y_values)
    z_grid = np.zeros(np.shape(x_grid))

    x_grid_flat, y_grid_flat = x_grid.flatten(), y_grid.flatten()
    for polygon in polygons:
        # Find flattened grid of bools for if point inside polygon
        count_grid = shapely.contains_xy(polygon, x=x_grid_flat, y=y_grid_flat)
        # Convert to 0 or 1
        count_grid = count_grid.astype('int')
        # make grid again
        count_grid = np.reshape(count_grid, np.shape(z_grid))
        z_grid += count_grid

    # Find the contour lines
    cont_gen = contour_generator(x=x_grid, y=y_grid, z=z_grid)
    multi_lines = cont_gen.multi_lines(np.arange(0, np.max(z_grid), 1, dtype='int'))
    # Find only the largest contours for each level of agreement by area
    intersection_contours = []
    for lines in multi_lines:
        possible_contour = []
        for xy in lines:
            contour = shapely.Polygon(xy)
            possible_contour.append(contour)
        areas = shapely.area(possible_contour)
        # Find contour with largest area
        contour = possible_contour[np.argmax(areas)]
        intersection_contours.append(contour)
    # Remove any artifacts from grid size, if specified
    if smoothing == 'no_smoothing':
        pass
    elif smoothing == 'rounded':
        for i in range(len(intersection_contours)):
            intersection_contours[i] = taubin_smooth(intersection_contours[i])
    else:
        tolerance = max(0.5 / num_grid_points, 0.01)
        intersection_contours = shapely.simplify(intersection_contours, tolerance)
    return intersection_contours
