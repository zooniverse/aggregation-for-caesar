from panoptes_aggregation.reducers.shape_reducer_dbscan import process_data as process_data_dbscan, shape_reducer_dbscan
from panoptes_aggregation.reducers.shape_reducer_hdbscan import process_data as process_data_hdbscan, shape_reducer_hdbscan
from panoptes_aggregation.reducers.shape_reducer_optics import process_data as process_data_optics, shape_reducer_optics
from .base_test_class import ReducerTest, ReducerTestNoProcessing
import copy

extracted_data = [
    {
        'frame0': {
            'T0_tool0_x': [0.0, 100.0],
            'T0_tool0_y': [0.0, 100.0],
            'T0_tool0_width': [50.0, 10.0],
            'T0_tool0_height': [60.0, 20.0]
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
            'T0_tool0_height': [60.0, 20.0],
            'T0_tool1_x': [0.0, 100.0],
            'T0_tool1_y': [100.0, 0.0],
            'T0_tool1_width': [10.0, 50.0],
            'T0_tool1_height': [50.0, 10.0]
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
            'T0_tool1_height': [50.0, 10.0]
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
    'n_classifications': 5,
    'shape': 'rectangle',
    'symmetric': False,
    'frame0': {
        'T0_tool0': [
            (0.0, 0.0, 50.0, 60.0),
            (100.0, 100.0, 10.0, 20.0),
            (0.0, 0.0, 50.0, 60.0),
            (100.0, 100.0, 10.0, 20.0)
        ],
        'T0_tool1': [
            (0.0, 100.0, 10.0, 50.0),
            (100.0, 0.0, 50.0, 10.0),
            (0.0, 100.0, 10.0, 50.0),
            (100.0, 0.0, 50.0, 10.0)
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
        'T0_tool0_rectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rectangle_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rectangle_width': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_rectangle_height': [60.0, 20.0, 60.0, 20.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_n_classifications': [5, 5],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool0_clusters_width': [50.0, 10.0],
        'T0_tool0_clusters_height': [60.0, 20.0],
        'T0_tool0_shape': ['rectangle', 'rectangle'],
        'T0_tool1_rectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_rectangle_y': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_rectangle_width': [10.0, 50.0, 10.0, 50.0],
        'T0_tool1_rectangle_height': [50.0, 10.0, 50.0, 10.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_n_classifications': [5, 5],
        'T0_tool1_clusters_x': [0.0, 100.0],
        'T0_tool1_clusters_y': [100.0, 0.0],
        'T0_tool1_clusters_width': [10.0, 50.0],
        'T0_tool1_clusters_height': [50.0, 10.0],
        'T0_tool1_shape': ['rectangle', 'rectangle']
    },
    'frame1': {
        'T0_tool0_rectangle_x': [20.0],
        'T0_tool0_rectangle_y': [20.0],
        'T0_tool0_rectangle_width': [20.0],
        'T0_tool0_rectangle_height': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_rectangle_x': [50.0, 50.0],
        'T0_tool1_rectangle_y': [50.0, 50.0],
        'T0_tool1_rectangle_width': [50.0, 50.0],
        'T0_tool1_rectangle_height': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_n_classifications': [5],
        'T0_tool1_clusters_x': [50.0],
        'T0_tool1_clusters_y': [50.0],
        'T0_tool1_clusters_width': [50.0],
        'T0_tool1_clusters_height': [50.0],
        'T0_tool1_shape': ['rectangle']
    }
}

TestShapeReducerRectangle = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape rectangle reducer with DBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'eps': 5,
        'min_samples': 2
    },
    test_name='TestShapeReducerRectangle'
)

TestShapeReducerRectangleOptics = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data,
    'Test shape rectangle reducer with OPTICS',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'min_samples': 2
    },
    test_name='TestShapeReducerRectangleOptics'
)


reduced_data_hdbscan = copy.deepcopy(reduced_data)
reduced_data_hdbscan['frame0']['T0_tool0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame0']['T0_tool1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan['frame1']['T0_tool0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan['frame1']['T0_tool1_cluster_probabilities'] = [1.0, 1.0]

TestShapeReducerRectangleHdbscan = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan,
    'Test shape rectangle reducer with HDBSCAN',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerRectangleHdbscan'
)


reduced_data_collab_true = {
    'data': [
        {
            "frame": 0,
            "markID": "consensus_0",
            "min_threshold": 0,
            "stepKey": "S0",
            "taskIndex": 0,
            "taskKey": "T0",
            "taskType": "rectangle",
            "threshold": 0.4,
            "toolIndex": 0,
            "toolType": "freehandLine",
            "pathX": 0.0,
            "pathY": 0.0,
            "pathWidth": 50.0,
            "pathHeight": 60.0
        },
        {
            "frame": 0,
            "markID": "consensus_1",
            "min_threshold": 0,
            "stepKey": "S0",
            "taskIndex": 0,
            "taskKey": "T0",
            "taskType": "rectangle",
            "threshold": 0.4,
            "toolIndex": 0,
            "toolType": "freehandLine",
            "pathX": 100.0,
            "pathY": 100.0,
            "pathWidth": 10.0,
            "pathHeight": 20.0
        },
        {
            "frame": 0,
            "markID": "consensus_0",
            "min_threshold": 0,
            "stepKey": "S0",
            "taskIndex": 0,
            "taskKey": "T0",
            "taskType": "rectangle",
            "threshold": 0.4,
            "toolIndex": 1,
            "toolType": "freehandLine",
            "pathX": 0.0,
            "pathY": 100.0,
            "pathWidth": 10.0,
            "pathHeight": 50.0,
        },
        {
            "frame": 0,
            "markID": "consensus_1",
            "min_threshold": 0,
            "stepKey": "S0",
            "taskIndex": 0,
            "taskKey": "T0",
            "taskType": "rectangle",
            "threshold": 0.4,
            "toolIndex": 1,
            "toolType": "freehandLine",
            "pathX": 100.0,
            "pathY": 0.0,
            "pathWidth": 50.0,
            "pathHeight": 10.0
        },
        {
            "frame": 1,
            "markID": "consensus_0",
            "min_threshold": 0,
            "stepKey": "S0",
            "taskIndex": 0,
            "taskKey": "T0",
            "taskType": "rectangle",
            "threshold": 0.4,
            "toolIndex": 1,
            "toolType": "freehandLine",
            "pathX": 50.0,
            "pathY": 50.0,
            "pathWidth": 50.0,
            "pathHeight": 50.0
        }
    ],
    'frame0': {
        'T0_tool0_rectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rectangle_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rectangle_width': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_rectangle_height': [60.0, 20.0, 60.0, 20.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [2, 2],
        'T0_tool0_n_classifications': [5, 5],
        'T0_tool0_clusters_x': [0.0, 100.0],
        'T0_tool0_clusters_y': [0.0, 100.0],
        'T0_tool0_clusters_width': [50.0, 10.0],
        'T0_tool0_clusters_height': [60.0, 20.0],
        'T0_tool0_shape': ['rectangle', 'rectangle'],
        'T0_tool1_rectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_rectangle_y': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_rectangle_width': [10.0, 50.0, 10.0, 50.0],
        'T0_tool1_rectangle_height': [50.0, 10.0, 50.0, 10.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [2, 2],
        'T0_tool1_n_classifications': [5, 5],
        'T0_tool1_clusters_x': [0.0, 100.0],
        'T0_tool1_clusters_y': [100.0, 0.0],
        'T0_tool1_clusters_width': [10.0, 50.0],
        'T0_tool1_clusters_height': [50.0, 10.0],
        'T0_tool1_shape': ['rectangle', 'rectangle']
    },
    'frame1': {
        'T0_tool0_rectangle_x': [20.0],
        'T0_tool0_rectangle_y': [20.0],
        'T0_tool0_rectangle_width': [20.0],
        'T0_tool0_rectangle_height': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_rectangle_x': [50.0, 50.0],
        'T0_tool1_rectangle_y': [50.0, 50.0],
        'T0_tool1_rectangle_width': [50.0, 50.0],
        'T0_tool1_rectangle_height': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [2],
        'T0_tool1_n_classifications': [5],
        'T0_tool1_clusters_x': [50.0],
        'T0_tool1_clusters_y': [50.0],
        'T0_tool1_clusters_width': [50.0],
        'T0_tool1_clusters_height': [50.0],
        'T0_tool1_shape': ['rectangle']
    }
}

TestShapeReducerRectangleDbscanCollabTrue = ReducerTest(
    shape_reducer_dbscan,
    process_data_dbscan,
    extracted_data,
    processed_data,
    reduced_data_collab_true,
    'Test shape rectangle reducer with DBSCAN when collab: True',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'eps': 5,
        'min_samples': 2,
        'collab': True
    },
    test_name='TestShapeReducerRectangleDBScanCollabTrue'
)

TestShapeReducerRectangleOpticsCollabTrue = ReducerTest(
    shape_reducer_optics,
    process_data_optics,
    extracted_data,
    processed_data,
    reduced_data_collab_true,
    'Test shape rectangle reducer with OPTICS when collab: True',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'min_samples': 2,
        'collab': True
    },
    test_name='TestShapeReducerRectangleOpticsCollabTrue'
)

reduced_data_hdbscan_collab_true = copy.deepcopy(reduced_data_collab_true)
reduced_data_hdbscan_collab_true['frame0']['T0_tool0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan_collab_true['frame0']['T0_tool1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan_collab_true['frame1']['T0_tool0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan_collab_true['frame1']['T0_tool1_cluster_probabilities'] = [1.0, 1.0]

TestShapeReducerRectangleHdbscanCollabTrue = ReducerTest(
    shape_reducer_hdbscan,
    process_data_hdbscan,
    extracted_data,
    processed_data,
    reduced_data_hdbscan_collab_true,
    'Test shape rectangle reducer with HDBSCAN when collab: True',
    network_kwargs=kwargs_extra_data,
    pkwargs={'shape': 'rectangle'},
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'collab': True,
        'allow_single_cluster': True
    },
    test_name='TestShapeReducerRectangleHdbscanCollabTrue'
)

reduced_data_min_threshold = {
    'frame0': {
        'T0_tool0_rectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rectangle_y': [0.0, 100.0, 0.0, 100.0],
        'T0_tool0_rectangle_width': [50.0, 10.0, 50.0, 10.0],
        'T0_tool0_rectangle_height': [60.0, 20.0, 60.0, 20.0],
        'T0_tool0_cluster_labels': [0, 1, 0, 1],
        'T0_tool0_clusters_count': [],
        'T0_tool0_n_classifications': [5, 5],
        'T0_tool0_clusters_x': [],
        'T0_tool0_clusters_y': [],
        'T0_tool0_clusters_width': [],
        'T0_tool0_clusters_height': [],
        'T0_tool0_shape': ['rectangle', 'rectangle'],
        'T0_tool1_rectangle_x': [0.0, 100.0, 0.0, 100.0],
        'T0_tool1_rectangle_y': [100.0, 0.0, 100.0, 0.0],
        'T0_tool1_rectangle_width': [10.0, 50.0, 10.0, 50.0],
        'T0_tool1_rectangle_height': [50.0, 10.0, 50.0, 10.0],
        'T0_tool1_cluster_labels': [0, 1, 0, 1],
        'T0_tool1_clusters_count': [],
        'T0_tool1_n_classifications': [5, 5],
        'T0_tool1_clusters_x': [],
        'T0_tool1_clusters_y': [],
        'T0_tool1_clusters_width': [],
        'T0_tool1_clusters_height': [],
        'T0_tool1_shape': ['rectangle', 'rectangle']
    },
    'frame1': {
        'T0_tool0_rectangle_x': [20.0],
        'T0_tool0_rectangle_y': [20.0],
        'T0_tool0_rectangle_width': [20.0],
        'T0_tool0_rectangle_height': [20.0],
        'T0_tool0_cluster_labels': [-1],
        'T0_tool1_rectangle_x': [50.0, 50.0],
        'T0_tool1_rectangle_y': [50.0, 50.0],
        'T0_tool1_rectangle_width': [50.0, 50.0],
        'T0_tool1_rectangle_height': [50.0, 50.0],
        'T0_tool1_cluster_labels': [0, 0],
        'T0_tool1_clusters_count': [],
        'T0_tool1_n_classifications': [5],
        'T0_tool1_clusters_x': [],
        'T0_tool1_clusters_y': [],
        'T0_tool1_clusters_width': [],
        'T0_tool1_clusters_height': [],
        'T0_tool1_shape': ['rectangle']
    }
}

TestShapeReducerRectangleDbscanMinThreshold = ReducerTestNoProcessing(
    shape_reducer_dbscan,
    extracted_data,
    reduced_data_min_threshold,
    'Test shape rectangle reducer with DBSCAN when collab: True and threshold < min_threshold',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'eps': 5,
        'min_samples': 2,
        'collab': True,
        'min_threshold': 0.5,
        'shape': 'rectangle'
    },
    test_name='TestShapeReducerRectangleDBScanMinThreshold'
)


TestShapeReducerRectangleOpticsMinThreshold = ReducerTestNoProcessing(
    shape_reducer_optics,
    extracted_data,
    reduced_data_min_threshold,
    'Test shape rectangle reducer with OPTICS when collab: True and threshold < min_threshold',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'min_samples': 2,
        'collab': True,
        'min_threshold': 0.5,
        'shape': 'rectangle'
    },
    test_name='TestShapeReducerRectangleOpticsMinThreshold'
)

reduced_data_hdbscan_min_threshold = copy.deepcopy(reduced_data_min_threshold)
reduced_data_hdbscan_min_threshold['frame0']['T0_tool0_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan_min_threshold['frame0']['T0_tool1_cluster_probabilities'] = [1.0, 1.0, 1.0, 1.0]
reduced_data_hdbscan_min_threshold['frame1']['T0_tool0_cluster_probabilities'] = [0.0]
reduced_data_hdbscan_min_threshold['frame1']['T0_tool1_cluster_probabilities'] = [1.0, 1.0]

TestShapeReducerRectangleHdbscanMinThreshold = ReducerTestNoProcessing(
    shape_reducer_hdbscan,
    extracted_data,
    reduced_data_hdbscan_min_threshold,
    'Test shape rectangle reducer with HDBSCAN when collab: True and threshold < min_threshold',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'min_cluster_size': 2,
        'min_samples': 1,
        'min_threshold': 0.5,
        'collab': True,
        'allow_single_cluster': True,
        'shape': 'rectangle'
    },
    test_name='TestShapeReducerRectangleHdbscanMinThreshold'
)

extracted_data_empty_subtasks_clusters_of_one = [
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
                    {'text': 'Lilley', 'gold_standard': False},
                    {'text': '1915-05-05', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Malta', 'gold_standard': False},
                    {'text': '1917-05-18', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'J. Lilley &Son', 'gold_standard': False},
                    {'text': '1917-12-07', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Cape of Good Hope', 'gold_standard': False},
                    {'text': '1918-07-02', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'J Lilley &Son', 'gold_standard': False},
                    {'text': '1918-09-20', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'HMS ""Kildare""', 'gold_standard': False},
                    {'text': '1919-05-05', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'J Lilly&Son', 'gold_standard': False},
                    {'text': '1922-10-13', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'JLilley &Son', 'gold_standard': False},
                    {'text': '1923-02-16', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'J Lilley &Son', 'gold_standard': False},
                    {'text': '1923-04-27', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Portsmouth', 'gold_standard': False},
                    {'text': '1924-03-31', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Sheerness', 'gold_standard': False},
                    {'text': '1926-01-27', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Lilley', 'gold_standard': False},
                    {'text': '1927-03-31', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Portsmouth', 'gold_standard': False},
                    {'text': '1929-12-03', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Lilley', 'gold_standard': False},
                    {'text': '1931-03-25', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'V. Kullberg', 'gold_standard': False},
                    {'text': '1935-08-30', 'gold_standard': False},
                    {'text': '2-16-0', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ]
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
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Lilly', 'gold_standard': False},
                    {'text': '1915-05-05', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Malta', 'gold_standard': False},
                    {'text': '1914-05-18', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'J. Lilley & Son', 'gold_standard': False},
                    {'text': '1914-12-07', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Cape of Good Hope', 'gold_standard': False},
                    {'text': '1918-07-02', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'J Lilley & Son', 'gold_standard': False},
                    {'text': '1918-09-20', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'J Lilley & Son', 'gold_standard': False},
                    {'text': '1922-12-13', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'J Lilley & Son', 'gold_standard': False},
                    {'text': '1923-02-07', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'J Lilly & Son', 'gold_standard': False},
                    {'text': '1923-04-27', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Portsmouth', 'gold_standard': False},
                    {'text': '1924-03-31', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Sheemess', 'gold_standard': False},
                    {'text': '1926-01-27', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Lilly', 'gold_standard': False},
                    {'text': '1924-05-31', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Portsmouth', 'gold_standard': False},
                    {'text': '1919-12-03', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Lilly', 'gold_standard': False},
                    {'text': '1931-03-28', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'V. Kullberg (unclear)', 'gold_standard': False},
                    {'text': '1935-08-30', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': '(unclear)Steve Vildare(unclear)', 'gold_standard': False},
                    {'text': '1919-05-05', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ]
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


reduced_data_empty_subtasks_clusters_of_one = {
    "frame0": {
        "T0_tool0_rectangle_x": [
            901.3092651367188, 904.9237060546875, 896.7911987304688, 880.5261840820312,
            887.7550659179688, 867.8756103515625, 890.4659423828125, 893.1767578125,
            903.1165161132812, 894.080322265625, 913.9598388671875, 915.76708984375,
            938.0682373046875, 976.9236450195312, 985.9597778320312, -9.742353439331055,
            423.4798278808594, 1160.939208984375, 883.1085205078125, 1363.4852294921875,
            1115.87890625, 873.0498046875, 1031.3603515625, 1181.77392578125,
            903.3765869140625, 1185.6890869140625, 891.61962890625, 880.8611450195312,
            876.495849609375, 872.1119384765625, 874.17138671875, 872.6128540039062,
            878.608642578125, 884.288818359375, 886.793212890625, 887.1810913085938,
            887.0620727539062, 893.8353881835938, 884.1692504882812, 904.79541015625,
            887.8665161132812, 870.9708251953125, 875.6729125976562
        ],
        "T0_tool0_rectangle_y": [
            729.5806884765625, 840.72509765625, 940.12255859375, 1035.905517578125,
            1137.1102294921875, 1250.965576171875, 1357.5919189453125, 1462.4110107421875,
            1561.808349609375, 1680.1817626953125, 1766.0250244140625, 1873.554931640625,
            1989.89404296875, 2072.122802734375, 2215.79736328125, -3.116422653198242,
            256.030029296875, 243.6797332763672, 383.2991943359375, 110.43333435058594,
            712.0652465820312, 699.6864013671875, 719.7999877929688, 713.116455078125,
            737.5718994140625, 753.4766235351562, 715.47021484375, 695.65087890625,
            819.0789794921875, 909.5127563476562, 1017.8277587890625, 1117.206298828125,
            1335.4556884765625, 1436.809326171875, 1547.3175048828125, 1649.8463134765625,
            1759.5242919921875, 1874.884521484375, 1985.36669921875, 2085.9462890625,
            2206.82373046875, 1343.0013427734375, 2184.53515625
        ],
        "T0_tool0_rectangle_width": [
            770.7821655273438, 750.902587890625, 728.3123168945312, 774.3965454101562,
            782.5291137695312, 835.84228515625, 793.3724365234375, 768.0712890625,
            766.2640991210938, 752.7099609375, 760.8424072265625, 752.7098388671875,
            631.625732421875, 637.0473022460938, 652.4087524414062, 336.03468132019043,
            349.5593566894531, 102.291015625, 48.19427490234375, 50.0760498046875,
            0.0, 472.5726318359375, 355.8408203125, 488.4212646484375,
            276.3695068359375, 191.9783935546875, 309.0950927734375, 807.5890502929688,
            809.861083984375, 813.3726806640625, 827.4056396484375, 815.9467163085938,
            809.661376953125, 801.8133544921875, 791.160888671875, 802.7300415039062,
            798.5192260742188, 800.9204711914062, 805.5040893554688, 762.917724609375,
            794.4669799804688, 816.923095703125, 811.0797729492188
        ],
        "T0_tool0_rectangle_height": [
            102.1082763671875, 93.975830078125, 110.2408447265625, 114.7589111328125,
            127.409423828125, 84.9395751953125, 120.1805419921875, 110.2408447265625,
            130.120361328125, 72.2891845703125, 95.782958984375, 129.216552734375,
            75.903564453125, 136.44580078125, 65.060302734375, 524.3477458953857,
            113.49136352539062, 94.02519226074219, 96.18414306640625, 82.36686706542969,
            0.0, 26.27093505859375, 31.686279296875, 9.3726806640625,
            24.7528076171875, 30.563232421875, 120.85577392578125, 122.03204345703125,
            88.61627197265625, 103.9720458984375, 91.78271484375, 101.5477294921875,
            91.816650390625, 94.9967041015625, 90.3236083984375, 100.845947265625,
            101.8271484375, 75.5814208984375, 96.654052734375, 81.45263671875,
            78.5068359375, 99.2750244140625, 104.9940185546875
        ],
        "T0_tool0_cluster_labels": [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
            18, 19, -1, 20, 21, 22, 23, 24, 25, 0, 1, 26, 3, 4, 6, 27, 8,
            9, 10, 11, 12, 13, 14, 6, 14
        ],
        'T0_tool0_n_classifications': [
            4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
            4, 4, 4, 4, 4, 4, 4, 4
        ],
        'T0_tool0_shape': [
            'rectangle', 'rectangle', 'rectangle', 'rectangle', 'rectangle',
            'rectangle', 'rectangle', 'rectangle', 'rectangle', 'rectangle',
            'rectangle', 'rectangle', 'rectangle', 'rectangle', 'rectangle',
            'rectangle', 'rectangle', 'rectangle', 'rectangle', 'rectangle',
            'rectangle', 'rectangle', 'rectangle', 'rectangle', 'rectangle',
            'rectangle', 'rectangle', 'rectangle'
        ],
        "T0_tool0_clusters_count": [
            2, 2, 1, 2, 2, 1, 3, 1, 2, 2,
            2, 2, 2, 2, 3, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1
        ],
        "T0_tool0_clusters_x": [
            901.3092651367188, 904.9237060546875, 896.7911987304688, 880.5261840820312,
            887.7550659179688, 867.8756103515625, 870.9708251953125, 893.1767578125,
            903.1165161132812, 894.080322265625, 913.9598388671875, 915.76708984375,
            938.0682373046875, 976.9236450195312, 887.8665161132812, -9.742353439331055,
            423.4798278808594, 1160.939208984375, 883.1085205078125, 1363.4852294921875,
            873.0498046875, 1031.3603515625, 1181.77392578125, 903.3765869140625,
            1185.6890869140625, 891.61962890625, 872.1119384765625, 884.288818359375
        ],
        "T0_tool0_clusters_y": [
            729.5806884765625, 840.72509765625, 940.12255859375, 1035.905517578125,
            1137.1102294921875, 1250.965576171875, 1343.0013427734375, 1462.4110107421875,
            1561.808349609375, 1680.1817626953125, 1766.0250244140625, 1873.554931640625,
            1989.89404296875, 2072.122802734375, 2206.82373046875, -3.116422653198242,
            256.030029296875, 243.6797332763672, 383.2991943359375, 110.43333435058594,
            699.6864013671875, 719.7999877929688, 713.116455078125, 737.5718994140625,
            753.4766235351562, 715.47021484375, 909.5127563476562, 1436.809326171875
        ],
        "T0_tool0_clusters_width": [
            770.7821655273438, 750.902587890625, 728.3123168945312, 774.3965454101562,
            782.5291137695312, 835.84228515625, 816.923095703125, 768.0712890625,
            766.2640991210938, 752.7099609375, 760.8424072265625, 752.7098388671875,
            631.625732421875, 637.0473022460938, 794.4669799804688, 336.03468132019043,
            349.5593566894531, 102.291015625, 48.19427490234375, 50.0760498046875,
            472.5726318359375, 355.8408203125, 488.4212646484375, 276.3695068359375,
            191.9783935546875, 309.0950927734375, 813.3726806640625, 801.8133544921875
        ],
        "T0_tool0_clusters_height": [
            102.1082763671875, 93.975830078125, 110.2408447265625, 114.7589111328125,
            127.409423828125, 84.9395751953125, 99.2750244140625, 110.2408447265625,
            130.120361328125, 72.2891845703125, 95.782958984375, 129.216552734375,
            75.903564453125, 136.44580078125, 78.5068359375, 524.3477458953857,
            113.49136352539062, 94.02519226074219, 96.18414306640625, 82.36686706542969,
            26.27093505859375, 31.686279296875, 9.3726806640625, 24.7528076171875,
            30.563232421875, 120.85577392578125, 103.9720458984375, 94.9967041015625
        ],
        "T0_tool0_clusters_sigma": [
            0.3789732377978776, 0.453660846404056, 0.0, 0.47020357992725637, 0.4616297607454718,
            0.0, 0.3129964078854421, 0.0, 0.4860395843149953,
            0.3550447249953831, 0.11180631928856122, 0.4362014709732337, 0.38420782292669176,
            0.4660228237578812, 0.2946687840505092, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0
        ],
        "T0_tool0_details": [
            [
                {'text': 'Lilley', 'gold_standard': False},
                {'text': '1915-05-05', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Malta', 'gold_standard': False},
                {'text': '1917-05-18', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'J. Lilley &Son', 'gold_standard': False},
                {'text': '1917-12-07', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Cape of Good Hope', 'gold_standard': False},
                {'text': '1918-07-02', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'J Lilley &Son', 'gold_standard': False},
                {'text': '1918-09-20', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'HMS ""Kildare""', 'gold_standard': False},
                {'text': '1919-05-05', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'J Lilly&Son', 'gold_standard': False},
                {'text': '1922-10-13', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'JLilley &Son', 'gold_standard': False},
                {'text': '1923-02-16', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'J Lilley &Son', 'gold_standard': False},
                {'text': '1923-04-27', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Portsmouth', 'gold_standard': False},
                {'text': '1924-03-31', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Sheerness', 'gold_standard': False},
                {'text': '1926-01-27', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Lilley', 'gold_standard': False},
                {'text': '1927-03-31', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Portsmouth', 'gold_standard': False},
                {'text': '1929-12-03', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Lilley', 'gold_standard': False},
                {'text': '1931-03-25', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'V. Kullberg', 'gold_standard': False},
                {'text': '1935-08-30', 'gold_standard': False},
                {'text': '2-16-0', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Lilly', 'gold_standard': False},
                {'text': '1915-05-05', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Malta', 'gold_standard': False},
                {'text': '1914-05-18', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'J. Lilley & Son', 'gold_standard': False},
                {'text': '1914-12-07', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Cape of Good Hope', 'gold_standard': False},
                {'text': '1918-07-02', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'J Lilley & Son', 'gold_standard': False},
                {'text': '1918-09-20', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'J Lilley & Son', 'gold_standard': False},
                {'text': '1922-12-13', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'J Lilley & Son', 'gold_standard': False},
                {'text': '1923-02-07', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'J Lilly & Son', 'gold_standard': False},
                {'text': '1923-04-27', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Portsmouth', 'gold_standard': False},
                {'text': '1924-03-31', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Sheemess', 'gold_standard': False},
                {'text': '1926-01-27', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Lilly', 'gold_standard': False},
                {'text': '1924-05-31', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Portsmouth', 'gold_standard': False},
                {'text': '1919-12-03', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Lilly', 'gold_standard': False},
                {'text': '1931-03-28', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'V. Kullberg (unclear)', 'gold_standard': False},
                {'text': '1935-08-30', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': '(unclear)Steve Vildare(unclear)', 'gold_standard': False},
                {'text': '1919-05-05', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'V Kullberg ', 'gold_standard': False},
                {'text': '1935-08-30', 'gold_standard': False},
                {'text': '2-16-0', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],

        ],
    }
}


TestRectReducerEmptySubtasksClustersOfOne = ReducerTestNoProcessing(
    shape_reducer_dbscan,
    extracted_data_empty_subtasks_clusters_of_one,
    reduced_data_empty_subtasks_clusters_of_one,
    'Test rectangle reducer with six clusters of one that have empty subtasks',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'eps': 0.5,
        'min_samples': 1,
        'metric_type': 'IoU',
        'estimate_average': True,
        'shape': 'rectangle',
        'details': {
            'T0_tool0': [
                'text_reducer',
                'text_reducer',
                'text_reducer',
                'text_reducer'
            ]
        }
    },
    test_name='TestShapeReducerRectangleClustersOfOneWithEmptySubtasks'
)


extracted_data_cluster_with_empty_subtask = [
    {
        "frame0": {
            "T0_tool0_x": [
                395.15679931640625, 394.6253662109375, 391.43670654296875,
                397.2825622558594, 398.3454284667969, 399.93975830078125,
                405.2541809082031, 397.8139953613281
            ],
            "T0_tool0_y": [
                312.8265380859375, 355.3418273925781, 399.98284912109375,
                440.90380859375, 491.9221496582031, 538.68896484375,
                576.4212646484375, 622.6566162109375
            ],
            "T0_tool0_width": [
                323.6475830078125, 319.39599609375, 315.14447021484375,
                320.4588928222656, 316.7388000488281, 318.86456298828125,
                321.5217590332031, 334.2763977050781
            ],
            "T0_tool0_height": [
                34.54364013671875, 45.70391845703125, 39.326629638671875,
                54.20697021484375, 44.641021728515625, 41.452392578125,
                50.4869384765625, 59.52142333984375
            ],
            "T0_tool0_details": [
                [],
                [
                    {'text': 'Milford Haven', 'gold_standard': False},
                    {'text': '1916-07-13', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Williamson', 'gold_standard': False},
                    {'text': '1916-08-05', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Rosyth', 'gold_standard': False},
                    {'text': '1917-04-25', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Williamson', 'gold_standard': False},
                    {'text': '1917-05-19', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Portsmouth', 'gold_standard': False},
                    {'text': '1918-05-04', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Williamson', 'gold_standard': False},
                    {'text': '1918-06-15', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'S.N.O. Grimaldy', 'gold_standard': False},
                    {'text': '1919-11-25', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ]
            ],
        }
    },
    {
        "frame0": {
            "T0_tool0_x": [
                395.81158447265625, 393.8092041015625, 395.81158447265625,
                396.8127746582031, 401.8187255859375, 406.8246765136719,
                405.823486328125, 396.8127746582031
            ],
            "T0_tool0_y": [
                309.3208312988281, 358.379150390625, 405.43505859375,
                445.482666015625, 492.5386047363281, 537.5921630859375,
                588.6528930664062, 626.6981201171875
            ],
            "T0_tool0_width": [
                338.40228271484375, 337.40106201171875, 338.40228271484375,
                324.3855895996094, 325.38677978515625, 325.3868103027344,
                332.3951416015625, 353.4201354980469
            ],
            "T0_tool0_height": [
                46.05474853515625, 40.047576904296875, 34.04046630859375,
                41.048797607421875, 42.050018310546875, 43.05120849609375,
                32.0380859375, 53.06304931640625
            ],
            "T0_tool0_details": [
                [
                    {'text': 'Williamson', 'gold_standard': False},
                    {'text': '1915-12-04', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Milford Haven', 'gold_standard': False},
                    {'text': '1916-07-13', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Williamson', 'gold_standard': False},
                    {'text': '1916-08-05', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Rosyth', 'gold_standard': False},
                    {'text': '1917-04-25', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Williamson', 'gold_standard': False},
                    {'text': '1917-05-19', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Portsmouth', 'gold_standard': False},
                    {'text': '1918-05-04', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Williamson', 'gold_standard': False},
                    {'text': '1918-06-15', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'S.N.O. Grimsby', 'gold_standard': False},
                    {'text': '1919-11-25', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ]
            ],
        }
    },
    {
        "frame0": {
            "T0_tool0_x": [
                401.36431884765625, 395.5323181152344, 402.09332275390625,
                407.9253234863281, 408.6543273925781, 410.1123046875,
                410.84130859375, 404.2803039550781
            ],
            "T0_tool0_y": [
                313.8993225097656, 356.91033935546875, 403.56634521484375,
                446.57733154296875, 496.8783264160156, 542.0763549804688,
                584.3583374023438, 628.8273315429688
            ],
            "T0_tool0_width": [
                311.28302001953125, 317.8439636230469, 303.99298095703125,
                305.4509582519531, 298.8899841308594, 298.1610107421875,
                312.74102783203125, 321.4889831542969
            ],
            "T0_tool0_height": [
                29.889007568359375, 39.365997314453125, 29.88897705078125,
                40.824005126953125, 37.907989501953125, 34.26300048828125,
                37.17901611328125, 43.739990234375
            ],
            "T0_tool0_details": [
                [
                    {'text': 'Williamson', 'gold_standard': False},
                    {'text': '1915-12-04', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Milford Haven', 'gold_standard': False},
                    {'text': '1916-07-13', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Williamson', 'gold_standard': False},
                    {'text': '1916-08-05', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Rosyth', 'gold_standard': False},
                    {'text': '1917-04-25', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Williamson', 'gold_standard': False},
                    {'text': '1917-05-09', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Portsmouth', 'gold_standard': False},
                    {'text': '1918-05-04', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'Williamson', 'gold_standard': False},
                    {'text': '1918-06-15', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ],
                [
                    {'text': 'S.V.O. Grimsby', 'gold_standard': False},
                    {'text': '1919-11-25', 'gold_standard': False},
                    {'text': '', 'gold_standard': False},
                    {'text': '', 'gold_standard': False}
                ]
            ],
        }
    },
]

reduced_data_cluster_with_empty_subtask = {
    "frame0": {
        "T0_tool0_rectangle_x": [
            395.15679931640625, 394.6253662109375, 391.43670654296875,
            397.2825622558594, 398.3454284667969, 399.93975830078125,
            405.2541809082031, 397.8139953613281, 395.81158447265625,
            393.8092041015625, 395.81158447265625, 396.8127746582031,
            401.8187255859375, 406.8246765136719, 405.823486328125,
            396.8127746582031, 401.36431884765625, 395.5323181152344,
            402.09332275390625, 407.9253234863281, 408.6543273925781,
            410.1123046875, 410.84130859375, 404.2803039550781
        ],
        "T0_tool0_rectangle_y": [
            312.8265380859375, 355.3418273925781, 399.98284912109375,
            440.90380859375, 491.9221496582031, 538.68896484375,
            576.4212646484375, 622.6566162109375, 309.3208312988281,
            358.379150390625, 405.43505859375, 445.482666015625,
            492.5386047363281, 537.5921630859375, 588.6528930664062,
            626.6981201171875, 313.8993225097656, 356.91033935546875,
            403.56634521484375, 446.57733154296875, 496.8783264160156,
            542.0763549804688, 584.3583374023438, 628.8273315429688
        ],
        "T0_tool0_rectangle_width": [
            323.6475830078125, 319.39599609375, 315.14447021484375,
            320.4588928222656, 316.7388000488281, 318.86456298828125,
            321.5217590332031, 334.2763977050781, 338.40228271484375,
            337.40106201171875, 338.40228271484375, 324.3855895996094,
            325.38677978515625, 325.3868103027344, 332.3951416015625,
            353.4201354980469, 311.28302001953125, 317.8439636230469,
            303.99298095703125, 305.4509582519531, 298.8899841308594,
            298.1610107421875, 312.74102783203125, 321.4889831542969

        ],
        "T0_tool0_rectangle_height": [
            34.54364013671875, 45.70391845703125, 39.326629638671875,
            54.20697021484375, 44.641021728515625, 41.452392578125,
            50.4869384765625, 59.52142333984375, 46.05474853515625,
            40.047576904296875, 34.04046630859375, 41.048797607421875,
            42.050018310546875, 43.05120849609375, 32.0380859375,
            53.06304931640625, 29.889007568359375, 39.365997314453125,
            29.88897705078125, 40.824005126953125, 37.907989501953125,
            34.26300048828125, 37.17901611328125, 43.739990234375
        ],
        "T0_tool0_cluster_labels": [
            0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4,
            5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7
        ],
        "T0_tool0_clusters_count": [
            3, 3, 3, 3, 3, 3, 3, 3
        ],
        "T0_tool0_n_classifications": [
            3, 3, 3, 3, 3, 3, 3, 3
        ],
        "T0_tool0_shape": [
            'rectangle', 'rectangle', 'rectangle', 'rectangle', 'rectangle',
            'rectangle', 'rectangle', 'rectangle'
        ],
        "T0_tool0_clusters_x": [
            395.15679931640625, 395.5323181152344, 391.43670654296875,
            396.8127746582031, 401.8187255859375, 399.93975830078125,
            410.84130859375, 396.8127746582031
        ],
        "T0_tool0_clusters_y": [
            312.8265380859375, 356.91033935546875, 399.98284912109375,
            445.482666015625, 492.5386047363281, 538.68896484375,
            584.3583374023438, 626.6981201171875
        ],
        "T0_tool0_clusters_width": [
            323.6475830078125, 317.8439636230469, 315.14447021484375,
            324.3855895996094, 325.38677978515625, 318.86456298828125,
            312.74102783203125, 353.4201354980469
        ],
        "T0_tool0_clusters_height": [
            34.54364013671875, 39.365997314453125, 39.326629638671875,
            41.048797607421875, 42.050018310546875, 41.452392578125,
            37.17901611328125, 53.06304931640625
        ],
        "T0_tool0_clusters_sigma": [
            0.23394466009520068, 0.14060733263477962, 0.24169162128055466,
            0.19057187422567212, 0.1457329023562676, 0.17413816388776374,
            0.23854725775033608, 0.20692086799701523
        ],
        "T0_tool0_details": [
            [
                {'text': 'Milford Haven', 'gold_standard': False},
                {'text': '1916-07-13', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Williamson', 'gold_standard': False},
                {'text': '1916-08-05', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Rosyth', 'gold_standard': False},
                {'text': '1917-04-25', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Williamson', 'gold_standard': False},
                {'text': '1917-05-19', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Portsmouth', 'gold_standard': False},
                {'text': '1918-05-04', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Williamson', 'gold_standard': False},
                {'text': '1918-06-15', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'S.N.O. Grimaldy', 'gold_standard': False},
                {'text': '1919-11-25', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Williamson', 'gold_standard': False},
                {'text': '1915-12-04', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Milford Haven', 'gold_standard': False},
                {'text': '1916-07-13', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Williamson', 'gold_standard': False},
                {'text': '1916-08-05', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Rosyth', 'gold_standard': False},
                {'text': '1917-04-25', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Williamson', 'gold_standard': False},
                {'text': '1917-05-19', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Portsmouth', 'gold_standard': False},
                {'text': '1918-05-04', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Williamson', 'gold_standard': False},
                {'text': '1918-06-15', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'S.N.O. Grimsby', 'gold_standard': False},
                {'text': '1919-11-25', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Williamson', 'gold_standard': False},
                {'text': '1915-12-04', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Milford Haven', 'gold_standard': False},
                {'text': '1916-07-13', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Williamson', 'gold_standard': False},
                {'text': '1916-08-05', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Rosyth', 'gold_standard': False},
                {'text': '1917-04-25', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Williamson', 'gold_standard': False},
                {'text': '1917-05-09', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Portsmouth', 'gold_standard': False},
                {'text': '1918-05-04', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'Williamson', 'gold_standard': False},
                {'text': '1918-06-15', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ],
            [
                {'text': 'S.V.O. Grimsby', 'gold_standard': False},
                {'text': '1919-11-25', 'gold_standard': False},
                {'text': '', 'gold_standard': False},
                {'text': '', 'gold_standard': False}
            ]
        ],
    }
}

TestRectReducerOneEmptySubtasks = ReducerTestNoProcessing(
    shape_reducer_dbscan,
    extracted_data_cluster_with_empty_subtask,
    reduced_data_cluster_with_empty_subtask,
    'Test rectangle reducer with a cluster with both empty and non-empty subtasks',
    network_kwargs=kwargs_extra_data,
    kwargs={
        'eps': 0.5,
        'min_samples': 1,
        'metric_type': 'IoU',
        'estimate_average': True,
        'shape': 'rectangle',
        'details': {
            'T0_tool0': [
                'text_reducer',
                'text_reducer',
                'text_reducer',
                'text_reducer'
            ]
        }
    },
    test_name='TestShapeReducerRectangleClusterWithEmptySubtask'
)
