'''
Intersection of Union Metric
----------------------------
This module provides a custom intersection of union (IoU) metric
to be used with `panoptes_aggregation.reducers.shape_reducer_dbscan`.
'''
import shapely.geometry
import shapely.affinity
import scipy.optimize
import numpy
from functools import lru_cache
from packaging import version


VALID_IOU_SHAPES = [
    'rectangle',
    'rotateRectangle',
    'temporalRotateRectangle',
    'column',
    'graph2dRangeX',
    'circle',
    'ellipse',
    'triangle'
]


def tupleize(func):
    def wrapper(params, shape, **kwargs):
        return func(tuple(params), shape, **kwargs)
    return wrapper


@tupleize
@lru_cache(maxsize=100)
def panoptes_to_geometry(params, shape, classifier_version=version.parse('1.0')):
    '''Convert shapes created with the Panoptes Front End (PFE) to shapely
    geometry objects.

    Parameters
    ----------
    params : tuple
        A tuple of the parameters for the shape (as defined by PFE)
    shape : string
        The name of the shape these parameters belong to.  Supported shapes are:

        * rectangle
        * rotateRectangle
        * circle
        * ellipse
        * triangle

    classifier_version : packaging.version
        The version of classifier used to make the classifications, either `1.0` for PFE or `2.0`
        for FEM, default is `packaging.version.parse('1.0')`

    Returns
    -------
    geometry : shapely.geometry
        The Shapely geometry object for the shape
    '''
    if shape == 'rectangle':
        if classifier_version == version.parse('1.0'):
            x, y, width, height = params
        else:
            x_center, y_center, width, height = params
            x = x_center - 0.5 * width
            y = y_center - 0.5 * height
        rectangle = shapely.geometry.box(x, y, x + width, y + height)
        return rectangle
    elif shape == 'rotateRectangle':
        if classifier_version == version.parse('1.0'):
            x, y, width, height, angle = params
        else:
            x_center, y_center, width, height, angle = params
            x = x_center - 0.5 * width
            y = y_center - 0.5 * height
        rot_rectangle = shapely.geometry.box(x, y, x + width, y + height)
        rot_rectangle = shapely.affinity.rotate(rot_rectangle, angle)
        return rot_rectangle
    elif shape == 'temporalRotateRectangle':
        # only defined for classifier_version = 2
        xc, yc, width, height, angle, _ = params
        x, y = xc - 0.5 * width, yc - 0.5 * height
        rot_rectangle = shapely.geometry.box(x, y, x + width, y + height)
        rot_rectangle = shapely.affinity.rotate(rot_rectangle, angle)
        return rot_rectangle
    elif (shape == 'column') or (shape == 'graph2dRangeX'):
        x_center, width = params
        x = x_center - 0.5 * width
        # the column tool is technically a line
        # making it a box of height 1 make the IoU metric work as expected
        column = shapely.geometry.box(x, 0, x + width, 1)
        return column
    elif shape == 'circle':
        # same for all classifier_version
        x, y, r = params
        circle = shapely.geometry.Point(x, y).buffer(r)
        return circle
    elif shape == 'ellipse':
        x, y, rx, ry, angle = params
        if classifier_version == version.parse('1.0'):
            angle = -angle
        ellipse = shapely.geometry.Point(x, y).buffer(1)
        ellipse = shapely.affinity.scale(ellipse, rx, ry)
        ellipse = shapely.affinity.rotate(ellipse, angle)
        return ellipse
    elif shape == 'triangle':
        # only defined for classifier_version = 1
        x, y, r, angle = params
        triangle = shapely.geometry.Polygon([
            [0, -r],
            [r * numpy.sqrt(3) / 2, r / 2],
            [-r * numpy.sqrt(3) / 2, r / 2]
        ])
        triangle = shapely.affinity.rotate(triangle, -angle, origin=(0, 0))
        triangle = shapely.affinity.translate(triangle, xoff=x, yoff=y)
        return triangle
    else:
        raise ValueError(f'The IoU metric only works with the following shapes: {VALID_IOU_SHAPES}')


def IoU_metric(params1, params2, shape, eps_t=None, classifier_version='1.0'):
    '''Find the Intersection of Union distance between two shapes.

    Parameters
    ----------
    params1 : list
        A list of the parameters for shape 1 (as defined by PFE)
    params2 : list
        A list of the parameters for shape 2 (as defined by PFE)
    shape : string
        The shape these parameters belong to (see :meth:`panoptes_to_geometry` for
        supported shapes)
    eps_t : float
        For temporal tools, this defines the temporal width of the rectangle.
        Two shapes are connected if the displayTime parameters are within eps_t.
    classifier_version : str
        The version of classifier used to make the classifications, either `"1.0"` for PFE or `"2.0"`
        for FEM, default is "1.0"

    Returns
    -------
    distance : float
        The IoU distance between the two shapes.  0 means the shapes are the same,
        1 means the shapes don't overlap, values in the middle mean partial
        overlap.
    '''
    classifier_version = version.parse(classifier_version)
    geo1 = panoptes_to_geometry(params1, shape, classifier_version=classifier_version)
    geo2 = panoptes_to_geometry(params2, shape, classifier_version=classifier_version)
    intersection = 0
    if geo1.intersects(geo2):
        intersection = geo1.intersection(geo2).area

    if 'temporal' in shape:
        # combine the shape IoU with the time difference and normalize
        # build two boxes in the time domain with width eps_t and height 1
        # centered at (t - eps_t / 2, 0.5) and calculate the intersection in time
        time_params1 = (params1[-1] - eps_t, 0, eps_t, 1)
        time_params2 = (params2[-1] - eps_t, 0, eps_t, 1)
        time_geo1 = panoptes_to_geometry(time_params1, 'rectangle', classifier_version=classifier_version)
        time_geo2 = panoptes_to_geometry(time_params2, 'rectangle', classifier_version=classifier_version)
        time_intersection = 0
        if time_geo1.intersects(time_geo2):
            time_intersection = time_geo1.intersection(time_geo2).area

        intersection = intersection * time_intersection
        union = ((geo1.area + geo2.area) * eps_t - intersection)
    else:
        union = geo1.union(geo2).area

    if union == 0:
        # catch divide by zero (i.e. cases when neither shape has an area)
        return numpy.inf

    return 1 - intersection / union


def average_bounds(params_list, shape, classifier_version=version.parse('1.0')):
    '''Find the bounding box for the average shape for each of the shapes
    parameters.

    Parameters
    ----------
    params_list : list
        A list of shape parameters that are being averaged
    shape : string
        The shape these parameters belong to (see :meth:`panoptes_to_geometry` for
        supported shapes)
    classifier_version : packaging.version
        The version of classifier used to make the classifications, either `1.0` for PFE or `2.0`
        for FEM, default is `packaging.version.parse('1.0')`

    Returns
    -------
    bound : list
        This is a list of tuples giving the min and max bounds for
        each shape parameter.
    '''
    geo = panoptes_to_geometry(params_list[0], shape, classifier_version=classifier_version)
    # Use the union of all shapes to find the bounding box
    for params in params_list[1:]:
        geo = geo.union(panoptes_to_geometry(params, shape, classifier_version=classifier_version))
    # bound on x
    bx = (geo.bounds[0], geo.bounds[2])
    # bound on y
    by = (geo.bounds[1], geo.bounds[3])
    # width of geo
    dx = bx[1] - bx[0]
    # height of geo
    dy = by[1] - by[0]
    # bound is a list of tuples giving (min, max) values for each parameters of the shape
    bound = [bx, by]
    if shape in ['rectangle', 'rotateRectangle', 'temporalRotateRectangle', 'column', 'graph2dRangeX', 'ellipse']:
        # bound on width or radius_x, min set to 1 pixel
        bound.append((1, dx))
        # bound on height or radius_y, min set to 1 pixel
        bound.append((1, dy))
        if shape in ['rotateRectangle', 'ellipse', 'temporalRotateRectangle']:
            # bound on angle (capped at 180 due to symmetry)
            bound.append((0, 180))
    elif shape in ['circle', 'triangle']:
        # bound on radius
        bound.append((1, max(dx, dy)))
        if shape == 'triangle':
            # triangle has three fold symmetry
            bound.append((0, 120))

    if 'temporal' in shape:
        bound.append((0, 1))

    return bound


def scale_shape(params, shape, gamma, classifier_version=version.parse('1.0')):
    '''Scale a given shape about its center by the given scale factor

    Parameters
    ----------
    params : list
        A list of the parameters for the shape (as defined by PFE)
    shape : string
        The name of the shape these parameters belong to (see :meth:`panoptes_to_geometry` for
        supported shapes)
    gamma : float
        The scaling factor to use
    classifier_version : packaging.version
        The version of classifier used to make the classifications, either `1.0` for PFE or `2.0`
        for FEM, default is `packaging.version.parse('1.0')`

    Returns
    -------
    scaled_params : list
        A list of parameters for the scaled shape
    '''
    # uniform scaling of each shape about its center
    if shape == 'rectangle':
        if classifier_version == version.parse('1.0'):
            return [
                # upper left corner moves
                params[0] + (params[2] * (1 - gamma) / 2),
                params[1] + (params[3] * (1 - gamma) / 2),
                # width and height scale
                gamma * params[2],
                gamma * params[3]
            ]
        else:
            return [
                # center point does not change
                params[0],
                params[1],
                # width and height scale
                gamma * params[2],
                gamma * params[3]
            ]
    elif shape == 'rotateRectangle':
        if classifier_version == version.parse('1.0'):
            return [
                # upper left corner moves
                params[0] + (params[2] * (1 - gamma) / 2),
                params[1] + (params[3] * (1 - gamma) / 2),
                # width and height scale
                gamma * params[2],
                gamma * params[3],
                # angle does not change
                params[4]
            ]
        else:
            return [
                # center point does not change
                params[0],
                params[1],
                # width and height scale
                gamma * params[2],
                gamma * params[3],
                # angle does not change
                params[4]
            ]
    elif shape == 'temporalRotateRectangle':
        return [
            # center point does not change
            params[0],
            params[1],
            # width and height scale
            gamma * params[2],
            gamma * params[3],
            # angle does not change
            params[4],
            # time does not change
            params[5]
        ]
    elif (shape == 'column') or (shape == 'graph2dRangeX'):
        return [
            params[0],
            gamma * params[1]
        ]
    elif shape == 'circle':
        return [
            # center is the same
            params[0],
            params[1],
            # radius scales
            gamma * params[2]
        ]
    elif shape == 'ellipse':
        return [
            # center is the same
            params[0],
            params[1],
            # radius_x and radius_y scale
            gamma * params[2],
            gamma * params[3],
            # angle does not change
            params[4]
        ]
    elif shape == 'triangle':
        return [
            params[0],
            params[1],
            gamma * params[2],
            params[3]
        ]
    else:
        raise ValueError(f'The IoU metric only works with the following shapes: {VALID_IOU_SHAPES}')


def average_shape_IoU(params_list, shape, eps_t=None, estimate=False, classifier_version='1.0'):
    '''Find the average shape and standard deviation from a list of parameters with respect
    to the IoU metric.

    Parameters
    ----------
    params_list : list
        A list of shape parameters that are being averaged
    shape : string
        The shape these parameters belong to (see :meth:`panoptes_to_geometry` for
        supported shapes)
    estimate : bool (optional)
        Estimate the average and sigma by the most representative shape from the cluster,
        this is significantly faster to compute than the true average, False by default.
    classifier_version : str
        The version of classifier used to make the classifications, either `"1.0"` for PFE or `"2.0"`
        for FEM, default is "1.0"
        
    Returns
    -------
    average_shape : list
        A list of shape parameters for the average shape

    sigma : float
        The standard deviation of the input shapes with respect to the IoU metric
    '''
    classifier_version = version.parse(classifier_version)
    if estimate:
        N = len(params_list)
        distance_matrix = numpy.zeros((N, N))
        for i in range(N):
            for j in range(i + 1, N):
                distance = IoU_metric(params_list[i], params_list[j], shape=shape, eps_t=eps_t, classifier_version=classifier_version)
                distance_matrix[i, j] = distance
                distance_matrix[j, i] = distance
        sum_square_distance = numpy.sum(distance_matrix**2, axis=1)
        mdx = numpy.argmin(sum_square_distance)
        sigma = numpy.sqrt(sum_square_distance[mdx] / max((N - 1), 1))
        return params_list[mdx], sigma
    else:
        geo_list = [panoptes_to_geometry(p, shape, classifier_version=classifier_version) for p in params_list]
        if 'temporal' in shape:
            time_geo_list = [panoptes_to_geometry((params[-1] - eps_t, 0, eps_t, 1), 'rectangle', classifier_version=classifier_version)
                            for params in params_list]
            geo_areas = numpy.array([geo_item.area for geo_item in geo_list])

        def sum_distance(x):
            geo = panoptes_to_geometry(x, shape, classifier_version=classifier_version)
            intersections = shapely.intersection(geo, geo_list)
            intersections = numpy.array([inter.area for inter in intersections])
            if 'temporal' in shape:
                time_geo = panoptes_to_geometry((x[-1] - eps_t, 0, eps_t, 1), 'rectangle', classifier_version=classifier_version)
                time_intersections = shapely.intersection(time_geo, time_geo_list)
                time_intersections = numpy.array([inter.area for inter in time_intersections])
                intersections = intersections * time_intersections
                unions = ((geo.area + geo_areas) * eps_t - intersections)
            else:
                unions = shapely.union(geo, geo_list)
                unions = numpy.array([uni.area for uni in unions])
            iou_distances = [1 - intersections[i] / unions[i] if unions[i] > 0 else numpy.inf for i in range(len(unions))]
            iou_distances = numpy.array(iou_distances)
            return numpy.sum(iou_distances**2)
        # find shape that minimizes the variance in the IoU metric using bounds
        m = scipy.optimize.direct(
            sum_distance,
            locally_biased=False,
            bounds=average_bounds(params_list, shape, classifier_version=classifier_version)
        )
        # find the 1-sigma value
        sigma = numpy.sqrt(m.fun / max((len(params_list) - 1), 1))
        return list(m.x), sigma


def sigma_shape(params, shape, sigma, classifier_version='1.0'):
    '''Return the plus and minus one sigma shape given the starting parameters
    and sigma value.

    Parameters
    ----------
    params : list
        A list of the parameters for the shape (as defined by PFE or FEM)
    shape : string
        The name of the shape these parameters belong to (see :meth:`panoptes_to_geometry` for
        supported shapes)
    sigma : float
        The standard deviation used to scale up and down the input shape
    classifier_version : str
        The version of classifier used to make the classifications, either `"1.0"` for PFE or `"2.0"`
        for FEM, default is "1.0"

    Returns
    -------
    plus_sigma : list
        A list of shape parameters for the 1-sigma scaled up average
    minus_sigma : list
        A list of shape parameters for the 1-sigma scaled down average
    '''
    classifier_version = version.parse(classifier_version)
    gamma = numpy.sqrt(1 - sigma)
    plus_sigma = scale_shape(params, shape, 1 / gamma, classifier_version=classifier_version)
    minus_sigma = scale_shape(params, shape, gamma, classifier_version=classifier_version)
    return plus_sigma, minus_sigma
