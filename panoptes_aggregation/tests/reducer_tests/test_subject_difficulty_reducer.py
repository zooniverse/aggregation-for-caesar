from panoptes_aggregation.reducers.subject_difficulty_reducer import subject_difficulty_reducer
from .base_test_class import ReducerTest


def process(data):
    return data


extracted_data = [
    {
        'feedback':
            {
                "success": [
                    False,
                    False,
                    False
                ]
            }
    },
    {
        'feedback':
            {
                "success": [
                    True,
                    True,
                    True
                ]
            }
    },
    {
        'feedback':
            {
                "success": [
                    True,
                    True,
                    True
                ]
            }
    },
    {}
]


reduced_data = {
    "difficulty": [
        0.6666666666666666,
        0.6666666666666666,
        0.6666666666666666
    ]
}


TestGoldStandardReducer = ReducerTest(
    subject_difficulty_reducer,
    process,
    extracted_data,
    extracted_data,
    reduced_data,
    'Test  gold standard reducer',
    add_version=False,
    processed_type='list',
    test_name='TestGoldStandardReducer'
)

extracted_data_empty = []

processed_data_empty = []

reduced_data_empty = {}

TestGoldStandardReducerEmpty = ReducerTest(
    subject_difficulty_reducer,
    process,
    extracted_data_empty,
    extracted_data_empty,
    reduced_data_empty,
    'Test  gold standard reducer with no extracts',
    add_version=False,
    processed_type='list',
    test_name='TestGoldStandardReducerEmpty'
)
