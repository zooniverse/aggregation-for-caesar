from panoptes_aggregation import reducers
from .base_test_class import ReducerTestNoProcessing

extracted_data = [
    {'variants': ['a', 'b']},
    {},
    {'variants': ['c']}
]

reduced_data = {
    'variants': [
        'a',
        'b',
        'c'
    ]
}

TestSWVariantsReducer = ReducerTestNoProcessing(
    reducers.sw_variant_reducer,
    extracted_data,
    reduced_data,
    'Test SW variants reducer'
)
