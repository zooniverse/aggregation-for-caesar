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
        },
        'level': 1
    }
}

reduced_data = {
    'alpha': {
        'BLIP': 6 / 8,
        'WHISTLE': 8 / 11
    },
    'level_up': True,
    'max_workflow_id': 2,
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
        },
        'level': 2
    }
}

TestGravitySpyUserReducer = RunningReducerTestNoProcessing(
    gravity_spy_user_reducer,
    extracted_data,
    reduced_data,
    'Test Gravity Spy User reducer',
    kwargs={
        'level_config': {
            1: {
                'workflow_id': 1,
                'new_categories': [
                    'BLIP',
                    'WHISTLE'
                ],
                'threshold': 0.7
            },
            2: {
                'workflow_id': 2
            }
        }
    },
    network_kwargs=kwargs_extra_data,
    test_name='TestGravitySpyUserReducer'
)

kwargs_extra_data_no_store = {
    'store': {}
}

reduced_data_no_store = {
    'alpha': {
        'BLIP': 1.0
    },
    'level_up': False,
    'max_workflow_id': 1,
    'normalized_confusion_matrix': {
        'BLIP': {
            'BLIP': 1.0
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
        },
        'level': 1
    }
}


TestGravitySpyUserReducerNoStore = RunningReducerTestNoProcessing(
    gravity_spy_user_reducer,
    extracted_data,
    reduced_data_no_store,
    'Test Gravity Spy User reducer with no store',
    kwargs={
        'level_config': {
            1: {
                'workflow_id': 1,
                'new_categories': [
                    'BLIP',
                    'WHISTLE'
                ],
                'threshold': 0.7
            },
            2: {
                'workflow_id': 2
            }
        }
    },
    network_kwargs=kwargs_extra_data_no_store,
    test_name='TestGravitySpyUserReducerNoStore'
)
