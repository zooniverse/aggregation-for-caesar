import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import os
import pandas
from pandas.util.testing import assert_frame_equal
import panoptes_aggregation.scripts.extract_panoptes_csv as extract_panoptes_csv

classification_data_dump = '''classification_id,user_name,user_id,workflow_id,workflow_version,created_at,annotations,subject_ids
1,1,1,4249,14.18,2017-05-31 12:33:46 UTC,"[{""task"":""T0""},{""task"":""T1""}]",1
2,2,2,4249,14.18,2017-05-31 12:33:51 UTC,"[{""task"":""T0""},{""task"":""T1""}]",1
'''

extractor_config_yaml = '''{
    'workflow_id': 4249,
    'workflow_version': '14.18',
    'extractor_config': {'question_extractor': [{'task': 'T0'}, {'task': 'T1'}]}
}'''

extracted_csv = '''classification_id,user_name,user_id,workflow_id,task,created_at,subject_id,extractor,data.blue,data.green,data.no,data.yes
1,1,1,4249,T0,2017-05-31 12:33:46 UTC,1,question_extractor,,,,1.0
1,1,1,4249,T1,2017-05-31 12:33:46 UTC,1,question_extractor,1.0,1.0,,
2,2,2,4249,T0,2017-05-31 12:33:51 UTC,1,question_extractor,,,1.0,
2,2,2,4249,T1,2017-05-31 12:33:51 UTC,1,question_extractor,,,,
'''


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
    {}
]
mock_extractors_dict = {
    'question_extractor': mock_question_extractor
}


class TestExtractCSV(unittest.TestCase):
    def setUp(self):
        self.classification_data_dump = StringIO(classification_data_dump)
        self.config_yaml = StringIO(extractor_config_yaml)
        self.extracts_dataframe = pandas.read_csv(StringIO(extracted_csv))

    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.progressbar.ProgressBar')
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.pandas.DataFrame.to_csv')
    @patch.dict('panoptes_aggregation.scripts.extract_panoptes_csv.extractors.extractors', mock_extractors_dict)
    @patch('panoptes_aggregation.scripts.extract_panoptes_csv.flatten_data', CaptureValues(extract_panoptes_csv.flatten_data))
    def test_extract_csv(self, mock_to_csv, mock_pbar):
        '''Test one extractor makes one csv file'''
        output_file_names = extract_panoptes_csv.extract_csv(
            self.classification_data_dump,
            self.config_yaml
        )
        output_path = os.path.join(os.getcwd(), 'question_extractor_extractions.csv')
        self.assertEqual(output_file_names, [output_path])
        result_dataframe = extract_panoptes_csv.flatten_data.return_values[0]
        assert_frame_equal(result_dataframe, self.extracts_dataframe)
        mock_to_csv.assert_called_once_with(output_path, index=False, encoding='utf-8')
