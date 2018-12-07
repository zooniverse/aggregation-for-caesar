from panoptes_aggregation.reducers.tess_reducer_column import process_data, tess_reducer_column
from .base_test_class import ReducerTest
import numpy as np
from scipy.stats import norm


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
    {},
    {}
]

processed_data = {
    'count_classified': 5,
    'frame0': {
        'T0_tool0_count': 3,
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

x_eval = np.arange(0, 150.01, 0.01)
x_center = [0.5, 150, 75, 0.5, 150, 50, 102.5, 57]
width = [1, 100, 50, 1, 100, 100, 5, 4]
tick_pdf = np.zeros_like(x_eval)
for x, w in zip(x_center, width):
    tick_pdf += norm.pdf(x_eval, loc=x, scale=w/2.355)

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
        ],
        'T0_tool0_pdf': tick_pdf.round(5).tolist(),
        'T0_tool0_x_eval': x_eval.round(5).tolist(),
        'T0_tool0_count_ratio': 1.5
    }
}

TestShapeReducerColumn = ReducerTest(
    tess_reducer_column,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test TESS column reducer',
    kwargs={
        'x_min': 0,
        'x_max': 150,
        'x_step': 0.01,
        'thres': 0.05,
        'min_dist': 2
    }
)
