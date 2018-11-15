import numpy as np
from scipy.optimize import minimize_scalar


def angle_distance(theta1, theta2, factor=1):
    max_angle = 360 / factor
    d = abs(theta1 % max_angle - theta2 % max_angle)
    return min(max_angle - d, d)


def get_angle_metric(factor=1):
    def angle_euclidean_metric(a, b):
        difference = a - b
        difference[-1] = angle_distance(a[-1], b[-1], factor=factor)
        distance = np.linalg.norm(difference)
        return distance
    return angle_euclidean_metric


def avg_angle(theta, factor=1):
    def sum_distance(x):
        return sum([angle_distance(x, t, factor=factor)**2 for t in theta])
    m = minimize_scalar(
        sum_distance,
        bounds=(0, 360 / factor),
        method='Bounded'
    )
    return np.round(m.x, 3) % (360 / factor)


def get_avg_function(factor=None):
    if factor is None:
        def custom_average(data):
            return data.mean(axis=0)
    else:
        def custom_average(data):
            avg_data = data.mean(axis=0)
            theta = data[:, -1]
            avg_theta = avg_angle(theta, factor=factor)
            avg_data[-1] = avg_theta
            return avg_data
    return custom_average


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


def get_shape_metric_and_avg(shape, symmetric=False):
    if symmetric:
        factor = SHAPE_FACTOR_SYMETRIC_LUT.get(shape, None)
    else:
        factor = SHAPE_FACTOR_LUT.get(shape, None)
    if factor is not None:
        metric = get_angle_metric(factor=factor)
    else:
        metric = 'euclidean'
    avg = get_avg_function(factor=factor)
    return metric, avg
