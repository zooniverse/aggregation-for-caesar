from panoptes_aggregation.reducers.tess_gold_standard_reducer import process_data, tess_gold_standard_reducer
from .base_test_class import ReducerTest

extracted_data = [
    {
        'feedback':
            [
                {'success': True},
                {'success': True},
                {'success': False},
                {'success': True}
            ]
    },
    {
        'feedback':
            [
                {'success': False},
                {'success': True},
                {'success': False},
                {'success': True}
            ]
    },
    {
        'feedback':
            [
                {'success': True},
                {'success': False},
                {'success': True},
                {'success': True}
            ]
    },
    {
        'feedback': None
    },
    {
        'feedback':
            [
                {'success': True},
                {'success': True},
                {'success': False},
                {'success': True}
            ]
    }
]

processed_data = [
    [True, True, False, True],
    [False, True, False, True],
    [True, False, True, True],
    [True, True, False, True],
]

reduced_data = {
    'difficulty': [
        0.75,
        0.75,
        0.25,
        1.0
    ]
}

TestTESSGoldStandardReducer = ReducerTest(
    tess_gold_standard_reducer,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test TESS gold standard reducer',
    add_version=False,
    processed_type='list'
)

extracted_data_empty = []

processed_data_empty = []

reduced_data_empty = {}

TestTESSGoldStandardReducerEmpty = ReducerTest(
    tess_gold_standard_reducer,
    process_data,
    extracted_data_empty,
    processed_data_empty,
    reduced_data_empty,
    'Test TESS gold standard reducer with no extracts',
    add_version=False,
    processed_type='list'
)
