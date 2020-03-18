from panoptes_aggregation.reducers.text_reducer import process_data, text_reducer
from .base_test_class import ReducerTest

extracted_data = [
    {
        'text': 'this is some test text',
        'gold_standard': True
    },
    {
        'text': 'this is some text text'
    },
    {
        'text': 'this is some test text',
        'gold_standard': False
    },
    {
        'text': ''
    },
    {
        'text': '     ',
        'gold_standard': False
    }
]

kwargs_extra_data = {
    'user_id': [
        1,
        2,
        None,
        4,
        5
    ]
}

processed_data = [
    [0, 'this is some test text', True],
    [1, 'this is some text text', False],
    [2, 'this is some test text', False]
]

reduced_data = {
    'aligned_text': [
        ['this', 'this', 'this'],
        ['is', 'is', 'is'],
        ['some', 'some', 'some'],
        ['test', 'text', 'test'],
        ['text', 'text', 'text']
    ],
    'number_views': 3,
    'consensus_score': 2.8,
    'consensus_text': 'this is some test text',
    'gold_standard': [True, False, False],
    'user_ids': [1, 2, None]
}

TestTextReducer = ReducerTest(
    text_reducer,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test text reducer',
    network_kwargs=kwargs_extra_data,
    processed_type='list',
    test_name='TestTextReducer'
)

extracted_data_blank = [
    {'text': ''},
    {'text': ' '},
    {'text': '   '},
]

processed_data_blank = []
reduced_data_blank = {}

kwargs_extra_data_blank = {
    'user_id': [
        1,
        2,
        3
    ]
}

TextBlankTextReducer = ReducerTest(
    text_reducer,
    process_data,
    extracted_data_blank,
    processed_data_blank,
    reduced_data_blank,
    'Test text reducer all extracts blank',
    network_kwargs=kwargs_extra_data_blank,
    processed_type='list',
    test_name='TextBlankTextReducer'
)

extracted_data_no_text = [
    {'gold_standard': False}
]

processed_data_no_text = []
reduced_data_no_text = {}

kwargs_extra_data_no_text = {
    'user_id': [
        1
    ]
}

TextNoTextReducer = ReducerTest(
    text_reducer,
    process_data,
    extracted_data_no_text,
    processed_data_no_text,
    reduced_data_no_text,
    'Test text reducer no text passed in',
    network_kwargs=kwargs_extra_data_no_text,
    processed_type='list',
    test_name='TextNoTextReducer'
)
