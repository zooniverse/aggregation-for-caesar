from panoptes_aggregation.reducers.rectangle_reducer import process_data, rectangle_reducer
from .base_test_class import ReducerTest, ReducerTestNoProcessing

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_width': [50.0, 10.0],
            'T0_tool0_height': [20.0, 8.0]
        },
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_width': [50.0],
            'T0_tool1_height': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_width': [50.0, 10.0],
            'T0_tool0_height': [20.0, 8.0],
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_width': [10.0, 50.0],
            'T0_tool1_height': [8.0, 20.0]
        }
    },
    {
        'frame1': {
            'T0_tool1_x': [50.0],
            'T0_tool1_y': [50.0],
            'T0_tool1_width': [50.0],
            'T0_tool1_height': [50.0]
        }
    },
    {
        'frame0': {
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_width': [10.0, 50.0],
            'T0_tool1_height': [8.0, 20.0]
        },
        'frame1': {
            'T0_tool0_x': [20.0],
            'T0_tool0_y': [20.0],
            'T0_tool0_width': [20.0],
            'T0_tool0_height': [20.0]
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
        'T0_tool0': [
            (0.0, 0.0, 50.0, 20.0),
            (100.0, 100.0, 10.0, 8.0),
            (0.0, 0.0, 50.0, 20.0),
            (100.0, 100.0, 10.0, 8.0)
        ],
        'T0_tool1': [
            (0.0, 100.0, 10.0, 8.0),
            (100.0, 0.0, 50.0, 20.0),
            (0.0, 100.0, 10.0, 8.0),
            (100.0, 0.0, 50.0, 20.0)
        ]
    },
    'frame1': {
        'T0_tool0': [
            (20.0, 20.0, 20.0, 20.0)
        ],
        'T0_tool1': [
            (50.0, 50.0, 50.0, 50.0),
            (50.0, 50.0, 50.0, 50.0)
        ]
    }
}

reduced_data = {
    'frame0': {
        'T0_tool0_rec_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rec_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rec_width': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_rec_height': [20.0, 8.0, 20.0, 8.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool0_clusters_width': [50.0, 10.0],
        'T0_tool0_clusters_height': [20.0, 8.0],
        'T0_tool1_rec_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_rec_y': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_rec_width': [10.0, 50.0, 10.0, 50.0],
        'T0_tool1_rec_height': [8.0, 20.0, 8.0, 20.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_clusters_x': [0.0, 100.0],
        'T0_tool1_clusters_y': [100.0, 0.0],
        'T0_tool1_clusters_width': [10.0, 50.0],
        'T0_tool1_clusters_height': [8.0, 20.0],
    },
    'frame1': {
        'T0_tool0_rec_x': [20.0],
        'T0_tool0_rec_y': [20.0],
        'T0_tool0_rec_width': [20.0],
        'T0_tool0_rec_height': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_rec_x': [50.0, 50.0],
        'T0_tool1_rec_y': [50.0, 50.0],
        'T0_tool1_rec_width': [50.0, 50.0],
        'T0_tool1_rec_height': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_clusters_x': [50.0],
        'T0_tool1_clusters_y': [50.0],
        'T0_tool1_clusters_width': [50.0],
        'T0_tool1_clusters_height': [50.0],
    }
}

TestRectReducer = ReducerTest(
    rectangle_reducer,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test rectangle reducer',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestRectReducer'
)

extracted_data_sw = [
    {
        'frame0': {
            'tool0_x': [0.0, 100.0],
            'tool0_y': [0.0, 100.0],
            'tool0_width': [50.0, 10.0],
            'tool0_height': [20.0, 8.0],
            'tool0_tag': [
                '<graphic>seal</graphic>',
                '<graphic>seal</graphic>'
            ]
        }
    },
    {
        'frame0': {
            'tool0_x': [0.0, 100.0],
            'tool0_y': [0.0, 100.0],
            'tool0_width': [50.0, 10.0],
            'tool0_height': [20.0, 8.0],
            'tool0_tag': [
                '<graphic>seal</graphic>',
                '<graphic>text</graphic>'
            ]
        }
    }
]

kwargs_extra_data_sw = {
    'user_id': [
        1,
        2
    ]
}

processed_data_sw = {
    'frame0': {
        'tool0': [
            (0.0, 0.0, 50.0, 20.0),
            (100.0, 100.0, 10.0, 8.0),
            (0.0, 0.0, 50.0, 20.0),
            (100.0, 100.0, 10.0, 8.0)
        ],
        'tag': [
            '<graphic>seal</graphic>',
            '<graphic>seal</graphic>',
            '<graphic>seal</graphic>',
            '<graphic>text</graphic>'
        ]
    }
}

reduced_data_sw = {
    'frame0': {
        'rec_tags': [
            '<graphic>seal</graphic>',
            '<graphic>seal</graphic>',
            '<graphic>seal</graphic>',
            '<graphic>text</graphic>'
        ],
        'tool0_rec_x': [0.0, 100.0, 0.0, 100.0],
        'tool0_rec_y': [0.0, 100.0, 0.0, 100.0],
        'tool0_rec_width': [50.0, 10.0, 50.0, 10.0],
        'tool0_rec_height': [20.0, 8.0, 20.0, 8.0],
        'tool0_cluster_labels': [0, 1, 0, 1],
        'tool0_clusters_count': [2, 2],
        'tool0_clusters_x': [0.0, 100.0],
        'tool0_clusters_y': [0.0, 100.0],
        'tool0_clusters_width': [50.0, 10.0],
        'tool0_clusters_height': [20.0, 8.0],
    }
}

TestSWRectReducer = ReducerTest(
    rectangle_reducer,
    process_data,
    extracted_data_sw,
    processed_data_sw,
    reduced_data_sw,
    'Test SW rectangle reducer',
    network_kwargs=kwargs_extra_data_sw,
    kwargs={
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestSWRectReducer'
)

extracted_data_with_mixed_subtasks = [
    {
        "frame0": {
            "T0_tool0_x": [
                901.3092651367188, 904.9237060546875, 896.7911987304688, 880.5261840820312,
                887.7550659179688, 867.8756103515625, 890.4659423828125, 893.1767578125,
                903.1165161132812, 894.080322265625, 913.9598388671875, 915.76708984375,
                938.0682373046875, 976.9236450195312, 985.9597778320312
            ],
            "T0_tool0_y": [
                729.5806884765625, 840.72509765625, 940.12255859375, 1035.905517578125,
                1137.1102294921875, 1250.965576171875, 1357.5919189453125, 1462.4110107421875,
                1561.808349609375, 1680.1817626953125, 1766.0250244140625, 1873.554931640625,
                1989.89404296875, 2072.122802734375, 2215.79736328125
            ],
            "T0_tool0_width": [
                770.7821655273438, 750.902587890625, 728.3123168945312, 774.3965454101562,
                782.5291137695312, 835.84228515625, 793.3724365234375, 768.0712890625,
                766.2640991210938, 752.7099609375, 760.8424072265625, 752.7098388671875,
                631.625732421875, 637.0473022460938, 652.4087524414062
            ],
            "T0_tool0_height": [
                102.1082763671875, 93.975830078125, 110.2408447265625, 114.7589111328125,
                127.409423828125, 84.9395751953125, 120.1805419921875, 110.2408447265625,
                130.120361328125, 72.2891845703125, 95.782958984375, 129.216552734375,
                75.903564453125, 136.44580078125, 65.060302734375
            ],
            "T0_tool0_details": [
                [
                    {"text": "Lilley", "gold_standard": False},
                    {"text": "1915-05-05", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Malta", "gold_standard": False},
                    {"text": "1917-05-18", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "J. Lilley &Son", "gold_standard": False},
                    {"text": "1917-12-07", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Cape of Good Hope", "gold_standard": False},
                    {"text": "1918-07-02", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "J Lilley &Son", "gold_standard": False},
                    {"text": "1918-09-20", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": 'HMS ""Kildare""', "gold_standard": False},
                    {"text": "1919-05-05", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "J Lilly&Son", "gold_standard": False},
                    {"text": "1922-10-13", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "JLilley &Son", "gold_standard": False},
                    {"text": "1923-02-16", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "J Lilley &Son", "gold_standard": False},
                    {"text": "1923-04-27", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Portsmouth", "gold_standard": False},
                    {"text": "1924-03-31", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Sheerness", "gold_standard": False},
                    {"text": "1926-01-27", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Lilley", "gold_standard": False},
                    {"text": "1927-03-31", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Portsmouth", "gold_standard": False},
                    {"text": "1929-12-03", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Lilley", "gold_standard": False},
                    {"text": "1931-03-25", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "V. Kullberg", "gold_standard": False},
                    {"text": "1935-08-30", "gold_standard": False},
                    {"text": "2-16-0", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
            ],
        }
    },
    {
        "frame0": {
            "T0_tool0_x": [],
            "T0_tool0_y": [],
            "T0_tool0_width": [],
            "T0_tool0_height": [],
            "T0_tool0_details": [],
        }
    },
    {
        "frame0": {
            "T0_tool0_x": [
                -9.742353439331055, 423.4798278808594, 1160.939208984375,
                883.1085205078125, 1363.4852294921875, 1115.87890625,
                873.0498046875, 1031.3603515625, 1181.77392578125,
                903.3765869140625, 1185.6890869140625, 891.61962890625,
                880.8611450195312, 876.495849609375, 872.1119384765625,
                874.17138671875, 872.6128540039062, 878.608642578125,
                884.288818359375, 886.793212890625, 887.1810913085938,
                887.0620727539062, 893.8353881835938, 884.1692504882812,
                904.79541015625, 887.8665161132812, 870.9708251953125
            ],
            "T0_tool0_y": [
                -3.116422653198242, 256.030029296875, 243.6797332763672,
                383.2991943359375, 110.43333435058594, 712.0652465820312,
                699.6864013671875, 719.7999877929688, 713.116455078125,
                737.5718994140625, 753.4766235351562, 715.47021484375,
                695.65087890625, 819.0789794921875, 909.5127563476562,
                1017.8277587890625, 1117.206298828125, 1335.4556884765625,
                1436.809326171875, 1547.3175048828125, 1649.8463134765625,
                1759.5242919921875, 1874.884521484375, 1985.36669921875,
                2085.9462890625, 2206.82373046875, 1343.0013427734375
            ],
            "T0_tool0_width": [
                336.03468132019043, 349.5593566894531, 102.291015625,
                48.19427490234375, 50.0760498046875, 0,
                472.5726318359375, 355.8408203125, 488.4212646484375,
                276.3695068359375, 191.9783935546875, 309.0950927734375,
                807.5890502929688, 809.861083984375, 813.3726806640625,
                827.4056396484375, 815.9467163085938, 809.661376953125,
                801.8133544921875, 791.160888671875, 802.7300415039062,
                798.5192260742188, 800.9204711914062, 805.5040893554688,
                762.917724609375, 794.4669799804688, 816.923095703125
            ],
            "T0_tool0_height": [
                524.3477458953857, 113.49136352539062, 94.02519226074219,
                96.18414306640625, 82.36686706542969, 0,
                26.27093505859375, 31.686279296875, 9.3726806640625,
                24.7528076171875, 30.563232421875, 120.85577392578125,
                122.03204345703125, 88.61627197265625, 103.9720458984375,
                91.78271484375, 101.5477294921875, 91.816650390625,
                94.9967041015625, 90.3236083984375, 100.845947265625,
                101.8271484375, 75.5814208984375, 96.654052734375,
                81.45263671875, 78.5068359375, 99.2750244140625
            ],
            "T0_tool0_details": [
                [],
                [],
                [],
                [],
                [],
                [],
                [
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Lilly", "gold_standard": False},
                    {"text": "1915-05-05", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Malta", "gold_standard": False},
                    {"text": "1914-05-18", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "J. Lilley & Son", "gold_standard": False},
                    {"text": "1914-12-07", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Cape of Good Hope", "gold_standard": False},
                    {"text": "1918-07-02", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "J Lilley & Son", "gold_standard": False},
                    {"text": "1918-09-20", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "J Lilley & Son", "gold_standard": False},
                    {"text": "1922-12-13", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "J Lilley & Son", "gold_standard": False},
                    {"text": "1923-02-07", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "J Lilly & Son", "gold_standard": False},
                    {"text": "1923-04-27", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Portsmouth", "gold_standard": False},
                    {"text": "1924-03-31", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Sheemess", "gold_standard": False},
                    {"text": "1926-01-27", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Lilly", "gold_standard": False},
                    {"text": "1924-05-31", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Portsmouth", "gold_standard": False},
                    {"text": "1919-12-03", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "Lilly", "gold_standard": False},
                    {"text": "1931-03-28", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "V. Kullberg (unclear)", "gold_standard": False},
                    {"text": "1935-08-30", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
                [
                    {"text": "(unclear)Steve Vildare(unclear)", "gold_standard": False},
                    {"text": "1919-05-05", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ],
            ],
        }
    },
    {
        "frame0": {
            "T0_tool0_x": [875.6729125976562],
            "T0_tool0_y": [2184.53515625],
            "T0_tool0_width": [811.0797729492188],
            "T0_tool0_height": [104.9940185546875],
            "T0_tool0_details": [
                [
                    {"text": "V Kullberg ", "gold_standard": False},
                    {"text": "1935-08-30", "gold_standard": False},
                    {"text": "2-16-0", "gold_standard": False},
                    {"text": "", "gold_standard": False},
                ]
            ],
        }
    },
]


reduced_data_with_mixed_subtasks = {
    "frame0": {
        "T0_tool0_rec_x": [
            901.3092651367188, 904.9237060546875, 896.7911987304688, 880.5261840820312,
            887.7550659179688, 867.8756103515625, 890.4659423828125, 893.1767578125,
            903.1165161132812, 894.080322265625, 913.9598388671875, 915.76708984375,
            938.0682373046875, 976.9236450195312, 985.9597778320312,
            873.0498046875, 1031.3603515625, 1181.77392578125, 903.3765869140625,
            1185.6890869140625, 891.61962890625, 880.8611450195312,
            876.495849609375, 872.1119384765625, 874.17138671875,
            872.6128540039062, 878.608642578125, 884.288818359375,
            886.793212890625, 887.1810913085938, 887.0620727539062,
            893.8353881835938, 884.1692504882812, 904.79541015625,
            887.8665161132812,
            870.9708251953125,
            875.6729125976562
        ],
        "T0_tool0_rec_y": [
            729.5806884765625, 840.72509765625, 940.12255859375, 1035.905517578125,
            1137.1102294921875, 1250.965576171875, 1357.5919189453125, 1462.4110107421875,
            1561.808349609375, 1680.1817626953125, 1766.0250244140625, 1873.554931640625,
            1989.89404296875, 2072.122802734375, 2215.79736328125,
            699.6864013671875, 719.7999877929688, 713.116455078125,
            737.5718994140625, 753.4766235351562, 715.47021484375,
            695.65087890625, 819.0789794921875, 909.5127563476562,
            1017.8277587890625, 1117.206298828125, 1335.4556884765625,
            1436.809326171875, 1547.3175048828125, 1649.8463134765625,
            1759.5242919921875, 1874.884521484375, 1985.36669921875,
            2085.9462890625, 2206.82373046875,
            1343.0013427734375,
            2184.53515625
        ],
        "T0_tool0_rec_width": [
            770.7821655273438, 750.902587890625, 728.3123168945312, 774.3965454101562,
            782.5291137695312, 835.84228515625, 793.3724365234375, 768.0712890625,
            766.2640991210938, 752.7099609375, 760.8424072265625, 752.7098388671875,
            631.625732421875, 637.0473022460938, 652.4087524414062,
            472.5726318359375, 355.8408203125, 488.4212646484375,
            276.3695068359375, 191.9783935546875, 309.0950927734375,
            807.5890502929688, 809.861083984375, 813.3726806640625,
            827.4056396484375, 815.9467163085938, 809.661376953125,
            801.8133544921875, 791.160888671875, 802.7300415039062,
            798.5192260742188, 800.9204711914062, 805.5040893554688,
            762.917724609375, 794.4669799804688,
            816.923095703125,
            811.0797729492188
        ],
        "T0_tool0_rec_height": [
            102.1082763671875, 93.975830078125, 110.2408447265625, 114.7589111328125,
            127.409423828125, 84.9395751953125, 120.1805419921875, 110.2408447265625,
            130.120361328125, 72.2891845703125, 95.782958984375, 129.216552734375,
            75.903564453125, 136.44580078125, 65.060302734375,
            26.27093505859375, 31.686279296875, 9.3726806640625,
            24.7528076171875, 30.563232421875, 120.85577392578125,
            122.03204345703125, 88.61627197265625, 103.9720458984375,
            91.78271484375, 101.5477294921875, 91.816650390625,
            94.9967041015625, 90.3236083984375, 100.845947265625,
            101.8271484375, 75.5814208984375, 96.654052734375,
            81.45263671875, 78.5068359375,
            99.2750244140625,
            104.9940185546875
        ],
        "T0_tool0_cluster_labels": [
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, -1
        ],
        "T0_tool0_details": [
            [
                {"text": "Lilley", "gold_standard": False},
                {"text": "1915-05-05", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Malta", "gold_standard": False},
                {"text": "1917-05-18", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "J. Lilley &Son", "gold_standard": False},
                {"text": "1917-12-07", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Cape of Good Hope", "gold_standard": False},
                {"text": "1918-07-02", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "J Lilley &Son", "gold_standard": False},
                {"text": "1918-09-20", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": 'HMS ""Kildare""', "gold_standard": False},
                {"text": "1919-05-05", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "J Lilly&Son", "gold_standard": False},
                {"text": "1922-10-13", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "JLilley &Son", "gold_standard": False},
                {"text": "1923-02-16", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "J Lilley &Son", "gold_standard": False},
                {"text": "1923-04-27", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Portsmouth", "gold_standard": False},
                {"text": "1924-03-31", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Sheerness", "gold_standard": False},
                {"text": "1926-01-27", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Lilley", "gold_standard": False},
                {"text": "1927-03-31", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Portsmouth", "gold_standard": False},
                {"text": "1929-12-03", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Lilley", "gold_standard": False},
                {"text": "1931-03-25", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "V. Kullberg", "gold_standard": False},
                {"text": "1935-08-30", "gold_standard": False},
                {"text": "2-16-0", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Lilly", "gold_standard": False},
                {"text": "1915-05-05", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Malta", "gold_standard": False},
                {"text": "1914-05-18", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "J. Lilley & Son", "gold_standard": False},
                {"text": "1914-12-07", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Cape of Good Hope", "gold_standard": False},
                {"text": "1918-07-02", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "J Lilley & Son", "gold_standard": False},
                {"text": "1918-09-20", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "J Lilley & Son", "gold_standard": False},
                {"text": "1922-12-13", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "J Lilley & Son", "gold_standard": False},
                {"text": "1923-02-07", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "J Lilly & Son", "gold_standard": False},
                {"text": "1923-04-27", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Portsmouth", "gold_standard": False},
                {"text": "1924-03-31", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Sheemess", "gold_standard": False},
                {"text": "1926-01-27", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Lilly", "gold_standard": False},
                {"text": "1924-05-31", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Portsmouth", "gold_standard": False},
                {"text": "1919-12-03", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "Lilly", "gold_standard": False},
                {"text": "1931-03-28", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "V. Kullberg (unclear)", "gold_standard": False},
                {"text": "1935-08-30", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "(unclear)Steve Vildare(unclear)", "gold_standard": False},
                {"text": "1919-05-05", "gold_standard": False},
                {"text": "", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
            [
                {"text": "V Kullberg ", "gold_standard": False},
                {"text": "1935-08-30", "gold_standard": False},
                {"text": "2-16-0", "gold_standard": False},
                {"text": "", "gold_standard": False},
            ],
        ],
    }
}



TestRectReducerMixedSubtasks = ReducerTestNoProcessing(
    rectangle_reducer,
    extracted_data_with_mixed_subtasks,
    reduced_data_with_mixed_subtasks,
    'Test rectangle reducer with extracted data with both empty and non-empty subtasks',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'eps': 5,
        'min_samples': 2,
        'details': {
            'T0_tool0': [
                'text_reducer',
                'text_reducer',
                'text_reducer',
                'text_reducer'
                    ]
                }
    },
    test_name='TestRectReducerMixedSubtasks'
)