from panoptes_aggregation.reducers.first_n_true_reducer import first_n_true_reducer
from .base_test_class import ReducerTestNoProcessing

extracted_data_first_three_true = [
    {"result": result} for result in [True, True, True, False, False]
]

extracted_data_three_true = [
    {"result": result} for result in [True, False, True, False, True]
]

extracted_data_first_two_true = [
    {"result": result} for result in [True, True, False, False, False]
]

reduced_true = {"result": True}
reduced_false = {"result": False}

FirstThreeTrueTestReducer = ReducerTestNoProcessing(
    first_n_true_reducer,
    extracted_data_first_three_true,
    reduced_true,
    "Test with first three extracts True",
    kwargs={"n": 3},
    test_name="FirstThreeTrueTestReducer",
)

ThreeTrueTestReducer = ReducerTestNoProcessing(
    first_n_true_reducer,
    extracted_data_three_true,
    reduced_false,
    "Test with any three extracts True",
    kwargs={"n": 3},
    test_name="ThreeTrueTestReducer",
)

FirstTwoTrueTestReducer = ReducerTestNoProcessing(
    first_n_true_reducer,
    extracted_data_first_two_true,
    reduced_false,
    "Test with first two extracts True",
    kwargs={"n": 3},
    test_name="FirstTwoTrueTestReducer",
)
