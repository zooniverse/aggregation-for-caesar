import numpy as np
from sklearn.cluster import DBSCAN
from .process_kwargs import process_kwargs
from .cluster_points import cluster_points, DEFAULTS
from collections import OrderedDict


def process_data(data_list):
    data_by_frame = {}
    for data in data_list:
        for frame, value in data.items():
            data_by_frame.setdefault(frame, {})
            data_by_frame[frame].setdefault('loc', [])
            data_by_frame[frame].setdefault('text', [])
            for x, y, t in zip(value['points']['x'], value['points']['y'], value['text']):
                data_by_frame[frame]['loc'].append((x, y))
                data_by_frame[frame]['text'].append(t)
    return data_by_frame


def cluster_poly_lines(data_by_frame, **kwargs):
    reduced_data = OrderedDict()
    data_by_frame_locs = {}
    for frame, value in data_by_frame.items():
        data_by_frame_locs[frame] = value['loc']
    full_cluster_data = cluster_points(data_by_frame_locs, **kwargs)
    for frame in sorted(data_by_frame.keys()):
        reduced_data[frame] = OrderedDict()
        reduced_data[frame]['clusters_x'] = full_cluster_data['{0}_clusters_x'.format(frame)]
        reduced_data[frame]['clusters_y'] = full_cluster_data['{0}_clusters_y'.format(frame)]
        reduced_data[frame]['clusters_text'] = []
        labels = np.array(full_cluster_data['{0}_cluster_labels'.format(frame)])
        for k in set(labels):
            kdx = labels == k
            text_list = list(np.array(data_by_frame[frame]['text'])[kdx])
            reduced_data[frame]['clusters_text'].append(text_list)
    return reduced_data


def poly_line_text_reducer_request(request):
    data = process_data([d['data'] for d in request.get_json()])
    kwargs = process_kwargs(request.args, DEFAULTS)
    return cluster_poly_lines(data, **kwargs)


def reducer_base(data_in, **kwargs):
    data = process_data(data_in)
    kwargs_parse = process_kwargs(kwargs, DEFAULTS)
    return cluster_poly_lines(data, **kwargs_parse)
