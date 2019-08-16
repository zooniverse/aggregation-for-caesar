import unittest
from unittest.mock import patch, MagicMock, call
from io import StringIO
import os
import pandas
from pandas.util.testing import assert_frame_equal
import panoptes_aggregation.scripts.reduce_panoptes_csv as reduce_panoptes_csv

extracted_csv_question = '''classification_id,user_name,user_id,workflow_id,task,created_at,subject_id,extractor,data.blue,data.green,data.no,data.yes
1,1,1,4249,T0,2017-05-31 12:33:46 UTC,1,question_extractor,,,,1.0
1,1,1,4249,T1,2017-05-31 12:33:46 UTC,1,question_extractor,1.0,1.0,,
2,2,2,4249,T0,2017-05-31 12:33:51 UTC,1,question_extractor,,,1.0,
2,2,2,4249,T1,2017-05-31 12:33:51 UTC,1,question_extractor,,,,
3,1,1,4249,T0,2017-05-31 12:33:46 UTC,2,question_extractor,,,,1.0
3,1,1,4249,T1,2017-05-31 12:33:46 UTC,2,question_extractor,1.0,1.0,,
4,2,2,4249,T0,2017-05-31 12:33:51 UTC,2,question_extractor,,,1.0,
5,2,2,4249,T1,2017-05-31 12:33:51 UTC,2,question_extractor,,,,
'''

reducer_config_yaml_question = '''{'reducer_config': {'question_reducer': {}}}'''

reduced_csv_question = '''subject_id,workflow_id,task,reducer,data.blue,data.green,data.no,data.yes
1,4249,T0,question_reducer,,,1.0,1.0
1,4249,T1,question_reducer,1.0,1.0,,
2,4249,T0,question_reducer,,,1.0,1.0
2,4249,T1,question_reducer,1.0,1.0,,
'''

reduced_csv_question_stream = '''subject_id,workflow_id,task,reducer,data
1,4249,T0,question_reducer,"{'yes': 1, 'no': 1}"
1,4249,T1,question_reducer,"{'blue': 1, 'green': 1}"
2,4249,T0,question_reducer,"{'yes': 1, 'no': 1}"
2,4249,T1,question_reducer,"{'blue': 1, 'green': 1}"
'''

reduced_csv_question_stream_partial = '''subject_id,workflow_id,task,reducer,data
1,4249,T0,question_reducer,"{'yes': 1, 'no': 1}"
1,4249,T1,question_reducer,"{'blue': 1, 'green': 1}"
'''

extracted_csv_survey = '''classification_id,user_name,user_id,workflow_id,task,created_at,subject_id,extractor,data.choice,data.answers_howmany.1,data.answers_howmany.3,data.answers_howmany.4
1,1,1,4249,T0,2017-05-31 12:33:46 UTC,1,survey_extractor,dog,1.0,,
1,1,1,4249,T0,2017-05-31 12:33:46 UTC,1,survey_extractor,cat,,1.0,
2,2,2,4249,T0,2017-05-31 12:33:51 UTC,1,survey_extractor,cat,,,1.0
'''

reducer_config_yaml_survey = '''{'reducer_config': {'survey_reducer': {}}}'''

reduced_csv_survey = '''subject_id,workflow_id,task,reducer,data.choice,data.total_vote_count,data.choice_count,data.answers_howmany.1,data.answers_howmany.3,data.answers_howmany.4
1,4249,T0,survey_reducer,dog,3,1,1.0,,
1,4249,T0,survey_reducer,cat,3,2,,1.0,1.0
'''


class CaptureValues(object):
    def __init__(self, func):
        self.func = func
        self.return_values = []

    def __call__(self, *args, **kwargs):
        answer = self.func(*args, **kwargs)
        self.return_values.append(answer)
        return answer


mock_question_reducer = MagicMock()
mock_question_reducer.side_effect = [
    {'yes': 1, 'no': 1},
    {'blue': 1, 'green': 1},
    {'yes': 1, 'no': 1},
    {'blue': 1, 'green': 1},
    {'yes': 1, 'no': 1},
    {'blue': 1, 'green': 1},
    {'yes': 1, 'no': 1},
    {'blue': 1, 'green': 1},
    {'yes': 1, 'no': 1},
    {'blue': 1, 'green': 1}
]

mock_survey_reducer = MagicMock()
mock_survey_reducer.side_effect = [
    [
        {
            'choice': 'dog',
            'total_vote_count': 3,
            'choice_count': 1,
            'answers_howmany': {
                '1': 1
            }
        },
        {
            'choice': 'cat',
            'total_vote_count': 3,
            'choice_count': 2,
            'answers_howmany': {
                '3': 1,
                '4': 1
            }
        },
    ]
]

mock_reducers_dict = {
    'question_reducer': mock_question_reducer,
    'survey_reducer': mock_survey_reducer
}


class TestReduceCSV(unittest.TestCase):
    def setUp(self):
        self.extracted_csv_question = StringIO(extracted_csv_question)
        self.extracted_dataframe_question = pandas.read_csv(
            StringIO(extracted_csv_question),
            infer_datetime_format=True,
            parse_dates=['created_at'],
            encoding='utf-8'
        )
        self.config_yaml_question = StringIO(reducer_config_yaml_question)
        self.reduced_dataframe_question = pandas.read_csv(StringIO(reduced_csv_question))
        self.reduced_dataframe_question_stream = pandas.read_csv(StringIO(reduced_csv_question_stream))
        self.reduced_dataframe_question_stream_partial = pandas.read_csv(StringIO(reduced_csv_question_stream_partial))
        self.extracted_csv_survey = StringIO(extracted_csv_survey)
        self.config_yaml_survey = StringIO(reducer_config_yaml_survey)
        self.reduced_dataframe_survey = pandas.read_csv(StringIO(reduced_csv_survey))

    def test_first_filter(self):
        '''Test frist filter'''
        extracted_dataframe = pandas.read_csv(self.extracted_csv_question, parse_dates=['created_at'])
        task_T0_csv = extracted_dataframe[(extracted_dataframe.task == 'T0') & (extracted_dataframe.subject_id == 1)]
        expected = task_T0_csv[[True, False]]
        result = reduce_panoptes_csv.first_filter(task_T0_csv)
        assert_frame_equal(result, expected)

    def test_last_filter(self):
        '''Test last filter'''
        extracted_dataframe = pandas.read_csv(self.extracted_csv_question, parse_dates=['created_at'])
        task_T0_csv = extracted_dataframe[(extracted_dataframe.task == 'T0') & (extracted_dataframe.subject_id == 1)]
        expected = task_T0_csv[[False, True]]
        result = reduce_panoptes_csv.last_filter(task_T0_csv)
        assert_frame_equal(result, expected)

    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.reduce_panoptes_csv.reducers.reducers', mock_reducers_dict)
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.flatten_data', CaptureValues(reduce_panoptes_csv.flatten_data))
    def test_reduce_csv_object(self, mock_to_csv, mock_pbar):
        '''Test object reducer makes one csv file'''
        output_file_name = reduce_panoptes_csv.reduce_csv(
            self.extracted_csv_question,
            self.config_yaml_question,
            filter='all'
        )
        mock_question_reducer.assert_any_call([{'yes': 1.0}, {'no': 1.0}], user_id=[1, 2])
        output_path = os.path.join(os.getcwd(), 'question_reducer_reductions.csv')
        self.assertEqual(output_file_name, output_path)
        result_dataframe = reduce_panoptes_csv.flatten_data.return_values[0]
        assert_frame_equal(result_dataframe, self.reduced_dataframe_question, check_like=True)
        mock_to_csv.assert_called_once_with(output_path, index=False, encoding='utf-8')

    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.pandas.DataFrame.to_csv')
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.pandas.read_csv')
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.os.path.isfile')
    @patch.dict('panoptes_aggregation.scripts.reduce_panoptes_csv.reducers.reducers', mock_reducers_dict)
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.flatten_data', CaptureValues(reduce_panoptes_csv.flatten_data))
    def test_reduce_csv_stream(self, mock_is_file, mock_read_csv, mock_to_csv, mock_pbar):
        '''Test streaming object reducer makes one csv file'''
        mock_is_file.return_value = False
        mock_read_csv.side_effect = [
            self.extracted_dataframe_question,
            self.reduced_dataframe_question_stream
        ]
        output_file_name = reduce_panoptes_csv.reduce_csv(
            self.extracted_csv_question,
            self.config_yaml_question,
            filter='all',
            stream=True
        )
        output_path = os.path.join(os.getcwd(), 'question_reducer_reductions.csv')
        mock_is_file.assert_called_once_with(output_path)
        self.assertEqual(output_file_name, output_path)
        to_csv_calls = [
            call(output_path, mode='w', index=False, encoding='utf-8'),
            call(output_path, mode='a', index=False, header=False, encoding='utf-8'),
            call(output_path, index=False, encoding='utf-8')
        ]
        mock_to_csv.assert_has_calls(to_csv_calls, any_order=False)
        mock_read_csv.assert_has_calls([call(output_path, encoding='utf-8')])
        result_dataframe = reduce_panoptes_csv.flatten_data.return_values[0]
        assert_frame_equal(result_dataframe, self.reduced_dataframe_question, check_like=True)

    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.pandas.DataFrame.to_csv')
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.pandas.read_csv')
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.os.path.isfile')
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.open')
    @patch.dict('panoptes_aggregation.scripts.reduce_panoptes_csv.reducers.reducers', mock_reducers_dict)
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.flatten_data', CaptureValues(reduce_panoptes_csv.flatten_data))
    def test_reduce_csv_stream_resume(self, mock_open, mock_is_file, mock_read_csv, mock_to_csv, mock_pbar):
        '''Test resuming works'''
        mock_is_file.return_value = True
        mock_read_csv.side_effect = [
            self.extracted_dataframe_question,
            self.reduced_dataframe_question_stream_partial,
            self.reduced_dataframe_question_stream
        ]
        output_file_name = reduce_panoptes_csv.reduce_csv(
            self.extracted_csv_question,
            self.config_yaml_question,
            filter='all',
            stream=True
        )
        output_path = os.path.join(os.getcwd(), 'question_reducer_reductions.csv')
        mock_is_file.assert_called_once_with(output_path)
        self.assertEqual(output_file_name, output_path)
        to_csv_calls = [
            call(output_path, mode='a', index=False, header=False, encoding='utf-8'),
            call(output_path, index=False, encoding='utf-8')
        ]
        mock_to_csv.assert_has_calls(to_csv_calls, any_order=False)
        mock_read_csv.assert_has_calls([call(output_path, encoding='utf-8')])
        result_dataframe = reduce_panoptes_csv.flatten_data.return_values[0]
        assert_frame_equal(result_dataframe, self.reduced_dataframe_question, check_like=True)

    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.pandas.DataFrame.to_csv')
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.pandas.read_csv')
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.os.path.isfile')
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.open')
    @patch.dict('panoptes_aggregation.scripts.reduce_panoptes_csv.reducers.reducers', mock_reducers_dict)
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.flatten_data', CaptureValues(reduce_panoptes_csv.flatten_data))
    def test_reduce_csv_stream_resume_nothing_new_to_do(self, mock_open, mock_is_file, mock_read_csv, mock_to_csv, mock_pbar):
        '''Test resuming a finished file does not change it'''
        mock_is_file.return_value = True
        mock_read_csv.side_effect = [
            self.extracted_dataframe_question,
            self.reduced_dataframe_question,
            self.reduced_dataframe_question
        ]
        output_file_name = reduce_panoptes_csv.reduce_csv(
            self.extracted_csv_question,
            self.config_yaml_question,
            filter='all',
            stream=True
        )
        output_path = os.path.join(os.getcwd(), 'question_reducer_reductions.csv')
        mock_is_file.assert_called_once_with(output_path)
        self.assertEqual(output_file_name, output_path)
        mock_read_csv.assert_has_calls([call(output_path, encoding='utf-8')])
        mock_to_csv.assert_not_called()

    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.reduce_panoptes_csv.reducers.reducers', mock_reducers_dict)
    @patch('panoptes_aggregation.scripts.reduce_panoptes_csv.order_columns', CaptureValues(reduce_panoptes_csv.order_columns))
    def test_reduce_csv_list(self, mock_to_csv, mock_pbar):
        '''Test list reducer makes one csv file'''
        output_file_name = reduce_panoptes_csv.reduce_csv(
            self.extracted_csv_survey,
            self.config_yaml_survey,
            order=True
        )
        output_path = os.path.join(os.getcwd(), 'survey_reducer_reductions.csv')
        self.assertEqual(output_file_name, output_path)
        result_dataframe = reduce_panoptes_csv.order_columns.return_values[0]
        assert_frame_equal(result_dataframe, self.reduced_dataframe_survey)
        mock_to_csv.assert_called_once_with(output_path, index=False, encoding='utf-8')
