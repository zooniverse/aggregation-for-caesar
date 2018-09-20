from .text_utils import angle_metric
import numpy as np


def angle_euclidean_metric(a, b):
    theta_distance_2 = angle_metric(a[-1], b[-1]) ** 2
    space_distance_2 = (a[:-1] - b[:-1]) ** 2
    distance = np.sqrt(space_distance_2.sum() + theta_distance_2)
    return distance


def angle_mean(data, angle=False, kind=None):
    theta = data[:, -1]
    if angle:
        if (kind == 'angle') and (theta.max() - theta.min() > 180):
            ndx = theta < 0
            data[ndx, -1] += 360
        if (kind == 'rotation') and (theta.max() - theta.min() > 180):
            ndx = theta > 180
            data[ndx, -1] -= 360
    return data.mean(axis=0)
