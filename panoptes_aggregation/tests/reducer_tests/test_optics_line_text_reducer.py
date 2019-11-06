from panoptes_aggregation.reducers.optics_line_text_reducer import process_data, optics_line_text_reducer
from .base_test_class import ReducerTest

extracted_data = [
    {
        'frame0': {
            'points': {
                'x': [
                    [27.765213012695312, 984.8629150390625],
                    [111.51124572753906, 578.0963134765625],
                    [30.157958984375, 989.6483154296875],
                    [243.1121826171875, 733.624755859375],
                    [1149.962158203125, 2152.52197265625],
                    [1118.8565673828125, 1599.798095703125],
                    [1245.6719970703125, 1760.1119384765625],
                    [1346.167236328125, 1796.0030517578125]
                ],
                'y': [
                    [419.1290588378906, 397.5943298339844],
                    [533.980712890625, 131.99972534179688],
                    [313.8482971191406, 285.1353454589844],
                    [541.158935546875, 122.42880249023438],
                    [297.0990905761719, 273.1716613769531],
                    [376.0596618652344, 373.6669006347656],
                    [498.0895690917969, 69.78839111328125],
                    [533.980712890625, 158.31991577148438]
                ]
            },
            'text': [
                ['words on a page.'],
                ['There is this'],
                ['Here are some test'],
                ['text as well'],
                ['There are two columns'],
                ['of text.'],
                ['This looks like'],
                ['a big mess']
            ],
            'slope': [
                -1.3125665780470608,
                -40.966719469829826,
                -1.4137500414163335,
                -40.33550980324749,
                -1.252950483811786,
                -0.23999309197815955,
                -40.103966913878772,
                -39.504439692518773
            ],
            'gold_standard': False
        }
    },
    {
        'frame0': {
            'points': {
                'x': [
                    [32.550689697265625, 984.8629150390625],
                    [30.157958984375, 992.0411376953125],
                    [1243.2791748046875, 1755.326416015625],
                    [1346.167236328125, 1798.3958740234375],
                    [1128.427490234375, 2142.950927734375],
                    [1114.071044921875, 1587.8343505859375],
                    [104.33302307128906, 563.7398681640625],
                    [245.50491333007812, 731.23193359375]
                ],
                'y': [
                    [285.1353454589844, 268.3861389160156],
                    [402.3798522949219, 395.2015686035156],
                    [481.3403625488281, 45.8609619140625],
                    [526.802490234375, 148.74893188476562],
                    [282.7426452636719, 270.7789001464844],
                    [399.9870910644531, 380.8451232910156],
                    [536.37353515625, 148.74893188476562],
                    [543.5517578125, 129.60702514648438]
                ]
            },
            'text': [
                ['Here are some test'],
                ['words on a page.'],
                ['This looks like'],
                ['a big mess'],
                ['There are two columns'],
                ['of text.'],
                ['There is this'],
                ['test as well']
            ],
            'slope': [
                -0.84300379948873472,
                -0.41169221645914822,
                -40.611219258654081,
                -39.867717105940628,
                -0.77370202671330712,
                -1.9350479072142399,
                -40.214619322353997,
                -40.655937635767046
            ],
            'gold_standard': True
        },
        'frame1': {
            'points': {'x': [[1, 250]], 'y': [[1, 1]]},
            'text': [['page 2']],
            'slope': [0],
            'gold_standard': True
        }
    },
    {
        'frame0': {
            'points': {
                'x': [
                    [1248.064697265625, 1762.504638671875],
                    [1346.167236328125, 1800.78857421875],
                    [37.336181640625, 977.6846923828125],
                    [39.72892761230469, 1013.5758056640625],
                    [106.72576904296875, 597.23828125],
                    [1145.1767578125, 1587.8343505859375],
                    [247.89767456054688, 759.9449462890625],
                    [1137.99853515625, 2162.093017578125]
                ],
                'y': [
                    [483.7331237792969, 67.39566040039062],
                    [526.802490234375, 155.92721557617188],
                    [399.9870910644531, 392.8088684082031],
                    [297.0990905761719, 280.3498840332031],
                    [545.9444580078125, 127.21426391601562],
                    [390.4161071777344, 373.6669006347656],
                    [548.337158203125, 127.21426391601562],
                    [287.5281066894531, 268.3861389160156]
                ]
            },
            'text': [
                ['This looks like'],
                ['a big mess'],
                ['words on a page.'],
                ['Here are some test'],
                ['There is this'],
                ['of text.'],
                ['text as well'],
                ['There are two columns']
            ],
            'slope': [
                -39.504825159192279,
                -39.180903129348373,
                -0.61606969523056521,
                -0.69199657727551112,
                -40.728595229744641,
                -1.8257636189450075,
                -39.334667288762937,
                -1.122924085203026
            ],
            'gold_standard': False
        },
        'frame1': {
            'points': {'x': [[1.1, 251]], 'y': [[0.9, 0.9]]},
            'text': [['page 2']],
            'slope': [0],
            'gold_standard': False
        }
    },
    {
        'frame0': {
            'points': {'x': [[1000, 10]], 'y': [[700, 10]]},
            'text': [['not in a cluster']],
            'slope': [-145.12467165539783],
            'gold_standard': False
        },
        'frame2': {
            'points': {'x': [[1, 250]], 'y': [[1, 1]]},
            'text': [['some words']],
            'slope': [0],
            'gold_standard': False
        }
    },
    {}
]

kwargs_extra_data = {
    'user_id': [
        1,
        2,
        3,
        4,
        5
    ]
}

processed_data = {
    'frame0': {
        'X': [
            [0, 0],
            [1, 0],
            [2, 0],
            [3, 0],
            [4, 0],
            [5, 0],
            [6, 0],
            [7, 0],
            [8, 1],
            [9, 1],
            [10, 1],
            [11, 1],
            [12, 1],
            [13, 1],
            [14, 1],
            [15, 1],
            [16, 2],
            [17, 2],
            [18, 2],
            [19, 2],
            [20, 2],
            [21, 2],
            [22, 2],
            [23, 2],
            [24, 3]
        ],
        'data': [
            {'x': [27.765213012695312, 984.8629150390625], 'y': [419.1290588378906, 397.5943298339844], 'text': ['words on a page.'], 'gold_standard': False},
            {'x': [111.51124572753906, 578.0963134765625], 'y': [533.980712890625, 131.99972534179688], 'text': ['There is this'], 'gold_standard': False},
            {'x': [30.157958984375, 989.6483154296875], 'y': [313.8482971191406, 285.1353454589844], 'text': ['Here are some test'], 'gold_standard': False},
            {'x': [243.1121826171875, 733.624755859375], 'y': [541.158935546875, 122.42880249023438], 'text': ['text as well'], 'gold_standard': False},
            {'x': [1149.962158203125, 2152.52197265625], 'y': [297.0990905761719, 273.1716613769531], 'text': ['There are two columns'], 'gold_standard': False},
            {'x': [1118.8565673828125, 1599.798095703125], 'y': [376.0596618652344, 373.6669006347656], 'text': ['of text.'], 'gold_standard': False},
            {'x': [1245.6719970703125, 1760.1119384765625], 'y': [498.0895690917969, 69.78839111328125], 'text': ['This looks like'], 'gold_standard': False},
            {'x': [1346.167236328125, 1796.0030517578125], 'y': [533.980712890625, 158.31991577148438], 'text': ['a big mess'], 'gold_standard': False},
            {'x': [32.550689697265625, 984.8629150390625], 'y': [285.1353454589844, 268.3861389160156], 'text': ['Here are some test'], 'gold_standard': True},
            {'x': [30.157958984375, 992.0411376953125], 'y': [402.3798522949219, 395.2015686035156], 'text': ['words on a page.'], 'gold_standard': True},
            {'x': [1243.2791748046875, 1755.326416015625], 'y': [481.3403625488281, 45.8609619140625], 'text': ['This looks like'], 'gold_standard': True},
            {'x': [1346.167236328125, 1798.3958740234375], 'y': [526.802490234375, 148.74893188476562], 'text': ['a big mess'], 'gold_standard': True},
            {'x': [1128.427490234375, 2142.950927734375], 'y': [282.7426452636719, 270.7789001464844], 'text': ['There are two columns'], 'gold_standard': True},
            {'x': [1114.071044921875, 1587.8343505859375], 'y': [399.9870910644531, 380.8451232910156], 'text': ['of text.'], 'gold_standard': True},
            {'x': [104.33302307128906, 563.7398681640625], 'y': [536.37353515625, 148.74893188476562], 'text': ['There is this'], 'gold_standard': True},
            {'x': [245.50491333007812, 731.23193359375], 'y': [543.5517578125, 129.60702514648438], 'text': ['test as well'], 'gold_standard': True},
            {'x': [1248.064697265625, 1762.504638671875], 'y': [483.7331237792969, 67.39566040039062], 'text': ['This looks like'], 'gold_standard': False},
            {'x': [1346.167236328125, 1800.78857421875], 'y': [526.802490234375, 155.92721557617188], 'text': ['a big mess'], 'gold_standard': False},
            {'x': [37.336181640625, 977.6846923828125], 'y': [399.9870910644531, 392.8088684082031], 'text': ['words on a page.'], 'gold_standard': False},
            {'x': [39.72892761230469, 1013.5758056640625], 'y': [297.0990905761719, 280.3498840332031], 'text': ['Here are some test'], 'gold_standard': False},
            {'x': [106.72576904296875, 597.23828125], 'y': [545.9444580078125, 127.21426391601562], 'text': ['There is this'], 'gold_standard': False},
            {'x': [1145.1767578125, 1587.8343505859375], 'y': [390.4161071777344, 373.6669006347656], 'text': ['of text.'], 'gold_standard': False},
            {'x': [247.89767456054688, 759.9449462890625], 'y': [548.337158203125, 127.21426391601562], 'text': ['text as well'], 'gold_standard': False},
            {'x': [1137.99853515625, 2162.093017578125], 'y': [287.5281066894531, 268.3861389160156], 'text': ['There are two columns'], 'gold_standard': False},
            {'x': [1000, 10], 'y': [700, 10], 'text': ['not in a cluster'], 'gold_standard': False}
        ]
    },
    'frame1': {
        'X': [
            [0, 1],
            [1, 2]
        ],
        'data': [
            {'x': [1, 250], 'y': [1, 1], 'text': ['page 2'], 'gold_standard': True},
            {'x': [1.1, 251], 'y': [0.9, 0.9], 'text': ['page 2'], 'gold_standard': False}
        ]
    },
    'frame2': {
        'X': [
            [0, 3]
        ],
        'data': [
            {'x': [1, 250], 'y': [1, 1], 'text': ['some words'], 'gold_standard': False}
        ]
    }
}

reduced_data = {
    'frame0': [
        {
            'clusters_text': [
                ['Here', 'Here', 'Here'],
                ['are', 'are', 'are'],
                ['some', 'some', 'some'],
                ['test', 'test', 'test']
            ],
            'clusters_x': [32.550689697265625, 989.6483154296875],
            'clusters_y': [297.0990905761719, 280.3498840332031],
            'consensus_score': 3.0,
            'line_slope': 358.894,
            'number_views': 3,
            'user_ids': [1, 2, 3],
            'extract_index': [2, 0, 3],
            'gold_standard': [False, True, False],
            'slope_label': 0,
            'gutter_label': 0
        },
        {
            'clusters_text': [
                ['words', 'words', 'words'],
                ['on', 'on', 'on'],
                ['a', 'a', 'a'],
                ['page.', 'page.', 'page.']
            ],
            'clusters_x': [30.157958984375, 984.8629150390625],
            'clusters_y': [402.3798522949219, 395.2015686035156],
            'consensus_score': 3.0,
            'line_slope': 358.894,
            'number_views': 3,
            'user_ids': [1, 2, 3],
            'extract_index': [0, 1, 2],
            'gold_standard': [False, True, False],
            'slope_label': 0,
            'gutter_label': 0
        },
        {
            'clusters_text': [
                ['There', 'There', 'There'],
                ['are', 'are', 'are'],
                ['two', 'two', 'two'],
                ['columns', 'columns', 'columns']
            ],
            'clusters_x': [1137.99853515625, 2152.52197265625],
            'clusters_y': [287.5281066894531, 270.7789001464844],
            'consensus_score': 3.0,
            'line_slope': 358.894,
            'number_views': 3,
            'user_ids': [1, 2, 3],
            'extract_index': [4, 4, 7],
            'gold_standard': [False, True, False],
            'slope_label': 0,
            'gutter_label': 1
        },
        {
            'clusters_text': [
                ['of', 'of', 'of'],
                ['text.', 'text.', 'text.']
            ],
            'clusters_x': [1118.8565673828125, 1587.8343505859375],
            'clusters_y': [390.4161071777344, 373.6669006347656],
            'consensus_score': 3.0,
            'line_slope': 358.894,
            'number_views': 3,
            'user_ids': [1, 2, 3],
            'extract_index': [5, 5, 5],
            'gold_standard': [False, True, False],
            'slope_label': 0,
            'gutter_label': 1
        },
        {
            'clusters_text': [
                ['There', 'There', 'There'],
                ['is', 'is', 'is'],
                ['this', 'this', 'this']
            ],
            'clusters_x': [106.72576904296875, 578.0963134765625],
            'clusters_y': [536.37353515625, 131.99972534179688],
            'consensus_score': 3.0,
            'line_slope': 320.143,
            'number_views': 3,
            'user_ids': [1, 2, 3],
            'extract_index': [1, 6, 4],
            'gold_standard': [False, True, False],
            'slope_label': 1,
            'gutter_label': 0
        },
        {
            'clusters_text': [
                ['text', 'test', 'text'],
                ['as', 'as', 'as'],
                ['well', 'well', 'well']
            ],
            'clusters_x': [245.50491333007812, 733.624755859375],
            'clusters_y': [543.5517578125, 127.21426391601562],
            'consensus_score': 2.6666666666666665,
            'line_slope': 320.143,
            'number_views': 3,
            'user_ids': [1, 2, 3],
            'extract_index': [3, 7, 6],
            'gold_standard': [False, True, False],
            'slope_label': 1,
            'gutter_label': 0
        },
        {
            'clusters_text': [
                ['This', 'This', 'This'],
                ['looks', 'looks', 'looks'],
                ['like', 'like', 'like']],
            'clusters_x': [1245.6719970703125, 1760.1119384765625],
            'clusters_y': [483.7331237792969, 67.39566040039062],
            'consensus_score': 3.0,
            'line_slope': 320.143,
            'number_views': 3,
            'user_ids': [1, 2, 3],
            'extract_index': [6, 2, 0],
            'gold_standard': [False, True, False],
            'slope_label': 1,
            'gutter_label': 1
        },
        {
            'clusters_text': [
                ['a', 'a', 'a'],
                ['big', 'big', 'big'],
                ['mess', 'mess', 'mess']
            ],
            'clusters_x': [1346.167236328125, 1798.3958740234375],
            'clusters_y': [526.802490234375, 155.92721557617188],
            'consensus_score': 3.0,
            'line_slope': 320.143,
            'number_views': 3,
            'user_ids': [1, 2, 3],
            'extract_index': [7, 3, 1],
            'gold_standard': [False, True, False],
            'slope_label': 1,
            'gutter_label': 1
        },
        {
            'clusters_text': [
                ['not'],
                ['in'],
                ['a'],
                ['cluster']
            ],
            'clusters_x': [1000, 10],
            'clusters_y': [700, 10],
            'consensus_score': 1.0,
            'line_slope': 214.875,
            'number_views': 1,
            'user_ids': [4],
            'extract_index': [0],
            'gold_standard': [False],
            'slope_label': 2,
            'gutter_label': 0
        }
    ],
    'frame1': [
        {
            'clusters_text': [
                ['page', 'page'],
                ['2', '2']
            ],
            'clusters_x': [1.05, 250.5],
            'clusters_y': [0.95, 0.95],
            'consensus_score': 2.0,
            'line_slope': 0.0,
            'number_views': 2,
            'user_ids': [2, 3],
            'extract_index': [0, 0],
            'gold_standard': [True, False],
            'slope_label': 0,
            'gutter_label': 0
        }
    ],
    'frame2': [
        {
            'clusters_text': [
                ['some'],
                ['words']
            ],
            'clusters_x': [1, 250],
            'clusters_y': [1, 1],
            'consensus_score': 1.0,
            'line_slope': 0.0,
            'number_views': 1,
            'user_ids': [4],
            'extract_index': [0],
            'gold_standard': [False],
            'slope_label': 0,
            'gutter_label': 0
        }
    ]
}

TestOpticsLTReducer = ReducerTest(
    optics_line_text_reducer,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test optics line-text reducer with auto min_samples',
    kwargs={
        'angle_eps': 30,
        'gutter_eps': 150
    },
    okwargs={
        'min_samples': 'auto'
    },
    network_kwargs=kwargs_extra_data
)

TestOpticsLTReducerWithMinSamples = ReducerTest(
    optics_line_text_reducer,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test optics line-text reducer with specified min_samples',
    kwargs={
        'min_samples': 2,
        'angle_eps': 30,
        'gutter_eps': 150
    },
    network_kwargs=kwargs_extra_data
)

extracted_data_with_dolar_sign = [
    {
        'frame0': {
            'points': {
                'x': [[0, 100]],
                'y': [[0, 0]]
            },
            'text': [['$1 2 3 4 5']],
            'slope': [0.0],
            'gold_standard': False
        }
    },
    {
        'frame0': {
            'points': {
                'x': [[0, 100]],
                'y': [[0, 0]]
            },
            'text': [['$1 2 3 4 5']],
            'slope': [0.0],
            'gold_standard': False
        }
    },
    {
        'frame0': {
            'points': {
                'x': [[0, 100]],
                'y': [[0, 0]]
            },
            'text': [['$1 2 3 4 5']],
            'slope': [0.0],
            'gold_standard': False
        }
    },
    {
        'frame0': {
            'points': {
                'x': [[0, 100]],
                'y': [[0, 0]]
            },
            'text': [['$1 2 3 4 5']],
            'slope': [0.0],
            'gold_standard': False
        }
    },
    {
        'frame0': {
            'points': {
                'x': [[0, 100]],
                'y': [[0, 0]]
            },
            'text': [['$1 2 3 4 5']],
            'slope': [0.0],
            'gold_standard': False
        }
    },
    {
        'frame0': {
            'points': {
                'x': [[0, 100]],
                'y': [[0, 0]]
            },
            'text': [['$1 2 3 4 5']],
            'slope': [0.0],
            'gold_standard': False
        }
    },
    {
        'frame0': {
            'points': {
                'x': [[0, 100]],
                'y': [[0, 0]],
            },
            'text': [['$1 2 3 4 5']],
            'slope': [0.0],
            'gold_standard': False
        }
    }
]

kwargs_extra_data_with_dolar_sign = {
    'user_id': [
        1,
        2,
        3,
        4,
        5,
        6,
        None
    ]
}

processed_data_with_dolar_sign = {
    'frame0': {
        'X': [
            [0, 0],
            [1, 1],
            [2, 2],
            [3, 3],
            [4, 4],
            [5, 5],
            [6, 6]
        ],
        'data': [
            {'x': [0, 100], 'y': [0, 0], 'text': ['$1 2 3 4 5'], 'gold_standard': False},
            {'x': [0, 100], 'y': [0, 0], 'text': ['$1 2 3 4 5'], 'gold_standard': False},
            {'x': [0, 100], 'y': [0, 0], 'text': ['$1 2 3 4 5'], 'gold_standard': False},
            {'x': [0, 100], 'y': [0, 0], 'text': ['$1 2 3 4 5'], 'gold_standard': False},
            {'x': [0, 100], 'y': [0, 0], 'text': ['$1 2 3 4 5'], 'gold_standard': False},
            {'x': [0, 100], 'y': [0, 0], 'text': ['$1 2 3 4 5'], 'gold_standard': False},
            {'x': [0, 100], 'y': [0, 0], 'text': ['$1 2 3 4 5'], 'gold_standard': False}
        ]
    }
}

reduced_data_with_dolar_sign = {
    'frame0': [{
        'clusters_x': [0.0, 100.0],
        'clusters_y': [0.0, 0.0],
        'clusters_text': [
            ['$', '$', '$', '$', '$', '$', '$'],
            ['1', '1', '1', '1', '1', '1', '1'],
            ['2', '2', '2', '2', '2', '2', '2'],
            ['3', '3', '3', '3', '3', '3', '3'],
            ['4', '4', '4', '4', '4', '4', '4'],
            ['5', '5', '5', '5', '5', '5', '5'],
        ],
        'consensus_score': 7.0,
        'line_slope': 0.0,
        'number_views': 7,
        'user_ids': [1, 2, 3, 4, 5, 6, None],
        'extract_index': [0, 0, 0, 0, 0, 0, 0],
        'gold_standard': [False, False, False, False, False, False, False],
        'slope_label': 0,
        'gutter_label': 0
    }]
}

TestOpticsLTReducerWithDolarSign = ReducerTest(
    optics_line_text_reducer,
    process_data,
    extracted_data_with_dolar_sign,
    processed_data_with_dolar_sign,
    reduced_data_with_dolar_sign,
    'Test optics line-text reducer with dolar sign',
    kwargs={
        'angle_eps': 30,
        'gutter_eps': 150
    },
    okwargs={'min_samples': 'auto'},
    network_kwargs=kwargs_extra_data_with_dolar_sign
)

# this is a real classification that happened on ASM
extracted_data_no_length = [
    {
        'frame5': {
            'points': {
                'x': [
                    [620.4314017895185, 620.4314017895185]
                ],
                'y': [
                    [142.3093310609288, 142.3093310609288]
                ]
            },
            'text': [
                ['[ no content]']
            ],
            'slope': [0.0],
            'gold_standard': False
        }
    }
]

kwargs_extra_data_no_length = {
    'user_id': [
        1
    ]
}

processed_data_no_length = {
    'frame5': {
        'X': [],
        'data': []
    }
}

reduced_data_no_length = {'frame5': []}

TestOpticsLTReducerNoLengthLine = ReducerTest(
    optics_line_text_reducer,
    process_data,
    extracted_data_no_length,
    processed_data_no_length,
    reduced_data_no_length,
    'Text optics line-text reducer with a zero length line',
    okwargs={
        'min_samples': 'auto',
        'angle_eps': 30,
        'gutter_eps': 150
    },
    network_kwargs=kwargs_extra_data_no_length
)
