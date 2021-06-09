from panoptes_aggregation.reducers.question_consensus_reducer import question_consensus_reducer
from .base_test_class import ReducerTestNoProcessing

extracted_data = [
    {'a': 1, 'b': 1},
    {'a': 1},
    {'b': 1, 'c': 1},
    {'b': 1, 'a': 1}
]

reduced_data = {
    "most_likely": 'a',
    "num_votes": 3,
    "agreement": 3 / 7
}

TestQuestionReducer = ReducerTestNoProcessing(
    question_consensus_reducer,
    extracted_data,
    reduced_data,
    'Test question reducer',
    test_name='TestQuestionConsensusReducer'
)

reduced_data_pairs = {
    "most_likely": 'a+b',
    "num_votes": 2,
    "agreement": 2 / 4
}

TestQuestionReducerPairs = ReducerTestNoProcessing(
    question_consensus_reducer,
    extracted_data,
    reduced_data_pairs,
    'Test question consensus reducer as pairs',
    kwargs={'pairs': True},
    test_name='TestQuestionConsensusReducerPairs'
)
