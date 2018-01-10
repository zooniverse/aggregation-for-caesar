from panoptes_aggregation.reducers.rectangle_reducer import process_data, rectangle_reducer
from .base_test_class import ReducerTest

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
    kwargs={
        'eps': 5,
        'min_samples': 2
    }
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
    kwargs={
        'eps': 5,
        'min_samples': 2
    }
)
