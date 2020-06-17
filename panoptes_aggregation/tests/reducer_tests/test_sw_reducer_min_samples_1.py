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
            ],
            'gold_standard': False
        }
    }
]

kwargs_extra_data = {
    'user_id': [
        1
    ]
}

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
        ],
        'gold_standard': [
            False
        ],
        'data_index': [
            0
        ]
    }
}

reduced_data = {
    'reducer': 'poly_line_text_reducer',
    'low_consensus_lines': 1,
    'transcribed_lines': 1,
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
            'consensus_text': 'Gather as many rose',
            'gutter_label': 0,
            'line_slope': 0.80162463698921349,
            'number_views': 1,
            'slope_label': 0,
            'gold_standard': [False],
            'user_ids': [1],
            'extract_index': [0],
            'low_consensus': True,
            'flagged': True
        }
    ],
    'parameters': {
        'eps_slope': 0.5,
        'eps_line': 15.0,
        'eps_word': 30.0,
        'gutter_tol': 0.0,
        'min_samples': 1,
        'dot_freq': 'line',
        'min_word_count': 1,
        'low_consensus_threshold': 3.0,
        'process_by_line': False,
        'minimum_views': 5
    }
}

TestSWReducerMinSample = ReducerTest(
    poly_line_text_reducer,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test SW text reducer with min_samples=1',
    okwargs={
        'gutter_tol': 0.0,
        'min_word_count': 1,
        'low_consensus_threshold': 3.0,
        'minimum_views': 5
    },
    kwargs={
        'eps_slope': 0.5,
        'eps_line': 15.0,
        'eps_word': 30.0,
        'dot_freq': 'line',
        'min_samples': 1
    },
    network_kwargs=kwargs_extra_data,
    output_kwargs=True,
    test_name='TestSWReducerMinSample'
)
