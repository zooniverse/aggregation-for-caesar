from panoptes_aggregation.running_reducers.tess_gold_standard_reducer import tess_gold_standard_reducer_rr
from .base_test_class import RunningReducerTestNoProcessing


extracted_data = [{
    'feedback':
        [
            {'success': True},
            {'success': True},
            {'success': False},
            {'success': True}
        ]
}]

kwargs_extra_data = {
    'store': {
        'number_of_successes': [2, 2, 1, 3],
        'count': 3
    }
}

reduced_data = {
    'difficulty': [
        0.75,
        0.75,
        0.25,
        1.0
    ],
    '_store': {
        'number_of_successes': [3, 3, 1, 4],
        'count': 4
    }
}

TestTESSGoldStandardRunningReducer = RunningReducerTestNoProcessing(
    tess_gold_standard_reducer_rr,
    extracted_data,
    reduced_data,
    'Test TESS gold standard reducer in running mode',
    network_kwargs=kwargs_extra_data
)

kwargs_extra_data_no_store = {
    'store': {}
}

reduced_data_no_store = {
    'difficulty': [1, 1, 0, 1],
    '_store': {
        'number_of_successes': [1, 1, 0, 1],
        'count': 1
    }
}

TestTESSGoldStandardRunningReducerNoStore = RunningReducerTestNoProcessing(
    tess_gold_standard_reducer_rr,
    extracted_data,
    reduced_data_no_store,
    'Test TESS gold standard reducer in running mode with no store',
    network_kwargs=kwargs_extra_data_no_store
)

extracted_data_empty = []

reduced_data_empty = {
    'difficulty': [0.6666666666666666, 0.6666666666666666, 0.3333333333333333, 1.0],
    '_store': {
        'number_of_successes': [2, 2, 1, 3],
        'count': 3
    }
}

TestTESSGoldStandardRunningReducerEmptyExtract = RunningReducerTestNoProcessing(
    tess_gold_standard_reducer_rr,
    extracted_data_empty,
    reduced_data_empty,
    'Test TESS gold standard reducer in running mode with empty extract',
    network_kwargs=kwargs_extra_data
)

reduced_data_empty_no_store = {
    '_store': {}
}

TestTESSGoldStandardRunningReducerEmptyExtractNoStore = RunningReducerTestNoProcessing(
    tess_gold_standard_reducer_rr,
    extracted_data_empty,
    reduced_data_empty_no_store,
    'Test TESS gold standard reducer in running mode with empty extract and no store',
    network_kwargs=kwargs_extra_data_no_store
)
