from panoptes_aggregation.running_reducers.tess_reducer_column import tess_reducer_column_rr
from .base_test_class import RunningReducerTestNoProcessing

extracted_data = [{
    'frame0': {
        'T0_tool0_x': [
            0.0,
            100.0
        ],
        'T0_tool0_width': [
            100.0,
            5.0
        ]
    }
}]

kwargs_extra_data = {
    'user_id': [3],
    'relevant_reduction': [{'data': {'skill': 0.1}}],
    'store': {
        'data_by_tool': {
            'data': [
                [0.0, 1.0],
                [100.0, 100.0],
                [101.0, 101.0],
                [50.0, 50.0],
                [0.0, 1.0],
                [100.0, 100.0],
                [55.0, 4.0]
            ],
            'index': [
                0,
                0,
                0,
                0,
                1,
                1,
                1
            ]
        },
        'relevant_reduction': [
            {'data': {'skill': 0.4}},
            {'data': {'skill': 0.8}}
        ],
        'user_id': [
            1,
            2
        ]
    }
}

reduced_data = {
    'centers': [
        0.5,
        150.0,
        78.16666666666667
    ],
    'widths': [
        1.0,
        100.0,
        19.666666666666668
    ],
    'counts': [
        2,
        2,
        3
    ],
    'weighted_counts': [
        1.2000000000000002,
        1.2000000000000002,
        1.3000000000000003
    ],
    'user_ids': [
        [1, 2],
        [1, 2],
        [1, 2, 3]
    ],
    'max_weighted_count': 1.3000000000000003,
    '_store': {
        'data_by_tool': {
            'data': [
                [0.0, 1.0],
                [100.0, 100.0],
                [101.0, 101.0],
                [50.0, 50.0],
                [0.0, 1.0],
                [100.0, 100.0],
                [55.0, 4.0],
                [0.0, 100.0],
                [100.0, 5.0]
            ],
            'index': [
                0,
                0,
                0,
                0,
                1,
                1,
                1,
                2,
                2
            ]
        },
        'relevant_reduction': [
            {'data': {'skill': 0.4}},
            {'data': {'skill': 0.8}},
            {'data': {'skill': 0.1}}
        ],
        'user_id': [
            1,
            2,
            3
        ]
    }
}

TestTESSReducerColumnLeft = RunningReducerTestNoProcessing(
    tess_reducer_column_rr,
    extracted_data,
    reduced_data,
    'Test Tess column reducer in running mode with x=left',
    kwargs={
        'x': 'left',
        'eps': 50,
        'min_samples': 2
    },
    network_kwargs=kwargs_extra_data
)

kwargs_extra_data_no_store = {
    'user_id': [3],
    'relevant_reduction': [{'data': {'skill': 0.1}}],
    'store': {}
}

reduced_data_no_store = {
    'max_weighted_count': None,
    '_store': {
        'data_by_tool': {
            'data': [
                [0.0, 100.0],
                [100.0, 5.0]
            ],
            'index': [
                0,
                0
            ]
        },
        'relevant_reduction': [
            {'data': {'skill': 0.1}}
        ],
        'user_id': [
            3
        ]
    }
}

TestTESSReducerColumnNoStore = RunningReducerTestNoProcessing(
    tess_reducer_column_rr,
    extracted_data,
    reduced_data_no_store,
    'Test Tess column reducer in running mode with no store',
    kwargs={
        'x': 'center',
        'eps': 50,
        'min_samples': 2
    },
    network_kwargs=kwargs_extra_data_no_store
)
