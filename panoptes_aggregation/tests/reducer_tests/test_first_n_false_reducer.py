from panoptes_aggregation.reducers.first_n_false_reducer import first_n_false_reducer
from .base_test_class import ReducerTestNoProcessing

extracted_data_first_three_false = [
    {"result": result} for result in [False, False, False, True, True]
]

extracted_data_three_false = [
    {"result": result} for result in [False, True, False, True, False]
]

extracted_data_first_two_false = [
    {"result": result} for result in [False, False, True, True, True]
]

reduced_true = {"result": True}
reduced_false = {"result": False}

FirstThreeTrueTestReducer = ReducerTestNoProcessing(
    first_n_false_reducer,
    extracted_data_first_three_false,
    reduced_true,
    "Test with first three extracts False",
    kwargs={"n": 3},
    test_name="FirstThreeTrueTestReducer",
)

ThreeTrueTestReducer = ReducerTestNoProcessing(
    first_n_false_reducer,
    extracted_data_three_false,
    reduced_false,
    "Test with any three extracts False",
    kwargs={"n": 3},
    test_name="ThreeTrueTestReducer",
)

FirstTwoTrueTestReducer = ReducerTestNoProcessing(
    first_n_false_reducer,
    extracted_data_first_two_false,
    reduced_false,
    "Test with first two extracts False",
    kwargs={"n": 3},
    test_name="FirstTwoTrueTestReducer",
)
