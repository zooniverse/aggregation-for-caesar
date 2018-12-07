from panoptes_aggregation.reducers.tess_reducer_column import process_data, tess_reducer_column
from .base_test_class import ReducerTest

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0, 50.0],
            'T0_tool0_width': [1.0, 100.0, 50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_width': [1.0, 100.0],
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0, 55.0],
            'T0_tool0_width': [100.0, 5.0, 4.0]
        }
    },
    {}
]

processed_data = {
    'shape': 'column',
    'symmetric': False,
    'frame0': {
        'T0_tool0': [
            (0.0, 1.0),
            (100.0, 100.0),
            (50.0, 50.0),
            (0.0, 1.0),
            (100.0, 100.0),
            (0.0, 100.0),
            (100.0, 5.0),
            (55.0, 4.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_tool0_peak_x': [
            0.5,
            57.01,
            102.49
        ],
        'T0_tool0_peak_pdf': [
            1.88386,
            0.25897,
            0.21045
        ]
    }
}

TestShapeReducerColumn = ReducerTest(
    tess_reducer_column,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test TESS column reducer',
    pkwargs={'shape': 'column'},
    kwargs={
        'x_min': 0,
        'x_max': 150,
        'x_step': 0.01,
        'thres': 0.05,
        'min_dist': 2
    }
)
