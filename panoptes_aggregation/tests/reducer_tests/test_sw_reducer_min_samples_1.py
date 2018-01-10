from panoptes_aggregation.reducers.poly_line_text_reducer import process_data, poly_line_text_reducer
from .base_test_class import ReducerTest

extracted_data = [
    {
        'frame0': {
            'points': {
                'x': [
                    [860.71, 1418.89]
                ],
                'y': [
                    [267.38, 275.19]
                ]
            },
            'text': [
                ['Gather as many rose']
            ],
            'slope': [
                0.80162463698921349
            ]
        }
    }
]

processed_data = {
    'frame0': {
        'x': [
            [860.71, 1418.89]
        ],
        'y': [
            [267.38, 275.19]
        ],
        'text': [
            ['Gather as many rose']
        ],
        'slope': [
            0.80162463698921349
        ]
    }
}

reduced_data = {
    'frame0': [
        {
            'clusters_text': [
                ['Gather'],
                ['as'],
                ['many'],
                ['rose']
            ],
            'clusters_x': [860.71, 1418.89],
            'clusters_y': [267.38, 275.19],
            'consensus_score': 1.0,
            'gutter_label': 0,
            'line_slope': 0.80162463698921349,
            'number_views': 1,
            'slope_label': 0
        }
    ]
}

TestSWReducer = ReducerTest(
    poly_line_text_reducer,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test SW text reducer',
    okwargs={
        'metric': 'euclidean',
        'gutter_tol': 0,
        'min_word_count': 1
    },
    kwargs={
        'eps_slope': 0.5,
        'eps_line': 15,
        'eps_word': 30,
        'dot_freq': 'line',
        'min_samples': 1
    }
)
