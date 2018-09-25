import numpy as np
from .angle_avg import get_avg_function


def angle_distance(theta1, theta2, factor=1):
    max_angle = 360 / factor
    d = abs(theta1 - theta2)
    return min(max_angle - d, d)


def get_angle_metric(factor=1):
    def angle_euclidean_metric(a, b):
        difference = a - b
        difference[-1] = angle_distance(a[-1], b[-1], factor=factor)
        distance = np.linalg.norm(difference)
        return distance
    return angle_euclidean_metric


SHAPE_FACTOR_LUT = {
    'ellipse': 1,
    'rotateRectangle': 1,
    'triangle': 1,
    'fan': 1,
}

SHAPE_FACTOR_SYMETRIC_LUT = {
    'ellipse': 2,
    'rotateRectangle': 2,
    'triangle': 3,
    'fan': 1,
}


def get_shape_metric_and_avg(shape, symetric=False):
    if symetric:
        factor = SHAPE_FACTOR_SYMETRIC_LUT.get(shape, None)
    else:
        factor = SHAPE_FACTOR_LUT.get(shape, None)
    if factor is not None:
        metric = get_angle_metric(factor=factor)
    else:
        metric = 'euclidean'
    avg = get_avg_function(factor=factor)
    return metric, avg
