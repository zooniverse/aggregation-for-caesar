import unittest
from unittest.mock import patch, MagicMock, call
from io import StringIO
import os
import pandas
from pandas.testing import assert_frame_equal
import panoptes_aggregation.scripts.extract_panoptes_csv as extract_panoptes_csv
import panoptes_aggregation.scripts.batch_utils as batch_utils
import platform
import multiprocessing

if platform.system() == 'Windows':
    WINDOWS = True
else:
    WINDOWS = False

classification_data_dump_two_tasks = '''classification_id,user_name,user_id,workflow_id,workflow_version,created_at,annotations,subject_ids,metadata
1,1,1,4249,13.1,2017-05-20 1:33:46 UTC,"[{""task"":""T0""},{""task"":""T1""}]",1,"{}"
2,1,1,4249,14.1,2017-05-25 2:33:46 UTC,"[{""task"":""T0""},{""task"":""T1""}]",1,"{}"
3,1,1,4249,14.18,2017-05-31 12:33:46 UTC,"[{""task"":""T0""},{""task"":""T1""}]",1,"{}"
4,2,2,4249,14.18,2017-05-31 12:33:51 UTC,"[{""task"":""T0""},{""task"":""T1""}]",1,"{}"
'''

extractor_config_yaml_question = '''{
    'workflow_id': 4249,
    'workflow_version': '14.18',
    'extractor_config': {'question_extractor': [{'task': 'T0'}, {'task': 'T1'}]}
}'''

extracted_csv_question = '''classification_id,user_name,user_id,workflow_id,task,created_at,subject_id,extractor,data.blue,data.green,data.no,data.yes
3,1,1,4249,T0,2017-05-31 12:33:46 UTC,1,question_extractor,,,,1.0
3,1,1,4249,T1,2017-05-31 12:33:46 UTC,1,question_extractor,1.0,1.0,,
4,2,2,4249,T0,2017-05-31 12:33:51 UTC,1,question_extractor,,,1.0,
4,2,2,4249,T1,2017-05-31 12:33:51 UTC,1,question_extractor,,,,
'''

extractor_config_yaml_question_min = '''{
    'workflow_id': 4249,
    'workflow_version': {
        min: '14.1'
    },
    'extractor_config': {'question_extractor': [{'task': 'T0'}, {'task': 'T1'}]}
}'''

extracted_csv_question_min = '''classification_id,user_name,user_id,workflow_id,task,created_at,subject_id,extractor,data.blue,data.green,data.no,data.yes
2,1,1,4249,T0,2017-05-25 2:33:46 UTC,1,question_extractor,,,,1.0
2,1,1,4249,T1,2017-05-25 2:33:46 UTC,1,question_extractor,1.0,1.0,,
3,1,1,4249,T0,2017-05-31 12:33:46 UTC,1,question_extractor,,,,1.0
3,1,1,4249,T1,2017-05-31 12:33:46 UTC,1,question_extractor,1.0,1.0,,
4,2,2,4249,T0,2017-05-31 12:33:51 UTC,1,question_extractor,,,1.0,
4,2,2,4249,T1,2017-05-31 12:33:51 UTC,1,question_extractor,,,,
'''

extractor_config_yaml_question_max = '''{
    'workflow_id': 4249,
    'workflow_version': {
        max: '14.1'
    },
    'extractor_config': {'question_extractor': [{'task': 'T0'}, {'task': 'T1'}]}
}'''

extracted_csv_question_max = '''classification_id,user_name,user_id,workflow_id,task,created_at,subject_id,extractor,data.blue,data.green,data.yes
1,1,1,4249,T0,2017-05-20 1:33:46 UTC,1,question_extractor,,,1.0
1,1,1,4249,T1,2017-05-20 1:33:46 UTC,1,question_extractor,1.0,1.0,
2,1,1,4249,T0,2017-05-25 2:33:46 UTC,1,question_extractor,,,1.0
2,1,1,4249,T1,2017-05-25 2:33:46 UTC,1,question_extractor,1.0,1.0,
'''

classification_data_dump_one_task = '''classification_id,user_name,user_id,workflow_id,workflow_version,created_at,annotations,subject_ids,metadata
1,1,1,4249,14.1,2017-05-31 12:33:46 UTC,"[{""task"":""T0""}]",1,"{}"
2,2,2,4249,14.18,2017-05-31 12:33:51 UTC,"[{""task"":""T0""}]",1,"{}"
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
3,1,1,4249,T1,2017-05-31 12:33:46 UTC,1,shape_extractor_point,,1.0
4,2,2,4249,T1,2017-05-31 12:33:51 UTC,1,shape_extractor_point,1.0,
'''

extracted_csv_two_T0 = '''classification_id,user_name,user_id,workflow_id,task,created_at,subject_id,extractor,data.no,data.yes
3,1,1,4249,T0,2017-05-31 12:33:46 UTC,1,shape_extractor_rectangle,,1.0
4,2,2,4249,T0,2017-05-31 12:33:51 UTC,1,shape_extractor_rectangle,1.0,
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
mock_shape_extractor = MagicMock()
mock_survey_extractor = MagicMock()
mock_bad_extractor = MagicMock()

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

        self.config_yaml_question_min = StringIO(extractor_config_yaml_question_min)
        self.extracts_dataframe_question_min = pandas.read_csv(StringIO(extracted_csv_question_min))

        self.config_yaml_question_max = StringIO(extractor_config_yaml_question_max)
        self.extracts_dataframe_question_max = pandas.read_csv(StringIO(extracted_csv_question_max))

        self.config_yaml_survey = StringIO(extractor_config_yaml_survey)
        self.extracts_dataframe_survey = pandas.read_csv(StringIO(extracted_csv_survey))

        self.config_yaml_two = StringIO(extractor_config_yaml_two)
        self.extracts_dataframe_two_T0 = pandas.read_csv(StringIO(extracted_csv_two_T0))
        self.extracts_dataframe_two_T1 = pandas.read_csv(StringIO(extracted_csv_two_T1))

        self.config_yaml_fail = StringIO(extractor_config_yaml_fail)

    @patch('panoptes_aggregation.scripts.batch_utils.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.batch_utils.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.batch_utils.flatten_data', CaptureValues(batch_utils.flatten_data))
    def test_extract_csv_object(self, mock_to_csv, *_):
        '''Test one (object) extractor makes one csv file'''
        mock_question_extractor.side_effect = [
            {'yes': 1},
            {'blue': 1, 'green': 1},
            {'no': 1},
            {}
        ]
        output_file_names = extract_panoptes_csv.extract_csv(
            self.classification_data_dump_two_tasks,
            self.config_yaml_question,
            cpu_count=1
        )
        output_path = os.path.join(os.getcwd(), 'question_extractor_extractions.csv')
        self.assertEqual(output_file_names, [output_path])
        result_dataframe = batch_utils.flatten_data.return_values[0]
        assert_frame_equal(result_dataframe, self.extracts_dataframe_question, check_like=True)
        mock_to_csv.assert_called_once_with(output_path, index=False, encoding='utf-8')

    @unittest.skipIf(WINDOWS, 'Installed on windows, skipping multi core test')
    @patch('panoptes_aggregation.scripts.batch_utils.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.batch_utils.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.batch_utils.flatten_data', CaptureValues(batch_utils.flatten_data))
    def test_extract_csv_object_n2(self, mock_to_csv, *_):
        '''Test one (object) extractor makes one csv file with cpu_count==2'''
        mock_question_extractor.side_effect = [
            {'yes': 1},
            {'blue': 1, 'green': 1},
            {'no': 1},
            {}
        ]
        # on Mac's the multiprocessing start method needs to be set to 'fork' rather than 'spawn'
        # https://stackoverflow.com/a/70440892/1052418
        start_method = multiprocessing.get_start_method()
        multiprocessing.set_start_method('fork', force=True)
        output_file_names = extract_panoptes_csv.extract_csv(
            self.classification_data_dump_two_tasks,
            self.config_yaml_question,
            cpu_count=2,
            verbose=True
        )
        output_path = os.path.join(os.getcwd(), 'question_extractor_extractions.csv')
        self.assertEqual(output_file_names, [output_path])
        mock_to_csv.assert_called_once_with(output_path, index=False, encoding='utf-8')
        # set back to default
        multiprocessing.set_start_method(start_method, force=True)

    @patch('panoptes_aggregation.scripts.batch_utils.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.batch_utils.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.batch_utils.flatten_data', CaptureValues(batch_utils.flatten_data))
    def test_extract_csv_object_min_version(self, mock_to_csv, *_):
        '''Test one (object) extractor makes one csv file with min_version'''
        mock_question_extractor.side_effect = [
            {'yes': 1},
            {'blue': 1, 'green': 1},
            {'yes': 1},
            {'blue': 1, 'green': 1},
            {'no': 1},
            {}
        ]
        output_file_names = extract_panoptes_csv.extract_csv(
            self.classification_data_dump_two_tasks,
            self.config_yaml_question_min,
            cpu_count=1
        )
        output_path = os.path.join(os.getcwd(), 'question_extractor_extractions.csv')
        self.assertEqual(output_file_names, [output_path])
        result_dataframe = batch_utils.flatten_data.return_values[0]
        assert_frame_equal(result_dataframe, self.extracts_dataframe_question_min, check_like=True)
        mock_to_csv.assert_called_once_with(output_path, index=False, encoding='utf-8')

    @patch('panoptes_aggregation.scripts.batch_utils.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.batch_utils.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.batch_utils.flatten_data', CaptureValues(batch_utils.flatten_data))
    def test_extract_csv_object_max_version(self, mock_to_csv, *_):
        '''Test one (object) extractor makes one csv file with max_version'''
        mock_question_extractor.side_effect = [
            {'yes': 1},
            {'blue': 1, 'green': 1},
            {'yes': 1},
            {'blue': 1, 'green': 1}
        ]
        output_file_names = extract_panoptes_csv.extract_csv(
            self.classification_data_dump_two_tasks,
            self.config_yaml_question_max,
            cpu_count=1
        )
        output_path = os.path.join(os.getcwd(), 'question_extractor_extractions.csv')
        self.assertEqual(output_file_names, [output_path])
        result_dataframe = batch_utils.flatten_data.return_values[0]
        assert_frame_equal(result_dataframe, self.extracts_dataframe_question_max, check_like=True)
        mock_to_csv.assert_called_once_with(output_path, index=False, encoding='utf-8')

    @patch('panoptes_aggregation.scripts.batch_utils.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.batch_utils.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.order_columns', CaptureValues(extract_panoptes_csv.order_columns))
    def test_extract_csv_list(self, mock_to_csv, *_):
        '''Test one (list) extractor makes one csv file'''
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
        output_file_names = extract_panoptes_csv.extract_csv(
            self.classification_data_dump_one_task,
            self.config_yaml_survey,
            order=True,
            cpu_count=1
        )
        output_path = os.path.join(os.getcwd(), 'survey_extractor_extractions.csv')
        self.assertEqual(output_file_names, [output_path])
        result_dataframe = extract_panoptes_csv.order_columns.return_values[0]
        assert_frame_equal(result_dataframe, self.extracts_dataframe_survey)
        mock_to_csv.assert_called_once_with(output_path, index=False, encoding='utf-8')

    @patch('panoptes_aggregation.scripts.batch_utils.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.batch_utils.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.batch_utils.flatten_data', CaptureValues(batch_utils.flatten_data))
    def test_extract_csv_object_shape(self, mock_to_csv, *_):
        '''Test two (object) extractors makes two csv files'''
        mock_shape_extractor.side_effect = [
            {'yes': 1},
            {'yes': 1},
            {'no': 1},
            {'no': 1},
        ]
        output_file_names = extract_panoptes_csv.extract_csv(
            self.classification_data_dump_two_tasks,
            self.config_yaml_two,
            cpu_count=1
        )
        output_path_T0 = os.path.join(os.getcwd(), 'shape_extractor_point_extractions.csv')
        output_path_T1 = os.path.join(os.getcwd(), 'shape_extractor_rectangle_extractions.csv')
        self.assertCountEqual(output_file_names, [output_path_T0, output_path_T1])
        if batch_utils.flatten_data.return_values[0].task.iloc[0] == 'T0':
            result_dataframe_T0 = batch_utils.flatten_data.return_values[0]
            result_dataframe_T1 = batch_utils.flatten_data.return_values[1]
        else:
            result_dataframe_T1 = batch_utils.flatten_data.return_values[0]
            result_dataframe_T0 = batch_utils.flatten_data.return_values[1]
        assert_frame_equal(result_dataframe_T0, self.extracts_dataframe_two_T0, check_like=True)
        assert_frame_equal(result_dataframe_T1, self.extracts_dataframe_two_T1, check_like=True)
        to_csv_calls = [
            call(output_path_T0, index=False, encoding='utf-8'),
            call(output_path_T1, index=False, encoding='utf-8')
        ]
        mock_to_csv.assert_has_calls(to_csv_calls, any_order=True)

    @patch('panoptes_aggregation.scripts.batch_utils.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.batch_utils.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.batch_utils.print')
    def test_extract_csv_bad_classification_verbose(self, mock_print, *_):
        '''Test bad classification with verbose on'''
        mock_bad_extractor.side_effect = [
            Exception(),
            Exception()
        ]
        output_file_names = extract_panoptes_csv.extract_csv(
            self.classification_data_dump_one_task,
            self.config_yaml_fail,
            verbose=True,
            cpu_count=1
        )
        mock_print.assert_any_call('Incorrectly formatted annotation')
        self.assertEqual(output_file_names, [])

    @patch('panoptes_aggregation.scripts.batch_utils.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.batch_utils.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.batch_utils.print')
    def test_extract_csv_bad_classification_no_verbose(self, mock_print, *_):
        '''Test bad classification with verbose off'''
        mock_bad_extractor.side_effect = [
            Exception(),
            Exception()
        ]
        output_file_names = extract_panoptes_csv.extract_csv(
            self.classification_data_dump_one_task,
            self.config_yaml_fail,
            verbose=False,
            cpu_count=1
        )
        mock_print.assert_not_called()
        self.assertEqual(output_file_names, [])

    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch('panoptes_aggregation.scripts.batch_utils.progressbar.ProgressBar')
    @patch.dict('panoptes_aggregation.scripts.batch_utils.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.batch_utils.flatten_data', CaptureValues(batch_utils.flatten_data))
    def test_extract_csv_object_no_progress_bar(self, mock_progress_bar, *_):
        '''Test to make sure progress is not displayed'''
        mock_question_extractor.side_effect = [
            {'yes': 1},
            {'blue': 1, 'green': 1},
            {'no': 1},
            {}
        ]
        extract_panoptes_csv.extract_csv(
            self.classification_data_dump_two_tasks,
            self.config_yaml_question,
            cpu_count=1,
            hide_progressbar=True
        )
        mock_progress_bar.assert_not_called()
