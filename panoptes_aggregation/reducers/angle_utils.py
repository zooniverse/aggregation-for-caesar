import numpy as np


def angle_distance(theta1, theta2):
    d = abs(theta1 - theta2)
    return min(360 - d, d)


def avg_angle(theta):
    sm = np.sin(np.deg2rad(theta)).mean()
    cm = np.cos(np.deg2rad(theta)).mean()
    return np.rad2deg(np.arctan2(sm, cm))


def angle_euclidean_metric(a, b):
    theta_distance_2 = angle_distance(a[-1], b[-1]) ** 2
    space_distance_2 = (a[:-1] - b[:-1]) ** 2
    distance = np.sqrt(space_distance_2.sum() + theta_distance_2)
    return distance


def angle_mean(data, angle=False, kind=None):
    avg_data = data.mean(axis=0)
    if angle:
        theta = data[:, -1]
        avg_theta = avg_angle(theta)
        if (kind == 'rotation') and (avg_theta < 0):
            avg_theta += 360
            avg_theta %= 360
        avg_data[-1] = avg_theta
    return avg_data
