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


def panoptes_to_geometry(params, shape):
    '''Convert shapes created with the Panoptes Front End (PFE) to shapely
    geometry objects.

    Parameters
    ----------
    params : list
        A list of the parameters for the shape (as defined by PFE)
    shape : string
        The name of the shape these parameters belong to.  Supported shapes are:

        * rectangle
        * rotateRectangle
        * circle
        * ellipse
        * triangle

    Returns
    -------
    geometry : shapely.geometry
        The Shapely geometry object for the shape
    '''
    if shape == 'rectangle':
        x, y, width, height = params
        rectangle = shapely.geometry.box(x, y, x + width, y + height)
        return rectangle
    elif shape == 'rotateRectangle':
        x, y, width, height, angle = params
        rot_rectangle = shapely.geometry.box(x, y, x + width, y + height)
        rot_rectangle = shapely.affinity.rotate(rot_rectangle, angle)
        return rot_rectangle
    elif shape == 'circle':
        x, y, r = params
        circle = shapely.geometry.Point(x, y).buffer(r)
        return circle
    elif shape == 'ellipse':
        x, y, rx, ry, angle = params
        ellipse = shapely.geometry.Point(x, y).buffer(1)
        ellipse = shapely.affinity.scale(ellipse, rx, ry)
        ellipse = shapely.affinity.rotate(ellipse, -angle)
        return ellipse
    elif shape == 'triangle':
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
        raise ValueError('The IoU metric only works with the following shapes: rectangle, rotateing rectangle, circle, ellipse, or triangle')


def IoU_metric(params1, params2, shape):
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

    Returns
    -------
    distance : float
        The IoU distance between the two shapes.  0 means the shapes are the same,
        1 means the shapes don't overlap, values in the middle mean partial
        overlap.
    '''
    geo1 = panoptes_to_geometry(params1, shape)
    geo2 = panoptes_to_geometry(params2, shape)
    intersection = geo1.intersection(geo2).area
    union = geo1.union(geo2).area
    if union == 0:
        # catch divide by zero (i.e. cases when neither shape has an area)
        return numpy.inf
    return 1 - intersection / union


def average_bounds(params_list, shape):
    '''Find the bounding box for the average shape for each of the shapes
    parameters.

    Parameters
    ----------
    params_list : list
        A list of shape parameters that are being averaged
    shape : string
        The shape these parameters belong to (see :meth:`panoptes_to_geometry` for
        supported shapes)

    Returns
    -------
    bound : list
        This is a list of tuples giving the min and max bounds for
        each shape parameter.
    '''
    geo = panoptes_to_geometry(params_list[0], shape)
    # Use the union of all shapes to find the bounding box
    for params in params_list[1:]:
        geo = geo.union(panoptes_to_geometry(params, shape))
    # bound on x
    bx = (geo.bounds[0], geo.bounds[2])
    # bound on y
    by = (geo.bounds[1], geo.bounds[3])
    # width of geo
    dx = bx[1] - bx[0]
    # height of geo
    dy = by[1] - by[0]
    # bound is a list of tuples giving (min, max) values for each paramters of the shape
    bound = [bx, by]
    if shape in ['rectangle', 'rotateRectangle', 'ellipse']:
        # bound on width or radius_x, min set to 1 pixel
        bound.append((1, dx))
        # bound on height or radius_y, min set to 1 pixel
        bound.append((1, dy))
        if shape in ['rotateRectangle', 'ellipse']:
            # bound on angle (capped at 180 due to symmetry)
            bound.append((0, 180))
    elif shape in ['circle', 'triangle']:
        # bound on radius
        bound.append((1, max(dx, dy)))
        if shape == 'triangle':
            # triangle has three fold symmetry
            bound.append((0, 120))
    return bound


def scale_shape(params, shape, gamma):
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

    Returns
    -------
    scaled_params : list
        A list of parameters for the scaled shape
    '''
    # uniform scaling of each shape about its center
    if shape == 'rectangle':
        return [
            # upper left corner moves
            params[0] + (params[2] * (1 - gamma) / 2),
            params[1] + (params[3] * (1 - gamma) / 2),
            # width and height scale
            gamma * params[2],
            gamma * params[3]
        ]
    elif shape == 'rotateRectangle':
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
        raise ValueError('The IoU metric only works with the following shapes: rectangle, rotateing rectangle, circle, ellipse, or triangle')


def average_shape_IoU(params_list, shape):
    '''Find the average shape and standard deviation from a list of parameters with respect
    to the IoU metric.

    Parameters
    ----------
    params_list : list
        A list of shape parameters that are being averaged
    shape : string
        The shape these parameters belong to (see :meth:`panoptes_to_geometry` for
        supported shapes)

    Returns
    -------
    average_shape : list
        A list of shape parameters for the average shape

    sigma : float
        The standard deviation of the input shapes with respect to the IoU metric
    '''
    def sum_distance(x):
        return sum([IoU_metric(x, p, shape)**2 for p in params_list])
    # find shape that minimizes the variance in the IoU metric using bounds
    m = scipy.optimize.shgo(
        sum_distance,
        sampling_method='sobol',
        bounds=average_bounds(params_list, shape)
    )
    # find the 1-sigma value
    sigma = numpy.sqrt(m.fun / (len(params_list) - 1))
    return list(m.x), sigma


def sigma_shape(params, shape, sigma):
    '''Return the plus and minus one sigma shape given the starting parameters
    and sigma value.

    Parameters
    ----------
    params : list
        A list of the parameters for the shape (as defined by PFE)
    shape : string
        The name of the shape these parameters belong to (see :meth:`panoptes_to_geometry` for
        supported shapes)
    sigma : float
        The standard deviation used to scale up and down the input shape

    Returns
    -------
    plus_sigma : list
        A list of shape parameters for the 1-sigma scaled up average
    minus_sigma : list
        A list of shape parameters for the 1-sigma scaled down average
    '''
    gamma = numpy.sqrt(1 - sigma)
    plus_sigma = scale_shape(params, shape, 1 / gamma)
    minus_sigma = scale_shape(params, shape, gamma)
    return plus_sigma, minus_sigma
