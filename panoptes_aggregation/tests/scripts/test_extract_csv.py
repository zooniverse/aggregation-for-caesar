import unittest
from unittest.mock import patch
from io import StringIO
import os
import pandas
from pandas.util.testing import assert_frame_equal
import panoptes_aggregation.scripts.extract_panoptes_csv

classification_data_dump = '''classification_id,user_name,user_id,workflow_id,workflow_version,created_at,annotations,subject_ids
57562782,1,1,4249,14.18,2017-05-31 12:33:46 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""Yes""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Blue"",""Green""]}]",1
57562791,2,2,4249,14.18,2017-05-31 12:33:51 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""No""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[]}]",1
57562799,3,3,4249,14.18,2017-05-31 12:33:54 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""All of the above""}]",1
57562811,4,4,4249,14.18,2017-05-31 12:34:00 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""Yes""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Blue"",""Red"",""Green""]}]",1
57562821,5,5,4249,14.18,2017-05-31 12:34:04 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""No""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Green"",""Red""]}]",1
57562828,6,6,4249,14.18,2017-05-31 12:34:08 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""All of the above""}]",1
57562833,7,7,4249,14.18,2017-05-31 12:34:10 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""All of the above""}]",1
57562848,8,8,4249,14.18,2017-05-31 12:34:16 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""Yes""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Green"",""Blue""]}]",1
57562856,9,9,4249,14.18,2017-05-31 12:34:20 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""No""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[]}]",1
57562871,10,10,4249,14.18,2017-05-31 12:34:25 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""No""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Green"",""Red""]}]",1
57562882,1,1,4249,14.18,2017-05-31 12:34:29 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""No""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Blue""]}]",2
57562969,2,2,4249,14.18,2017-05-31 12:35:17 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""All of the above""}]",2
57562981,3,3,4249,14.18,2017-05-31 12:35:22 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""Yes""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Blue"",""Red""]}]",2
57562987,4,4,4249,14.18,2017-05-31 12:35:27 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""No""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Blue""]}]",2
57562999,5,5,4249,14.18,2017-05-31 12:35:33 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""Yes""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Green"",""Red""]}]",2
57563010,6,6,4249,14.18,2017-05-31 12:35:38 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""Yes""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Red"",""Blue""]}]",2
57563014,7,7,4249,14.18,2017-05-31 12:35:43 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""No""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Red"",""Green"",""Blue""]}]",2
57563019,8,8,4249,14.18,2017-05-31 12:35:47 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""All of the above""}]",2
57563026,9,9,4249,14.18,2017-05-31 12:35:50 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""Yes""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[]}]",2
57563034,10,10,4249,14.18,2017-05-31 12:35:56 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""No""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Green"",""Blue""]}]",2
57563039,1,1,4249,14.18,2017-05-31 12:35:59 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""All of the above""}]",3
57563046,2,2,4249,14.18,2017-05-31 12:36:05 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""Yes""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Blue"",""Red""]}]",3
57563051,3,3,4249,14.18,2017-05-31 12:36:09 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""No""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Green"",""Blue""]}]",3
57563057,4,4,4249,14.18,2017-05-31 12:36:12 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""All of the above""}]",3
57563061,5,5,4249,14.18,2017-05-31 12:36:15 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""Yes""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[]}]",3
57563065,6,6,4249,14.18,2017-05-31 12:36:21 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""No""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Green""]}]",3
57563069,7,7,4249,14.18,2017-05-31 12:36:25 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""Yes""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Blue"",""Green""]}]",3
57563075,8,8,4249,14.18,2017-05-31 12:36:30 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""No""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Green"",""Red""]}]",3
57563084,9,9,4249,14.18,2017-05-31 12:36:34 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""No""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Green"",""Red""]}]",3
57563088,10,10,4249,14.18,2017-05-31 12:36:38 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""All of the above""}]",3
57563099,1,1,4249,14.18,2017-05-31 12:36:45 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""No""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Green"",""Red""]}]",3
57563104,2,2,4249,14.18,2017-05-31 12:36:49 UTC,"[{""task"":""T0"",""task_label"":""A single question"",""value"":""No""},{""task"":""T1"",""task_label"":""A multi question"",""value"":[""Green"",""Blue""]}]",3'''

extractor_config_yaml = '''{
    'workflow_id': 4249,
    'workflow_version': '14.18',
    'extractor_config': {'question_extractor': [{'task': 'T0'}, {'task': 'T1'}]}
}'''

extracted_csv = '''classification_id,user_name,user_id,workflow_id,task,created_at,subject_id,extractor,data.all-of-the-above,data.blue,data.green,data.no,data.red,data.yes
57562782,1,1,4249,T0,2017-05-31 12:33:46 UTC,1,question_extractor,,,,,,1.0
57562782,1,1,4249,T1,2017-05-31 12:33:46 UTC,1,question_extractor,,1.0,1.0,,,
57562791,2,2,4249,T0,2017-05-31 12:33:51 UTC,1,question_extractor,,,,1.0,,
57562791,2,2,4249,T1,2017-05-31 12:33:51 UTC,1,question_extractor,,,,,,
57562799,3,3,4249,T0,2017-05-31 12:33:54 UTC,1,question_extractor,1.0,,,,,
57562799,3,3,4249,T1,2017-05-31 12:33:54 UTC,1,question_extractor,,,,,,
57562811,4,4,4249,T0,2017-05-31 12:34:00 UTC,1,question_extractor,,,,,,1.0
57562811,4,4,4249,T1,2017-05-31 12:34:00 UTC,1,question_extractor,,1.0,1.0,,1.0,
57562821,5,5,4249,T0,2017-05-31 12:34:04 UTC,1,question_extractor,,,,1.0,,
57562821,5,5,4249,T1,2017-05-31 12:34:04 UTC,1,question_extractor,,,1.0,,1.0,
57562828,6,6,4249,T0,2017-05-31 12:34:08 UTC,1,question_extractor,1.0,,,,,
57562828,6,6,4249,T1,2017-05-31 12:34:08 UTC,1,question_extractor,,,,,,
57562833,7,7,4249,T0,2017-05-31 12:34:10 UTC,1,question_extractor,1.0,,,,,
57562833,7,7,4249,T1,2017-05-31 12:34:10 UTC,1,question_extractor,,,,,,
57562848,8,8,4249,T0,2017-05-31 12:34:16 UTC,1,question_extractor,,,,,,1.0
57562848,8,8,4249,T1,2017-05-31 12:34:16 UTC,1,question_extractor,,1.0,1.0,,,
57562856,9,9,4249,T0,2017-05-31 12:34:20 UTC,1,question_extractor,,,,1.0,,
57562856,9,9,4249,T1,2017-05-31 12:34:20 UTC,1,question_extractor,,,,,,
57562871,10,10,4249,T0,2017-05-31 12:34:25 UTC,1,question_extractor,,,,1.0,,
57562871,10,10,4249,T1,2017-05-31 12:34:25 UTC,1,question_extractor,,,1.0,,1.0,
57562882,1,1,4249,T0,2017-05-31 12:34:29 UTC,2,question_extractor,,,,1.0,,
57562882,1,1,4249,T1,2017-05-31 12:34:29 UTC,2,question_extractor,,1.0,,,,
57562969,2,2,4249,T0,2017-05-31 12:35:17 UTC,2,question_extractor,1.0,,,,,
57562969,2,2,4249,T1,2017-05-31 12:35:17 UTC,2,question_extractor,,,,,,
57562981,3,3,4249,T0,2017-05-31 12:35:22 UTC,2,question_extractor,,,,,,1.0
57562981,3,3,4249,T1,2017-05-31 12:35:22 UTC,2,question_extractor,,1.0,,,1.0,
57562987,4,4,4249,T0,2017-05-31 12:35:27 UTC,2,question_extractor,,,,1.0,,
57562987,4,4,4249,T1,2017-05-31 12:35:27 UTC,2,question_extractor,,1.0,,,,
57562999,5,5,4249,T0,2017-05-31 12:35:33 UTC,2,question_extractor,,,,,,1.0
57562999,5,5,4249,T1,2017-05-31 12:35:33 UTC,2,question_extractor,,,1.0,,1.0,
57563010,6,6,4249,T0,2017-05-31 12:35:38 UTC,2,question_extractor,,,,,,1.0
57563010,6,6,4249,T1,2017-05-31 12:35:38 UTC,2,question_extractor,,1.0,,,1.0,
57563014,7,7,4249,T0,2017-05-31 12:35:43 UTC,2,question_extractor,,,,1.0,,
57563014,7,7,4249,T1,2017-05-31 12:35:43 UTC,2,question_extractor,,1.0,1.0,,1.0,
57563019,8,8,4249,T0,2017-05-31 12:35:47 UTC,2,question_extractor,1.0,,,,,
57563019,8,8,4249,T1,2017-05-31 12:35:47 UTC,2,question_extractor,,,,,,
57563026,9,9,4249,T0,2017-05-31 12:35:50 UTC,2,question_extractor,,,,,,1.0
57563026,9,9,4249,T1,2017-05-31 12:35:50 UTC,2,question_extractor,,,,,,
57563034,10,10,4249,T0,2017-05-31 12:35:56 UTC,2,question_extractor,,,,1.0,,
57563034,10,10,4249,T1,2017-05-31 12:35:56 UTC,2,question_extractor,,1.0,1.0,,,
57563039,1,1,4249,T0,2017-05-31 12:35:59 UTC,3,question_extractor,1.0,,,,,
57563039,1,1,4249,T1,2017-05-31 12:35:59 UTC,3,question_extractor,,,,,,
57563046,2,2,4249,T0,2017-05-31 12:36:05 UTC,3,question_extractor,,,,,,1.0
57563046,2,2,4249,T1,2017-05-31 12:36:05 UTC,3,question_extractor,,1.0,,,1.0,
57563051,3,3,4249,T0,2017-05-31 12:36:09 UTC,3,question_extractor,,,,1.0,,
57563051,3,3,4249,T1,2017-05-31 12:36:09 UTC,3,question_extractor,,1.0,1.0,,,
57563057,4,4,4249,T0,2017-05-31 12:36:12 UTC,3,question_extractor,1.0,,,,,
57563057,4,4,4249,T1,2017-05-31 12:36:12 UTC,3,question_extractor,,,,,,
57563061,5,5,4249,T0,2017-05-31 12:36:15 UTC,3,question_extractor,,,,,,1.0
57563061,5,5,4249,T1,2017-05-31 12:36:15 UTC,3,question_extractor,,,,,,
57563065,6,6,4249,T0,2017-05-31 12:36:21 UTC,3,question_extractor,,,,1.0,,
57563065,6,6,4249,T1,2017-05-31 12:36:21 UTC,3,question_extractor,,,1.0,,,
57563069,7,7,4249,T0,2017-05-31 12:36:25 UTC,3,question_extractor,,,,,,1.0
57563069,7,7,4249,T1,2017-05-31 12:36:25 UTC,3,question_extractor,,1.0,1.0,,,
57563075,8,8,4249,T0,2017-05-31 12:36:30 UTC,3,question_extractor,,,,1.0,,
57563075,8,8,4249,T1,2017-05-31 12:36:30 UTC,3,question_extractor,,,1.0,,1.0,
57563084,9,9,4249,T0,2017-05-31 12:36:34 UTC,3,question_extractor,,,,1.0,,
57563084,9,9,4249,T1,2017-05-31 12:36:34 UTC,3,question_extractor,,,1.0,,1.0,
57563088,10,10,4249,T0,2017-05-31 12:36:38 UTC,3,question_extractor,1.0,,,,,
57563088,10,10,4249,T1,2017-05-31 12:36:38 UTC,3,question_extractor,,,,,,
57563099,1,1,4249,T0,2017-05-31 12:36:45 UTC,3,question_extractor,,,,1.0,,
57563099,1,1,4249,T1,2017-05-31 12:36:45 UTC,3,question_extractor,,,1.0,,1.0,
57563104,2,2,4249,T0,2017-05-31 12:36:49 UTC,3,question_extractor,,,,1.0,,
57563104,2,2,4249,T1,2017-05-31 12:36:49 UTC,3,question_extractor,,1.0,1.0,,,'''


class CaptureValues(object):
    def __init__(self, func):
        self.func = func
        self.return_values = []

    def __call__(self, *args, **kwargs):
        answer = self.func(*args, **kwargs)
        self.return_values.append(answer)
        return answer


class TestExtractCSV(unittest.TestCase):
    def setUp(self):
        self.classification_data_dump = StringIO(classification_data_dump)
        self.config_yaml = StringIO(extractor_config_yaml)
        self.extracts_dataframe = pandas.read_csv(StringIO(extracted_csv))

    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.flatten_data', CaptureValues(panoptes_aggregation.scripts.extract_panoptes_csv.flatten_data))
    def test_extract_csv(self, mock_to_csv, mock_pbar):
        '''Test one extractor makes one csv file'''
        output_file_names = panoptes_aggregation.scripts.extract_panoptes_csv.extract_csv(
            self.classification_data_dump,
            self.config_yaml
        )
        output_path = os.path.join(os.getcwd(), 'question_extractor_extractions.csv')
        self.assertEqual(output_file_names, [output_path])
        result_dataframe = panoptes_aggregation.scripts.extract_panoptes_csv.flatten_data.return_values[0]
        trim_columns = [c for c in result_dataframe.columns if c != 'data.aggregation_version']
        assert_frame_equal(result_dataframe[trim_columns], self.extracts_dataframe)
        mock_to_csv.assert_called_once_with(output_path, index=False, encoding='utf-8')
