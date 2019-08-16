from panoptes_aggregation.reducers.text_reducer import process_data, text_reducer
from .base_test_class import ReducerTest

extracted_data = [
    {'text': 'this is some test text'},
    {'text': 'this is some text text'},
    {'text': 'this is some test text'},
    {'text': ''},
    {'text': '     '}
]

processed_data = [
    'this is some test text',
    'this is some text text',
    'this is some test text'
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
    'consensus_score': 2.8
}

TestTextReducer = ReducerTest(
    text_reducer,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test text reducer',
    processed_type='list'
)

extracted_data_blank = [
    {'text': ''},
    {'text': ' '},
    {'text': '   '},
]

processed_data_blank = []
reduced_data_blank = {}

TextBalnkTextReducer = ReducerTest(
    text_reducer,
    process_data,
    extracted_data_blank,
    processed_data_blank,
    reduced_data_blank,
    'Test text reducer all extracts balnk',
    processed_type='list'
)
