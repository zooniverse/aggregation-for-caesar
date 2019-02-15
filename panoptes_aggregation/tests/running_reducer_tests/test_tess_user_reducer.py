from panoptes_aggregation.running_reducers.tess_user_reducer import tess_user_reducer
from .base_test_class import RunningReducerTestNoProcessing

extracted_data = [
    {
        'value': [
            True,
            True,
            False,
            True
        ]
    }
]

kwargs_extra_data = {
    'relevant_reduction': [
        {
            'True': 5,
            'False': 3
        }
    ],
    'store': [
        {
            'seed': 1,
            'count': 5
        }
    ]
}

reduced_data = {
    'data': {
        'skill': 1.3594559055874569
    },
    'store': {
        'seed': 4.125,
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
