'''
TESS Column Running Reducer
---------------------------
This module porvides functions to reduce the column task extracts for the TESS project in running mode.
Extracts are from :mod:`panoptes_aggregation.extractors.shape_extractor`.
'''
from .running_reducer_wrapper import running_reducer_wrapper
from ..reducers.tess_reducer_column import DEFAULTS, process_data, tess_reducer_column


@running_reducer_wrapper(defaults_data=DEFAULTS, user_id=True, relevant_reduction=True)
def tess_reducer_column_rr(data, **kwargs):
    '''
    See :meth:`panoptes_aggregation.reducers.tess_reducer_column.tess_reducer_column`
    '''
    store = kwargs.pop('store')
    current_data = process_data(data)
    user_id = store.get('user_id', []) + kwargs.pop('user_id')
    relevant_reduction = store.get('relevant_reduction', []) + kwargs.pop('relevant_reduction')
    data_by_tool = store.get('data_by_tool', {'data': [], 'index': []})
    data_by_tool['data'] += current_data['data']
    if len(data_by_tool['index']) == 0:
        data_by_tool['index'] = current_data['index']
    else:
        data_by_tool['index'] += [max(data_by_tool['index']) + 1] * len(current_data['index'])
    clusters = tess_reducer_column._original(
        data_by_tool,
        user_id=user_id,
        relevant_reduction=relevant_reduction,
        **kwargs
    )
    clusters['_store'] = {
        'data_by_tool': data_by_tool,
        'user_id': user_id,
        'relevant_reduction': relevant_reduction
    }
    return clusters
