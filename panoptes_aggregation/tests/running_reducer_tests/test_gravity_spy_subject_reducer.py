from panoptes_aggregation.running_reducers.gravity_spy_subject_reducer import gravity_spy_subject_reducer
from .base_test_class import RunningReducerTestNoProcessing

extracted_data = [{
    'user_label': 'BLIP',
    'ml_weights': {
        'BLIP': 0.1,
        'WHISTLE': 0.9
    }
}]

kwargs_extra_data = {
    'relevant_reduction': [
        {'data': {
            'alpha': {
                'BLIP': 0.75,
                'WHISTLE': 8 / 11
            },
            'alpha_min': 8 / 11,
            'alpha_length': 2,
            'normalized_confusion_matrix': {
                'BLIP': {
                    'BLIP': 0.75,
                    'WHISTLE': 0.25
                },
                'WHISTLE': {
                    'BLIP': 3 / 11,
                    'WHISTLE': 8 / 11
                }
            }
        }}
    ],
    'store': {
        'number_views': 3,
        'category_weights_sum': {
            'BLIP': 2.4,
            'WHISTLE': 0.6
        }
    }
}

reduced_data = {
    'number_views': 4,
    'category_weights': {
        'BLIP': 0.7875,
        'WHISTLE': 0.2125
    },
    'max_category_weight': 0.7875,
    '_store': {
        'number_views': 4,
        'category_weights_sum': {
            'BLIP': 3.15,
            'WHISTLE': 0.85
        }
    }
}

TestGravitySpySubjectReducer = RunningReducerTestNoProcessing(
    gravity_spy_subject_reducer,
    extracted_data,
    reduced_data,
    'Test Gravity Spy Subject reducer',
    network_kwargs=kwargs_extra_data
)

kwargs_extra_data_no_store = {
    'relevant_reduction': [
        {'data': {
            'alpha': {
                'BLIP': 0.75,
                'WHISTLE': 8 / 11
            },
            'alpha_min': 8 / 11,
            'alpha_length': 2,
            'normalized_confusion_matrix': {
                'BLIP': {
                    'BLIP': 0.75,
                    'WHISTLE': 0.25
                },
                'WHISTLE': {
                    'BLIP': 3 / 11,
                    'WHISTLE': 8 / 11
                }
            }
        }}
    ],
    'store': {}
}

reduced_data_no_store = {
    'number_views': 2,
    'category_weights': {
        'BLIP': 0.425,
        'WHISTLE': 0.575
    },
    'max_category_weight': 0.575,
    '_store': {
        'number_views': 2,
        'category_weights_sum': {
            'BLIP': 0.85,
            'WHISTLE': 1.15
        }
    }
}

TestGravitySpySubjectReducerNoStore = RunningReducerTestNoProcessing(
    gravity_spy_subject_reducer,
    extracted_data,
    reduced_data_no_store,
    'Test Gravity Spy Subject reducer no store',
    network_kwargs=kwargs_extra_data_no_store
)

kwargs_extra_data_no_rr = {
    'relevant_reduction': [
        None
    ],
    'store': {}
}

reduced_data_no_rr = {
    'number_views': 1,
    'category_weights': {
        'BLIP': 0.1,
        'WHISTLE': 0.9
    },
    'max_category_weight': 0.9,
    '_store': {
        'number_views': 1,
        'category_weights_sum': {
            'BLIP': 0.1,
            'WHISTLE': 0.9
        }
    }
}

TestGravitySpySubjectReducerNoRR = RunningReducerTestNoProcessing(
    gravity_spy_subject_reducer,
    extracted_data,
    reduced_data_no_rr,
    'Test Gravity Spy Subject reducer no confusion matrix',
    network_kwargs=kwargs_extra_data_no_rr
)

kwargs_extra_data_no_column = {
    'relevant_reduction': [
        {'data': {
            'alpha': {
                'WHISTLE': 8 / 11
            },
            'alpha_min': 8 / 11,
            'alpha_length': 1,
            'normalized_confusion_matrix': {
                'WHISTLE': {
                    'BLIP': 3 / 11,
                    'WHISTLE': 8 / 11
                }
            }
        }}
    ],
    'store': {
        'number_views': 1,
        'category_weights_sum': {
            'BLIP': 0.1,
            'WHISTLE': 0.9
        }
    }
}

reduced_data_no_column = {
    'number_views': 1,
    'category_weights': {
        'BLIP': 0.1,
        'WHISTLE': 0.9
    },
    'max_category_weight': 0.9,
    '_store': {
        'number_views': 1,
        'category_weights_sum': {
            'BLIP': 0.1,
            'WHISTLE': 0.9
        }
    }
}

TestGravitySpySubjectReducerNoColumn = RunningReducerTestNoProcessing(
    gravity_spy_subject_reducer,
    extracted_data,
    reduced_data_no_column,
    'Test Gravity Spy Subject reducer no confusion matrix',
    network_kwargs=kwargs_extra_data_no_column
)
