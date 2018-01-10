from collections import Counter
from panoptes_aggregation.reducers.survey_reducer import process_data, survey_reducer
from .base_test_class import ReducerTestSurvey

extracted_data = [
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'grooming': 1.0}, 'choice': 'raccoon'},
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'standing': 1.0}, 'choice': 'raccoon'},
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'standing': 1.0}, 'answers_clickwowifthisasanespeciallyawesomephoto': {'wow': 1.0}, 'choice': 'raccoon'},
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'standing': 1.0}, 'choice': 'raccoon'},
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'interacting': 1.0, 'grooming': 1.0}, 'answers_clickwowifthisasanespeciallyawesomephoto': {'wow': 1.0}, 'choice': 'blackbear'},
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'standing': 1.0}, 'choice': 'blackbear'},
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'standing': 1.0}, 'answers_clickwowifthisasanespeciallyawesomephoto': {'wow': 1.0}, 'choice': 'blackbear'},
    {'answers_howmanyanimalsdoyousee': {'1': 1.0}, 'answers_whatistheanimalsdoing': {'grooming': 1.0}, 'choice': 'blackbear'}
]

processed_data = {
    'blackbear': [
        {
            'answers_clickwowifthisasanespeciallyawesomephoto': Counter({'wow': 1}),
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'interacting': 1, 'grooming': 1})
        },
        {
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'standing': 1})
        },
        {
            'answers_clickwowifthisasanespeciallyawesomephoto': Counter({'wow': 1}),
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'standing': 1})
        },
        {
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'grooming': 1})
        }
    ],
    'raccoon': [
        {
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'grooming': 1})
        },
        {
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'standing': 1})
        },
        {
            'answers_clickwowifthisasanespeciallyawesomephoto': Counter({'wow': 1}),
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'standing': 1})
        },
        {
            'answers_howmanyanimalsdoyousee': Counter({'1': 1}),
            'answers_whatistheanimalsdoing': Counter({'standing': 1})
        }
    ]
}

reduced_data = [
    {
        'choice': 'raccoon',
        'total_vote_count': 8,
        'choice_count': 4,
        'answers_howmanyanimalsdoyousee': {
            '1': 4
        },
        'answers_whatistheanimalsdoing': {
            'standing': 3,
            'grooming': 1
        },
        'answers_clickwowifthisasanespeciallyawesomephoto': {
            'wow': 1
        }
    },
    {
        'choice': 'blackbear',
        'total_vote_count': 8,
        'choice_count': 4,
        'answers_howmanyanimalsdoyousee': {
            '1': 4
        },
        'answers_whatistheanimalsdoing': {
            'standing': 2,
            'grooming': 2,
            'interacting': 1
        },
        'answers_clickwowifthisasanespeciallyawesomephoto': {
            'wow': 2
        }
    }
]

TestSurvey = ReducerTestSurvey(
    survey_reducer,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test survey reducer'
)
