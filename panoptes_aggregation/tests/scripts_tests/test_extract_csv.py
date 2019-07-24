import unittest
from unittest.mock import patch, MagicMock, call
from io import StringIO
import os
import pandas
from pandas.util.testing import assert_frame_equal
import panoptes_aggregation.scripts.extract_panoptes_csv as extract_panoptes_csv

classification_data_dump_two_tasks = '''classification_id,user_name,user_id,workflow_id,workflow_version,created_at,annotations,subject_ids
1,1,1,4249,14.18,2017-05-31 12:33:46 UTC,"[{""task"":""T0""},{""task"":""T1""}]",1
2,2,2,4249,14.18,2017-05-31 12:33:51 UTC,"[{""task"":""T0""},{""task"":""T1""}]",1
'''

extractor_config_yaml_question = '''{
    'workflow_id': 4249,
    'workflow_version': '14.18',
    'extractor_config': {'question_extractor': [{'task': 'T0'}, {'task': 'T1'}]}
}'''

extracted_csv_question = '''classification_id,user_name,user_id,workflow_id,task,created_at,subject_id,extractor,data.blue,data.green,data.no,data.yes
1,1,1,4249,T0,2017-05-31 12:33:46 UTC,1,question_extractor,,,,1.0
1,1,1,4249,T1,2017-05-31 12:33:46 UTC,1,question_extractor,1.0,1.0,,
2,2,2,4249,T0,2017-05-31 12:33:51 UTC,1,question_extractor,,,1.0,
2,2,2,4249,T1,2017-05-31 12:33:51 UTC,1,question_extractor,,,,
'''

classification_data_dump_one_task = '''classification_id,user_name,user_id,workflow_id,workflow_version,created_at,annotations,subject_ids
1,1,1,4249,14.18,2017-05-31 12:33:46 UTC,"[{""task"":""T0""}]",1
2,2,2,4249,14.18,2017-05-31 12:33:51 UTC,"[{""task"":""T0""}]",1
'''

extractor_config_yaml_survey = '''{
    'workflow_id': 4249,
    'workflow_version': '14',
    'extractor_config': {'survey_extractor': [{'task': 'T0'}]}
}'''

extracted_csv_survey = '''classification_id,user_name,user_id,workflow_id,task,created_at,subject_id,extractor,data.choice,data.answers_howmany.1,data.answers_howmany.3,data.answers_howmany.4
1,1,1,4249,T0,2017-05-31 12:33:46 UTC,1,survey_extractor,dog,1.0,,
1,1,1,4249,T0,2017-05-31 12:33:46 UTC,1,survey_extractor,cat,,1.0,
2,2,2,4249,T0,2017-05-31 12:33:51 UTC,1,survey_extractor,cat,,,1.0
'''

extractor_config_yaml_two = '''{
    'workflow_id': 4249,
    'workflow_version': '14.18',
    'extractor_config': {
        'shape_extractor_rectangle': [{'task': 'T0'}],
        'shape_extractor_point': [{'task': 'T1'}]
    }
}'''

extracted_csv_two_T1 = '''classification_id,user_name,user_id,workflow_id,task,created_at,subject_id,extractor,data.no,data.yes
1,1,1,4249,T1,2017-05-31 12:33:46 UTC,1,shape_extractor_point,,1.0
2,2,2,4249,T1,2017-05-31 12:33:51 UTC,1,shape_extractor_point,1.0,
'''

extracted_csv_two_T0 = '''classification_id,user_name,user_id,workflow_id,task,created_at,subject_id,extractor,data.no,data.yes
1,1,1,4249,T0,2017-05-31 12:33:46 UTC,1,shape_extractor_rectangle,,1.0
2,2,2,4249,T0,2017-05-31 12:33:51 UTC,1,shape_extractor_rectangle,1.0,
'''

extractor_config_yaml_fail = '''{
    'workflow_id': 4249,
    'workflow_version': '14.18',
    'extractor_config': {
        'bad_extractor': [{'task': 'T0'}]
    }
}'''


class CaptureValues(object):
    def __init__(self, func):
        self.func = func
        self.return_values = []

    def __call__(self, *args, **kwargs):
        answer = self.func(*args, **kwargs)
        self.return_values.append(answer)
        return answer


mock_question_extractor = MagicMock()
mock_question_extractor.side_effect = [
    {'yes': 1},
    {'blue': 1, 'green': 1},
    {'no': 1},
    {},
]

mock_shape_extractor = MagicMock()
mock_shape_extractor.side_effect = [
    {'yes': 1},
    {'yes': 1},
    {'no': 1},
    {'no': 1},
]


mock_survey_extractor = MagicMock()
mock_survey_extractor.side_effect = [
    [
        {
            'choice': 'dog',
            'answers_howmany': {'1': 1}
        },
        {
            'choice': 'cat',
            'answers_howmany': {'3': 1}
        },
    ],
    [
        {
            'choice': 'cat',
            'answers_howmany': {'4': 1}
        },
    ]
]

mock_bad_extractor = MagicMock()
mock_bad_extractor.side_effect = [
    Exception(),
    Exception(),
    Exception(),
    Exception()
]

mock_extractors_dict = {
    'question_extractor': mock_question_extractor,
    'shape_extractor': mock_shape_extractor,
    'survey_extractor': mock_survey_extractor,
    'bad_extractor': mock_bad_extractor
}


class TestExtractCSV(unittest.TestCase):
    def setUp(self):
        self.classification_data_dump_two_tasks = StringIO(classification_data_dump_two_tasks)
        self.config_yaml_question = StringIO(extractor_config_yaml_question)
        self.extracts_dataframe_question = pandas.read_csv(StringIO(extracted_csv_question))
        self.classification_data_dump_one_task = StringIO(classification_data_dump_one_task)
        self.config_yaml_survey = StringIO(extractor_config_yaml_survey)
        self.extracts_dataframe_survey = pandas.read_csv(StringIO(extracted_csv_survey))
        self.config_yaml_two = StringIO(extractor_config_yaml_two)
        self.extracts_dataframe_two_T0 = pandas.read_csv(StringIO(extracted_csv_two_T0))
        self.extracts_dataframe_two_T1 = pandas.read_csv(StringIO(extracted_csv_two_T1))
        self.config_yaml_fail = StringIO(extractor_config_yaml_fail)

    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.extract_panoptes_csv.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.flatten_data', CaptureValues(extract_panoptes_csv.flatten_data))
    def test_extract_csv_object(self, mock_to_csv, mock_pbar):
        '''Test one (object) extractor makes one csv file'''
        output_file_names = extract_panoptes_csv.extract_csv(
            self.classification_data_dump_two_tasks,
            self.config_yaml_question
        )
        output_path = os.path.join(os.getcwd(), 'question_extractor_extractions.csv')
        self.assertEqual(output_file_names, [output_path])
        result_dataframe = extract_panoptes_csv.flatten_data.return_values[0]
        assert_frame_equal(result_dataframe, self.extracts_dataframe_question, check_like=True)
        mock_to_csv.assert_called_once_with(output_path, index=False, encoding='utf-8')

    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.extract_panoptes_csv.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.order_columns', CaptureValues(extract_panoptes_csv.order_columns))
    def test_extract_csv_list(self, mock_to_csv, mock_pbar):
        '''Test one (list) extractor makes one csv file'''
        output_file_names = extract_panoptes_csv.extract_csv(
            self.classification_data_dump_one_task,
            self.config_yaml_survey,
            order=True
        )
        output_path = os.path.join(os.getcwd(), 'survey_extractor_extractions.csv')
        self.assertEqual(output_file_names, [output_path])
        result_dataframe = extract_panoptes_csv.order_columns.return_values[0]
        assert_frame_equal(result_dataframe, self.extracts_dataframe_survey)
        mock_to_csv.assert_called_once_with(output_path, index=False, encoding='utf-8')

    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.extract_panoptes_csv.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.flatten_data', CaptureValues(extract_panoptes_csv.flatten_data))
    def test_extract_csv_object_shape(self, mock_to_csv, mock_pbar):
        '''Test two (object) extractors makes two csv files'''
        output_file_names = extract_panoptes_csv.extract_csv(
            self.classification_data_dump_two_tasks,
            self.config_yaml_two
        )
        output_path_T0 = os.path.join(os.getcwd(), 'shape_extractor_point_extractions.csv')
        output_path_T1 = os.path.join(os.getcwd(), 'shape_extractor_rectangle_extractions.csv')
        self.assertCountEqual(output_file_names, [output_path_T0, output_path_T1])
        if extract_panoptes_csv.flatten_data.return_values[0].task.iloc[0] == 'T0':
            result_dataframe_T0 = extract_panoptes_csv.flatten_data.return_values[0]
            result_dataframe_T1 = extract_panoptes_csv.flatten_data.return_values[1]
        else:
            result_dataframe_T1 = extract_panoptes_csv.flatten_data.return_values[0]
            result_dataframe_T0 = extract_panoptes_csv.flatten_data.return_values[1]
        assert_frame_equal(result_dataframe_T0, self.extracts_dataframe_two_T0, check_like=True)
        assert_frame_equal(result_dataframe_T1, self.extracts_dataframe_two_T1, check_like=True)
        to_csv_calls = [
            call(output_path_T0, index=False, encoding='utf-8'),
            call(output_path_T1, index=False, encoding='utf-8')
        ]
        mock_to_csv.assert_has_calls(to_csv_calls, any_order=True)

    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.extract_panoptes_csv.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.print')
    def test_extract_csv_bad_classification_verbose(self, mock_print, mock_to_csv, mock_pbar):
        '''Test bad classification with verbose on'''
        output_file_names = extract_panoptes_csv.extract_csv(
            self.classification_data_dump_one_task,
            self.config_yaml_fail,
            verbose=True
        )
        mock_print.assert_any_call('Incorrectly formatted annotation')
        self.assertEqual(output_file_names, [])

    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.extract_panoptes_csv.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.print')
    def test_extract_csv_bad_classification_no_verbose(self, mock_print, mock_to_csv, mock_pbar):
        '''Test bad classification with verbose off'''
        output_file_names = extract_panoptes_csv.extract_csv(
            self.classification_data_dump_one_task,
            self.config_yaml_fail,
            verbose=False
        )
        mock_print.assert_not_called()
        self.assertEqual(output_file_names, [])
