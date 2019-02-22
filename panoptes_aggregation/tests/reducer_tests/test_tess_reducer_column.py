from panoptes_aggregation.reducers.tess_reducer_column import process_data, tess_reducer_column
from .base_test_class import ReducerTest
import copy

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [
                0.0,
                100.0,
                50.0
            ],
            'T0_tool0_width': [
                1.0,
                100.0,
                50.0
            ]
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [
                0.0,
                100.0,
                55.0
            ],
            'T0_tool0_width': [
                1.0,
                100.0,
                4.0
            ],
        }
    },
    {
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
    },
    {},
    {}
]

kwargs_extra_data = {
    'user_id': [
        1,
        2,
        3,
        4,
        5
    ],
    'relevant_reduction': [
        {'data': {'skill': 0.4}},
        {'data': {'skill': 0.8}},
        {'data': {'skill': 0.1}},
        {'data': {'skill': 0.3}},
        {'data': {'skill': 0.2}}
    ]
}

processed_data = {
    'data': [
        (0.0, 1.0),
        (100.0, 100.0),
        (50.0, 50.0),
        (0.0, 1.0),
        (100.0, 100.0),
        (55.0, 4.0),
        (0.0, 100.0),
        (100.0, 5.0)
    ],
    'index': [
        0,
        0,
        0,
        1,
        1,
        1,
        2,
        2
    ]
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
    ]
}


TestTESSReducerColumnLeft = ReducerTest(
    tess_reducer_column,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test TESS column reducer x=left',
    kwargs={
        'x': 'left',
        'eps': 50,
        'min_samples': 2
    },
    network_kwargs=kwargs_extra_data
)

reduced_data_center = copy.deepcopy(reduced_data)
reduced_data_center['centers'] = [
    0.0,
    100.0,
    68.33333333333333
]

TestTESSReducerColumnCenter = ReducerTest(
    tess_reducer_column,
    process_data,
    extracted_data,
    processed_data,
    reduced_data_center,
    'Test TESS column reducer x=center',
    kwargs={
        'x': 'center',
        'eps': 50,
        'min_samples': 2
    },
    network_kwargs=kwargs_extra_data
)
