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
            1
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
            0
        ],
        [
            0,
            0,
            1,
            0
        ]
    ],
    "skill": [
        0.0,
        1.0,
        0.5,
        0.0
    ],
    "weighted_skill": [
        0.0,
        0.9999999999999999,
        0.4347826086956522,
        0.0
    ]
}


TestkClassUserSkillReducer = ReducerTest(
    user_skill_reducer,
    process,
    extracted_data,
    extracted_data,
    reduced_data,
    'Test k-class user skill reducer',
    network_kwargs=kwargs_extra_data,
    add_version=False,
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
    "skill": np.asarray([
        0.6923076923076923, 0
    ]).tolist(),
    "weighted_skill": np.asarray([
        0.844106463878327, 0
    ]).tolist(),
    "classes": [
        "True",
        "False"
    ],
    "confusion_simple": np.asarray([
        [
            9.0, 0
        ],
        [
            4.0, 0
        ]
    ]).tolist(),
}

TestBinaryUserSkillReducer = ReducerTest(
    user_skill_reducer,
    process,
    extracted_data,
    extracted_data,
    reduced_data,
    'Test binary user skill reducer',
    network_kwargs=kwargs_extra_data,
    kwargs={'binary': True},
    add_version=False,
    processed_type='list',
    test_name='TestBinaryUserSkillReducer'
)
