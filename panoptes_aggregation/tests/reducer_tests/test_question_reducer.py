from collections import Counter
from panoptes_aggregation.reducers.question_reducer import process_data, question_reducer
from .base_test_class import ReducerTest

extracted_data = [
    {'a': 1, 'b': 1},
    {'a': 1},
    {'b': 1, 'c': 1},
    {'b': 1, 'a': 1}
]

processed_data = [
    Counter({'a': 1, 'b': 1}),
    Counter({'a': 1}),
    Counter({'b': 1, 'c': 1}),
    Counter({'b': 1, 'a': 1})
]

reduced_data = {
    'a': 3,
    'b': 3,
    'c': 1
}

TestQuestionReducer = ReducerTest(
    question_reducer,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test question reducer',
    processed_type='list'
)

processed_data_pairs = [
    Counter({'a+b': 1}),
    Counter({'a': 1}),
    Counter({'b+c': 1}),
    Counter({'a+b': 1})
]

reduced_data_pairs = {
    'a+b': 2,
    'a': 1,
    'b+c': 1
}

TestQuestionReducerPairs = ReducerTest(
    question_reducer,
    process_data,
    extracted_data,
    processed_data_pairs,
    reduced_data_pairs,
    'Test question reducer as pairs',
    pkwargs={'pairs': True},
    processed_type='list'
)
