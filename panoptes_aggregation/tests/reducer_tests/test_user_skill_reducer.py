from panoptes_aggregation.reducers.user_skill_reducer import user_skill_reducer
from .base_test_class import ReducerTest
import numpy as np


def process(data):
    return data


extracted_data = [
    {
        "WILDEBEEST": 1,
        "ZEBRA": 1,
        "feedback": {
            "true_choiceIds": [
                "WILDEBEEST",
                "ZEBRA"
            ],
            "strategy": "surveySimple"
        },
    },
    {
        "WILDEBEEST": 1,
        "CHEETAH": 1,
        "feedback": {
            "true_choiceIds": [
                "WILDEBEEST",
                "ZEBRA"
            ],
            "strategy": "surveySimple"
        },
    }
]

kwargs_extra_data = {
    "relevant_reduction": [
        {
            "data": {
                "difficulty": [
                    1.0,
                    0.13043478260869565
                ]
            }
        },
        {
            "data": {
                "difficulty": [
                    1.0,
                    0.13043478260869565
                ]
            }
        }
    ]
}


reduced_data = {
    "classes": [
        "cheetah",
        "wildebeest",
        "zebra",
        "NONE"
    ],
    "confusion_simple": [
        [
            0,
            0,
            0,
            0
        ],
        [
            0,
            2,
            0,
            0
        ],
        [
            0,
            0,
            1,
            1
        ],
        [
            1,
            0,
            0,
            0
        ]
    ],
    "skill": {
        "cheetah": 0.0,
        "wildebeest": 1.0,
        "zebra": 0.5,
        "NONE": 0.0
    },
    "weighted_skill": {
        "cheetah": 0.0,
        "wildebeest": 0.9999999999999999,
        "zebra": 0.4347826086956522,
        "NONE": 0.0
    },
    "count": {
        "cheetah": 0,
        "wildebeest": 2,
        "zebra": 2,
        "NONE": 1
    },
    'mean_skill': 0.47826086956521735,
    'level_up': False
}


TestkClassUserSkillReducer = ReducerTest(
    user_skill_reducer,
    process,
    extracted_data,
    extracted_data,
    reduced_data,
    'Test k-class user skill reducer',
    network_kwargs=kwargs_extra_data,
    kwargs={'mode': 'many-to-many'},
    add_version=False,
    processed_type='list',
    test_name='TestkClassUserSkillReducer'
)


reduced_data_strategy_all = {
    "classes": [
        "cheetah",
        "wildebeest",
        "zebra",
        "NONE"
    ],
    "confusion_simple": [
        [
            0,
            0,
            0,
            0
        ],
        [
            0,
            2,
            0,
            0
        ],
        [
            0,
            0,
            1,
            1
        ],
        [
            1,
            0,
            0,
            0
        ]
    ],
    "skill": {
        "cheetah": 0.0,
        "wildebeest": 1.0,
        "zebra": 0.5,
        "NONE": 0.0
    },
    "weighted_skill": {
        "cheetah": 0.0,
        "wildebeest": 0.9999999999999999,
        "zebra": 0.4347826086956522,
        "NONE": 0.0
    },
    "count": {
        "cheetah": 0,
        "wildebeest": 2,
        "zebra": 2,
        "NONE": 1
    },
    'mean_skill': 0.47826086956521735,
    'level_up': False
}


TestkClassUserSkillReducerStrategyAll = ReducerTest(
    user_skill_reducer,
    process,
    extracted_data,
    extracted_data,
    reduced_data,
    'Test k-class user skill reducer',
    network_kwargs=kwargs_extra_data,
    add_version=False,
    kwargs={'mode': 'many-to-many', 'strategy': 'all', 'skill_threshold': 0.5, 'count_threshold': 1},
    processed_type='list',
    test_name='TestkClassUserSkillReducer'
)

extracted_data = [
    {
        "frame0.T1_tool0_x": [
            7.007341202533306,
            15.085714457468555,
            23.197817872132134
        ],
        "frame0.T1_tool0_width": [
            0.3710317570116386,
            0.4722222361966306,
            0.43849207646830024
        ],
        "feedback": {
            "strategy": "graph2drange",
            "success": [
                True,
                True,
                True
            ],
            "true_x": [
                23.143580364475866,
                15.054503464475864,
                6.965426564475864
            ],
            "true_width": [
                0.3,
                0.3,
                0.3
            ]
        },
    },
    {
        "frame0.T1_tool0_x": [
            1.0201915505666743,
            7.546677964132965,
            20.683972321156585,
            27.345373182548535
        ],
        "frame0.T1_tool0_width": [
            0.40474334347697927,
            0.43847195543339446,
            0.33728611956414767,
            0.4384719554333891
        ],
        "feedback": {
            "strategy": "graph2drange",
            "success": [
                True,
                True,
                True,
                True
            ],
            "true_x": [
                27.29064002867498,
                20.71495532867498,
                7.5635859286749785,
                0.9879012286749784
            ],
            "true_width": [
                0.3,
                0.3,
                0.3,
                0.3
            ]
        },
    },
    {
        "frame0.T1_tool0_x": [
            6.702486768179421,
            19.95589913093957
        ],
        "frame0.T1_tool0_width": [
            0.43840804253405086,
            0.37096065137496126
        ],
        "feedback": {
            "strategy": "graph2drange",
            "success": [
                False,
                True,
                False,
                False,
                True,
                False
            ],
            "true_x": [
                24.38699889454371,
                19.956099794543707,
                15.525200694543706,
                11.094301594543705,
                6.663402494543703,
                2.232503394543703
            ],
            "true_width": [
                0.3,
                0.3,
                0.3,
                0.3,
                0.3,
                0.3
            ]
        }
    }
]

kwargs_extra_data = {
    "relevant_reduction": [
        {
            "data": {
                "difficulty": [
                    0.8333333333333334,
                    0.8333333333333334,
                    0.8333333333333334
                ]
            }
        },
        {
            "data": {
                "difficulty": [
                    0.8,
                    0.8,
                    0.8,
                    0.8
                ]
            }
        },
        {
            "data": {
                "difficulty": [
                    0.0,
                    0.8571428571428571,
                    0.14285714285714285,
                    0.0,
                    0.8571428571428571,
                    0.0
                ]
            }
        }
    ],
}


reduced_data = {
    "skill": {
        "True": 0.6923076923076923,
        "False": 0.0
    },
    "weighted_skill": {
        "True": 0.844106463878327,
        "False": 0.0
    },
    "count": {
        "True": 13.0,
        "False": 0.0
    },
    "classes": [
        "True",
        "False"
    ],
    "confusion_simple": np.asarray([
        [
            9.0, 4.0
        ],
        [
            0.0, 0.0
        ]
    ]).tolist(),
    'mean_skill': 0.844106463878327,
    'level_up': True
}

TestBinaryUserSkillReducer = ReducerTest(
    user_skill_reducer,
    process,
    extracted_data,
    extracted_data,
    reduced_data,
    'Test binary user skill reducer',
    network_kwargs=kwargs_extra_data,
    kwargs={'mode': 'binary'},
    add_version=False,
    processed_type='list',
    test_name='TestBinaryUserSkillReducer'
)


extracted_data = [
    {
        "BLIP": 1,
        "feedback": {
            "true_choiceIds": [
                "BLIP",
            ],
            "strategy": "surveySimple"
        },
    },
    {
        "WHISTLE": 1,
        "feedback": {
            "true_choiceIds": [
                "WHISTLE",
            ],
            "strategy": "surveySimple"
        },
    },
    {
        "NONEOFTHEABOVE": 1,
        "feedback": {
            "true_choiceIds": [
                "CHIRP",
            ],
            "strategy": "surveySimple"
        },
    }
]

kwargs_extra_data = {
    "relevant_reduction": [
        {
            "data": {
                "difficulty": [
                    1
                ]
            }
        },
        {
            "data": {
                "difficulty": [
                    0.5,
                ]
            }
        },
        {
            "data": {
                "difficulty": [
                    0.99,
                ]
            }
        }
    ]
}

reduced_data = {
    "classes": [
        "blip",
        "chirp",
        "noneoftheabove",
        "whistle"
    ],
    "confusion_simple": [
        [
            1,
            0,
            0,
            0
        ],
        [
            0,
            0,
            1,
            0
        ],
        [
            0,
            0,
            0,
            0
        ],
        [
            0,
            0,
            0,
            1
        ]
    ],
    "count": {
        "blip": 1,
        "chirp": 1,
        "noneoftheabove": 0,
        "whistle": 1
    },
    "level_up": False,
    "mean_skill": 0.49999999999999944,
    "skill": {
        "blip": 1.0,
        "chirp": 0.0,
        "noneoftheabove": 0.0,
        "whistle": 1.0
    },
    "weighted_skill": {
        "blip": 0.9999999999999981,
        "chirp": 0.0,
        "noneoftheabove": 0.0,
        "whistle": 0.9999999999999998
    }
}

TestOneToOneUserSkillReducer = ReducerTest(
    user_skill_reducer,
    process,
    extracted_data,
    extracted_data,
    reduced_data,
    'Test one-to-one user skill reducer',
    network_kwargs=kwargs_extra_data,
    kwargs={'mode': 'one-to-one'},
    add_version=False,
    processed_type='list',
    test_name='TestOneToOneUserSkillReducer'
)


extracted_data = [
    {
        "1": 1,
        "feedback": {
            "strategy": "singleAnswerQuestion",
            "true_answer": [
                "1"
            ],
            "agreement_score": 1
        },
        "aggregation_version": "4.1.0"
    },
    {
        "7": 1,
        "aggregation_version": "4.1.0"
    },
    {
        "1": 1,
        "feedback": {
            "strategy": "singleAnswerQuestion",
            "true_answer": [
                "2"
            ],
            "agreement_score": 0
        },
        "aggregation_version": "4.1.0"
    },
    {
        "1": 1,
        "aggregation_version": "4.1.0"
    },
    {
        "1": 1,
        "feedback": {
            "strategy": "singleAnswerQuestion",
            "true_answer": [
                "1"
            ],
            "agreement_score": 1
        },
        "aggregation_version": "4.1.0"
    }
]

kwargs_extra_data = {
    "relevant_reduction": [
        {
            "data": {
                "difficulty": [
                    1
                ],
                "aggregation_version": "4.1.0"
            }
        },
        {
            "data": {
                "aggregation_version": "4.1.0"
            }
        },
        {
            "data": {
                "difficulty": [
                    0
                ],
                "aggregation_version": "4.1.0"
            }
        },
        {
            "data": {
                "aggregation_version": "4.1.0"
            }
        },
        {
            "data": {
                "difficulty": [
                    1
                ],
                "aggregation_version": "4.1.0"
            }
        }
    ]
}


reduced_data = {
    "classes": [
        "1",
        "2"
    ],
    "confusion_simple": [
        [
            2,
            0
        ],
        [
            1,
            0
        ]
    ],
    "weighted_skill": {
        "1": 0.999999999999999,
        "2": 0.0
    },
    "skill": {
        "1": 1.0,
        "2": 0.0
    },
    "count": {
        "1": 2,
        "2": 1
    },
    "mean_skill": 0.999999999999999,
    "level_up": True
}

TestSubclassUserSkillReducer = ReducerTest(
    user_skill_reducer,
    process,
    extracted_data,
    extracted_data,
    reduced_data,
    'Test user skill reducer with class subsetting',
    network_kwargs=kwargs_extra_data,
    kwargs={'mode': 'one-to-one', 'strategy': 'all', 'skill_threshold': 0.2, 'count_threshold': 1, 'focus_classes': ["1"]},
    add_version=False,
    processed_type='list',
    test_name='TestUserSkillReducer_SubsetClass'
)
