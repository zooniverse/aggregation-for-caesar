import numpy as np


def avg_angle(theta, factor=1):
    sm = np.sin(np.deg2rad(factor * theta)).mean()
    cm = np.cos(np.deg2rad(factor * theta)).mean()
    return np.round(np.rad2deg(np.arctan2(sm, cm)) / factor, 10)


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
