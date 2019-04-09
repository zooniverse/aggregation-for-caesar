from panoptes_aggregation.running_reducers.tess_user_reducer import tess_user_reducer
from .base_test_class import RunningReducerTestNoProcessing

extracted_data = [{
    'feedback':
        [
            {'success': True},
            {'success': True},
            {'success': False},
            {'success': True}
        ]
}]

kwargs_extra_data = {
    'relevant_reduction': [
        {
            'data': {
                'difficulty': [
                    0.9,
                    0.4,
                    0.1,
                    0.8
                ]
            }
        }
    ],
    'store': {
        'seed': 1,
        'count': 5
    }
}

reduced_data = {
    'skill': 1.4617994418680003,
    '_store': {
        'seed': 5.1,
        'count': 9
    }
}

TestTESSUserReduer = RunningReducerTestNoProcessing(
    tess_user_reducer,
    extracted_data,
    reduced_data,
    'Test TESS User reducer',
    network_kwargs=kwargs_extra_data
)

kwargs_extra_data_no_rr = {
    'relevant_reduction': [
        None
    ],
    'store': {}
}

reduced_data_no_rr = {
    'skill': 1.0,
    '_store': {
        'seed': 0,
        'count': 4
    }
}

TestTESSUserReduerNoRR = RunningReducerTestNoProcessing(
    tess_user_reducer,
    extracted_data,
    reduced_data_no_rr,
    'Test TESS User reducer with no relevant reduction',
    network_kwargs=kwargs_extra_data_no_rr
)

kwargs_extra_data_no_gs_extract = {
    'relevant_reduction': [
        {
            'data': {}
        }
    ],
    'store': {}
}

TestTESSUserReduerNoGSExtract = RunningReducerTestNoProcessing(
    tess_user_reducer,
    extracted_data,
    reduced_data_no_rr,
    'Test TESS User reducer with no GS extract',
    network_kwargs=kwargs_extra_data_no_gs_extract
)
