# Tess uses classifier v2.0 with a shape_extractor and no subtasks
# it is also does not have `taskType: drawing`
# ensure the subtask wrapper passes it along correctly
from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    'annotations': [{
        'task': 'T1',
        'value': [{
            'x': 15,
            'tool': 0,
            'width': 0.92,
            'toolType': 'graph2dRangeX',
            'zoomLevelOnCreation': 1
        }],
        'taskType': 'dataVisAnnotation'
    }],
    'metadata': {
        'classifier_version': '2.0'
    }
}

expected = {
    'classifier_version': '2.0',
    'frame0': {
        'T1_tool0_x': [15],
        'T1_tool0_width': [0.92],
    }
}

TestShapeColumnTess = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape column for TESS v2.0 classification',
    kwargs={'shape': 'column'},
    test_name='TestShapeColumnTess'
)

TestShapeColumnTaskTess = ExtractorTest(
    extractors.shape_extractor,
    classification,
    expected,
    'Test shape column with task specified for TESS v2.0 classification',
    kwargs={
        'shape': 'column',
        'task': 'T1'
    },
    test_name='TestShapeColumnTaskTess'
)
