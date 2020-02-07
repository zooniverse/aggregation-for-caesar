from panoptes_aggregation.running_reducers.gravity_spy_user_reducer import gravity_spy_user_reducer
from .base_test_class import RunningReducerTestNoProcessing

extracted_data = [{
    'user_label': 'BLIP',
    'gold_label': 'BLIP'
}]

kwargs_extra_data = {
    'store': {
        'confusion_matrix': {
            'BLIP': {
                'BLIP': 5,
                'WHISTLE': 2
            },
            'WHISTLE': {
                'BLIP': 3,
                'WHISTLE': 8
            }
        },
        'column_normalization': {
            'BLIP': 7,
            'WHISTLE': 11
        }
    }
}

reduced_data = {
    'alpha': {
        'BLIP': 6 / 8,
        'WHISTLE': 8 / 11
    },
    'alpha_min': 8 / 11,
    'alpha_length': 2,
    'normalized_confusion_matrix': {
        'BLIP': {
            'BLIP': 6 / 8,
            'WHISTLE': 2 / 8
        },
        'WHISTLE': {
            'BLIP': 3 / 11,
            'WHISTLE': 8 / 11
        }
    },
    '_store': {
        'confusion_matrix': {
            'BLIP': {
                'BLIP': 6,
                'WHISTLE': 2
            },
            'WHISTLE': {
                'BLIP': 3,
                'WHISTLE': 8
            }
        },
        'column_normalization': {
            'BLIP': 8,
            'WHISTLE': 11
        }
    }
}

TestGravitySpyUserReducer = RunningReducerTestNoProcessing(
    gravity_spy_user_reducer,
    extracted_data,
    reduced_data,
    'Test Gravity Spy User reducer',
    network_kwargs=kwargs_extra_data,
    test_name='TestGravitySpyUserReducer'
)

kwargs_extra_data_no_store = {
    'store': {}
}

reduced_data_no_store = {
    'alpha': {
        'BLIP': 1
    },
    'alpha_min': 1.0,
    'alpha_length': 1,
    'normalized_confusion_matrix': {
        'BLIP': {
            'BLIP': 1
        }
    },
    '_store': {
        'confusion_matrix': {
            'BLIP': {
                'BLIP': 1
            }
        },
        'column_normalization': {
            'BLIP': 1
        }
    }
}


TestGravitySpyUserReducerNoStore = RunningReducerTestNoProcessing(
    gravity_spy_user_reducer,
    extracted_data,
    reduced_data_no_store,
    'Test Gravity Spy User reducer with no store',
    network_kwargs=kwargs_extra_data_no_store,
    test_name='TestGravitySpyUserReducerNoStore'
)
