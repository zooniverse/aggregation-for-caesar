from functools import wraps
from panoptes_aggregation.shape_tools import SHAPE_LUT_FEM


OTHER_SHAPES = {
    'freehandLine': ['x', 'y'],
    'polygon': ['x', 'y']
}


def collab_wrapper(func):
    @wraps(func)
    def wrapper(data, **kwargs):
        collab = kwargs.pop('collab', False)
        step_key = kwargs.pop('step_key', 'S0')
        task_index = kwargs.pop('task_index', 0)
        min_threshold = kwargs.pop('min_threshold', 0)

        # data is the `processed` data
        tool_type = data.get('shape', None)
        if tool_type == 'column':
            # ensure the FEM tool name is used
            tool_type = 'graph2dRangeX'
        # remove n_classifications from the processed data
        # as it is not expected for the reducers
        n_classifications = data.pop('n_classifications', 1)

        # call the original function with the collab keywords stripped off
        reduced_data = func(data, **kwargs)
        # Only needed for FEM shapes
        output_data = None

        if (tool_type not in SHAPE_LUT_FEM) and (tool_type not in OTHER_SHAPES):
            # tool does not support collab
            collab = False

        if collab:
            if tool_type in OTHER_SHAPES:
                shape_params = OTHER_SHAPES[tool_type]
            else:
                shape_params = SHAPE_LUT_FEM[tool_type]
            output_data = []
            for frame_key, frame in reduced_data.items():
                frame_index = int(frame_key[5:])
                unique_tools = set([
                    '_'.join(k.split('_')[:2])
                    for k in frame.keys() if ('subtask' not in k) and ('details' not in k)
                ])
                for tool in unique_tools:
                    task_key, tool_index = tool.split('_')
                    # could be using "old key" keyword
                    # check to get the correct tool index value
                    if 'Index' in tool_index:
                        tool_index = int(tool_index[9:])
                    else:
                        tool_index = int(tool_index[4:])
                    if f'{tool}_clusters_count' in frame:
                        for idx, clusters_count in enumerate(frame[f'{tool}_clusters_count']):
                            threshold = clusters_count / n_classifications
                            if threshold > min_threshold:
                                annotation = {
                                    'stepKey': step_key,
                                    'taskIndex': task_index,
                                    'taskKey': task_key,
                                    'taskType': 'drawing',
                                    'toolIndex': tool_index,
                                    'frame': frame_index,
                                    # markId needs to be a unique string for each cluster
                                    'markId': f'collab_{frame_key}_{tool}_{idx}',
                                    'toolType': tool_type
                                }
                                if tool_type == 'freehandLine':
                                    # param name is different for annotation
                                    # x -> pathX, y -> pathY
                                    annotation['pathX'] = frame[f'{tool}_clusters_x'][idx]
                                    annotation['pathY'] = frame[f'{tool}_clusters_y'][idx]
                                elif tool_type == 'polygon':
                                    # param output is different for annotation
                                    # points = [{'x': x[0], 'y': y[0]}, ...]
                                    annotation['points'] = [
                                        {'x': x, 'y': y}
                                        for x, y in zip(
                                            frame[f'{tool}_clusters_x'][idx],
                                            frame[f'{tool}_clusters_y'][idx]
                                        )
                                    ]
                                else:
                                    # otherwise the output names are the same as the inputs
                                    for param in shape_params:
                                        annotation[param] = frame[f'{tool}_clusters_{param}'][idx]
                                output_data.append(annotation)
            # sort to help with unit tests
            output_data.sort(
                key=lambda d: (d['frame'], d['toolIndex'], int(d['markId'].split('_')[-1]))
            )
            reduced_data['data'] = output_data
        return reduced_data
    return wrapper
