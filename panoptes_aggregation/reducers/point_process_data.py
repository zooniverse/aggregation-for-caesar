def process_data_by_frame(data):
    '''Process a list of extractions into lists of `x` and `y` sorted by `tool`

    Parameters
    ----------
    data : list
        A list of extractions crated by
        :meth:`panoptes_aggregation.extractors.point_extractor.point_extractor`

    Returns
    -------
    processed_data : dict
        A dictionary with each key being a `tool` with a list of (`x`, `y`)
        tuples as a value
    '''
    unique_frames = set(sum([list(d.keys()) for d in data], []))
    data_by_tool = {}
    for frame in unique_frames:
        if not frame.startswith('frame'):
            continue
        data_by_tool[frame] = {}
        unique_tools = set(sum([['_'.join(k.split('_')[:-1]) for k in d.get(frame, {}).keys()] for d in data], []))
        for tool in unique_tools:
            for d in data:
                if frame in d:
                    data_by_tool[frame].setdefault(tool, [])
                    if ('{0}_x'.format(tool) in d[frame]) and ('{0}_y'.format(tool) in d[frame]):
                        data_by_tool[frame][tool] += list(zip(d[frame]['{0}_x'.format(tool)], d[frame]['{0}_y'.format(tool)]))
    return data_by_tool


def process_temporal_data(data):
    '''Process a list of extractions into lists of `x` and `y` sorted by `tool`

    Parameters
    ----------
    data : list
        A list of extractions crated by
        :meth:`panoptes_aggregation.extractors.point_extractor.point_extractor`

    Returns
    -------
    processed_data : dict
        A dictionary with each key being a `tool` with a list of (`x`, `y`)
        tuples as a value
    '''
    unique_frames = set(sum([list(d.keys()) for d in data], []))
    data_by_tool = {}
    for frame in unique_frames:
        if not frame.startswith('frame'):
            continue
        data_by_tool[frame] = {}
        unique_tools = set(sum([['_'.join(k.split('_')[:-1]) for k in d.get(frame, {}).keys()] for d in data], []))
        for tool in unique_tools:
            for d in data:
                if frame in d:
                    data_by_tool[frame].setdefault(tool, [])
                    if (f'{tool}_x' in d[frame]) and (f'{tool}_y' in d[frame]) and (f'{tool}_displayTime' in d[frame]):
                        data_by_tool[frame][tool] += list(zip(d[frame][f'{tool}_x'], d[frame][f'{tool}_y'], d[frame][f'{tool}_displayTime']))
    return data_by_tool


def temporal_metric(point1, point2):
    '''
        Metric for points that contain (x, y) as well as temporal data.
        This metric weights individual coordinates by the time coordinate.
    '''
    x1, y1, displayTime1 = point1
    x2, y2, displayTime2 = point2

    # adjust the time by a small epsilon so that we don't zero out the metric
    displayTime1 += 1
    displayTime2 += 1

    return ((x1 * displayTime1 - x2 * displayTime2)**2 + (y1 * displayTime1 - y2 * displayTime2)**2)
