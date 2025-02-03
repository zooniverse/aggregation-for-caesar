'''
Utilities for `polygon_reducer`
----------------------------------------
This module provides utilities used to reduce the polygon extractions
for :mod:`panoptes_aggregation.reducers.polygon_reducer`.
'''
import numpy as np
import shapely
import datetime
from pandas._libs.tslibs.timestamps import Timestamp as pdtimestamp


def polygon_gap_ratio(polygon_xy):
    polygon_length = np.sum([((polygon_xy[i+1, 0] - polygon_xy[i, 0])**2 +
                              (polygon_xy[i+1, 1] - polygon_xy[i, 1])**2)**0.5
                             for i in range(len(polygon_xy)-1)])
    gap_length = ((polygon_xy[-1, 0] - polygon_xy[0, 0])**2 +
                  (polygon_xy[-1, 1] - polygon_xy[0, 1])**2)**0.5
    return gap_length/polygon_length


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

    Returns
    -------
    last : shapely.geometry.polygon.Polygon
        The last created shaeply polygon in the cluster.
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
        raise ValueError('`created_at` nees to contain either UTC strings, pandas timestamps or datetime objects')
    # sort in time order
    order_logic = np.argsort(created_at_list)
    # Select the last polygon to be created
    last = data[order_logic[-1]]['polygon']
    return last


def cluster_average_intersection(data, **kwargs):
    '''Find the intersection of provided cluster data

    Parameters
    ----------
    data : list
        A list of dicts that take the form
        {`polygon`: shapely.geometry.polygon.Polygon, 'gold_standard', bool}
        There is one element in this list for each classification made.
    kwargs :
        * `created_at` : A list of when the classifcations was made.
        Not used in this average.

    Returns
    -------
    intersection_all : shapely.geometry.polygon.Polygon
        The shapely intersection of the shaeply polygons in the cluster.
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


def cluster_average_union(data, **kwargs):
    '''Find the union of provided cluster data

    Parameters
    ----------
    data : list
        A list of dicts that take the form
        {`polygon`: shapely.geometry.polygon.Polygon, 'gold_standard', bool}
        There is one element in this list for each classification made.
    kwargs :
        * `created_at` : A list when the classifcation was made.
        Not used in this average.

    Returns
    -------
    union_all : shapely.geometry.polygon.Polygon
        The shapely union of the shaeply polygons in the cluster.
    '''
    polygon_list = [data[i]['polygon'] for i in range(len(data))]
    # Just one object, so return it as it is its own average
    if isinstance(polygon_list, shapely.geometry.polygon.Polygon) or len(polygon_list) == 1:
        return polygon_list
    # There must now be two polygons to average
    union_all = polygon_list[0].union(polygon_list[1])
    # If there are any other
    if len(polygon_list) > 2:
        for i in range(2, len(polygon_list)):
            union_all = union_all.union(polygon_list[i])
    if isinstance(union_all, shapely.geometry.collection.GeometryCollection):
        for geo in union_all.geoms:
            if isinstance(geo, shapely.geometry.polygon.Polygon):
                union_all = geo
    return union_all
