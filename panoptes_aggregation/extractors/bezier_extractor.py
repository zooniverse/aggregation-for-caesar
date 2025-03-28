'''
Bezier Tool Extractor
---------------------
This module provides a function to extract Bezier drawn
classifications from panoptes annotations.
'''
from collections import OrderedDict
import numpy as np
from .extractor_wrapper import extractor_wrapper
from .subtask_extractor_wrapper import subtask_wrapper
from .tool_wrapper import tool_wrapper
from scipy.special import comb


def _bezier_curve_func(points, num_iters=10):
    num_points = len(points)

    t = np.linspace(0.0, 1.0, num_iters)
    polynomial_array =\
        np.array([comb(num_points - 1, i) * (t ** (num_points - 1 - i)) * (1 - t) ** i
                  for i in range(num_points)])

    xs = np.dot(points[:, 0], polynomial_array)
    ys = np.dot(points[:, 1], polynomial_array)
    xy = np.array([xs, ys]).T
    # Make sure in correct order
    xy = xy[::-1]
    return xy


@extractor_wrapper(gold_standard=False)
@tool_wrapper
@subtask_wrapper
def bezier_extractor(classification, **kwargs):
    '''Extact Bezier data from annotation.

    See the `Bezier wiki <https://en.wikipedia.org/wiki/B%C3%A9zier_curve>`_
    for more info about Bezier curves.

    The output extraction is full xy curves, based on the individual Bezier
    curves from input control points stitched together into a single continuous
    curve. The individual Bezier curves have 10 points constructed from the
    3 control points of the quadratic Bezier curve.

    Parameters
    ----------
    classification : dict
        A dictionary containing an `annotations` key that is a list of
        panoptes annotations. The x and y data of the classifications needs to
        be of the format 'points': {'x': x, 'y': y}. It is
        assumed the input xy data is a continuous set of triplets (the last value of a triplet is the starting value of the next triplet)
        corresponding to the quadratic Bezier control points.

    Returns
    -------
    extraction : dict
        A dictionary containing one key per frame. Each frame contains lists
        `pathX` and `pathY`. These are lists of lists, where each inner list of
        `pathX` is the x values, and each inner list of `pathY` is the y
        values, for a particular Bezier drawing.
    '''
    extract = OrderedDict()
    for annotation in classification['annotations']:
        task_key = annotation['task']
        for value in annotation['value']:
            tool_index = value['tool']
            key = '{0}_tool{1}'.format(task_key, tool_index)
            frame = 'frame{0}'.format(value.get('frame', 0))
            extract.setdefault(frame, {})

            points = value["points"]
            xy_values = np.array([[point["x"], point["y"]] for point in points])
            # Only include extracts with data to make a Bezier curve
            if len(xy_values) > 2:
                # If even number of points, shape is closed, meaning first
                # becomes the last point
                if len(xy_values) % 2 == 0:
                    xy_values = np.append(xy_values, [xy_values[0]], axis=0)
                bezier_curve = np.array([_bezier_curve_func(xy_values[i - 1:i + 2]) for i in range(1, len(xy_values), 2)])
                # Stack the curves back to back
                shape = np.shape(bezier_curve)
                bezier_curve = bezier_curve.reshape(shape[0] * shape[1], shape[2])
                # Store the x/y data
                x = bezier_curve[:, 0].tolist()
                y = bezier_curve[:, 1].tolist()
                extract[frame].setdefault('{0}_{1}'.format(key, 'pathX'), []).append(x)
                extract[frame].setdefault('{0}_{1}'.format(key, 'pathY'), []).append(y)
    return extract
