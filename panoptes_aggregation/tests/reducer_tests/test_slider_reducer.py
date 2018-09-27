from panoptes_aggregation.reducers.slider_reducer import process_data, slider_reducer
from .base_test_class import ReducerTest

extracted_data = [
    {'slider_value': 1},
    {'slider_value': 2},
    {'slider_value': 3},
    {'slider_value': 4}
]

processed_data = [
    1,
    2,
    3,
    4
]

reduced_data = {
    'slider_mean': 2.5,
    'slider_median': 2.5,
    'slider_var': 1.25
}

TestSliderReducer = ReducerTest(
    slider_reducer,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test slider reducer',
    processed_type='list'
)
