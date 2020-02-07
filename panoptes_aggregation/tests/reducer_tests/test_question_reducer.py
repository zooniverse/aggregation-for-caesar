from panoptes_aggregation.reducers.question_reducer import question_reducer
from .base_test_class import ReducerTestNoProcessing

extracted_data = [
    {'a': 1, 'b': 1},
    {'a': 1},
    {'b': 1, 'c': 1},
    {'b': 1, 'a': 1}
]

reduced_data = {
    'a': 3,
    'b': 3,
    'c': 1
}

TestQuestionReducer = ReducerTestNoProcessing(
    question_reducer,
    extracted_data,
    reduced_data,
    'Test question reducer',
    test_name='TestQuestionReducer'
)

reduced_data_pairs = {
    'a+b': 2,
    'a': 1,
    'b+c': 1
}

TestQuestionReducerPairs = ReducerTestNoProcessing(
    question_reducer,
    extracted_data,
    reduced_data_pairs,
    'Test question reducer as pairs',
    kwargs={'pairs': True},
    test_name='TestQuestionReducerPairs'
)
