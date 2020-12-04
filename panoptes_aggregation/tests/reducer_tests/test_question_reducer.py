from panoptes_aggregation.reducers.question_reducer import question_reducer
from .base_test_class import ReducerTestNoProcessing

extracted_data = [
    {'a': 1, 'b': 1},
    {'a': 1},
    {'b': 1, 'c': 1},
    {'b': 1, 'a': 1}
]

kwargs_extra_data = {
    'user_id': [
        1,
        2,
        None,
        4
    ]
}

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
    test_name='TestQuestionReducer',
    network_kwargs=kwargs_extra_data
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
    test_name='TestQuestionReducerPairs',
    network_kwargs=kwargs_extra_data
)

reduced_data_users = {
    'a': 3,
    'b': 3,
    'c': 1,
    'user_ids_a': [1, 2, 4],
    'user_ids_b': [1, None, 4],
    'user_ids_c': [None]
}

TestQuestionReducerUsers = ReducerTestNoProcessing(
    question_reducer,
    extracted_data,
    reduced_data_users,
    'Test question reducer tracking users IDs',
    kwargs={'track_user_ids': True},
    test_name='TestQuestionReducerUsers',
    network_kwargs=kwargs_extra_data
)

reduced_data_pairs_users = {
    'a+b': 2,
    'a': 1,
    'b+c': 1,
    'user_ids_a+b': [1, 4],
    'user_ids_a': [2],
    'user_ids_b+c': [None]
}

TestQuestionReducerPairsUsers = ReducerTestNoProcessing(
    question_reducer,
    extracted_data,
    reduced_data_pairs_users,
    'Test question reducer as pairs and tracking users IDs',
    kwargs={
        'pairs': True,
        'track_user_ids': True
    },
    test_name='TestQuestionReducerPairsUsers',
    network_kwargs=kwargs_extra_data
)
