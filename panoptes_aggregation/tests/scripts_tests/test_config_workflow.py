import unittest
from unittest.mock import patch, call
from io import StringIO
import os
import panoptes_aggregation.scripts.config_workflow_panoptes


class TestConfigWorkflowCL(unittest.TestCase):
    def setUp(self):
        self.workflow_data_dump = StringIO('''workflow_id,version,tasks,strings,minor_version
        4249,13,"{""T0"":{""help"":""T0.help"",""type"":""single"",""answers"":[{""label"":""T0.answers.0.label""},{""label"":""T0.answers.1.label""},{""label"":""T0.answers.2.label""}],""question"":""T0.question"",""required"":true}}","{""T0.help"":"""",""T0.question"":""A single question"",""T0.answers.0.label"":""Yes"",""T0.answers.1.label"":""No""}",1
        4249,14,"{""T0"":{""help"":""T0.help"",""type"":""single"",""answers"":[{""label"":""T0.answers.0.label""},{""label"":""T0.answers.1.label""},{""label"":""T0.answers.2.label""}],""question"":""T0.question"",""required"":true}}","{""T0.help"":"""",""T0.question"":""A single question"",""T0.answers.0.label"":""Yes"",""T0.answers.1.label"":""No"",""T0.answers.2.label"":""All of the above""}",1
        4249,14,"{""T0"":{""help"":""T0.help"",""type"":""single"",""answers"":[{""next"":""T1"",""label"":""T0.answers.0.label""},{""next"":""T1"",""label"":""T0.answers.1.label""},{""label"":""T0.answers.2.label""}],""question"":""T0.question"",""required"":true},""T1"":{""help"":""T1.help"",""type"":""shortcut"",""answers"":[{""label"":""T1.answers.0.label""},{""label"":""T1.answers.1.label""},{""label"":""T1.answers.2.label""}],""question"":""T1.question""}}","{""T0.help"":"""",""T1.help"":"""",""T0.question"":""A single question"",""T1.question"":""A multi question"",""T0.answers.0.label"":""Yes"",""T0.answers.1.label"":""No"",""T0.answers.2.label"":""All of the above"",""T1.answers.0.label"":""Red"",""T1.answers.1.label"":""Blue"",""T1.answers.2.label"":""Green""}",18''')

        self.mock_extractor_config_14_18 = {'question_extractor': [{'task': 'T0'}, {'task': 'T1'}]}
        self.mock_extractor_config_14_1 = {'question_extractor': [{'task': 'T0'}]}

        self.mock_reducer_config_14_18 = [{'question_reducer': {}}]
        self.mock_reducer_config_14_1 = [{'question_reducer': {}}]

        self.expected_extractor_config_14_18 = {
            'workflow_id': 4249,
            'workflow_version': '14.18',
            'extractor_config': self.mock_extractor_config_14_18
        }
        self.expected_extractor_config_14_1 = {
            'workflow_id': 4249,
            'workflow_version': '14.1',
            'extractor_config': self.mock_extractor_config_14_1
        }

        self.expected_reducer_config_14_18 = {'reducer_config': self.mock_reducer_config_14_18[0]}
        self.expected_reducer_config_14_1 = {'reducer_config': self.mock_reducer_config_14_1[0]}

        self.expected_strings_14_18 = {
            'T0.question': 'A single question',
            'T0.answers.0.label': 'Yes',
            'T0.answers.1.label': 'No',
            'T0.answers.2.label': 'All of the above',
            'T1.question': 'A multi question',
            'T1.answers.0.label': 'Red',
            'T1.answers.1.label': 'Blue',
            'T1.answers.2.label': 'Green'
        }
        self.expected_strings_14_1 = {
            'T0.question': 'A single question',
            'T0.answers.0.label': 'Yes',
            'T0.answers.1.label': 'No',
            'T0.answers.2.label': 'All of the above'
        }

        self.open_calls_14_18 = [
            call('Extractor_config_workflow_4249_V14.18.yaml', 'w', encoding='utf-8'),
            call('Reducer_config_workflow_4249_V14.18_question_extractor.yaml', 'w', encoding='utf-8'),
            call('Task_labels_workflow_4249_V14.18.yaml', 'w', encoding='utf-8')
        ]
        self.open_calls_14_1 = [
            call('Extractor_config_workflow_4249_V14.1.yaml', 'w', encoding='utf-8'),
            call('Reducer_config_workflow_4249_V14.1_question_extractor.yaml', 'w', encoding='utf-8'),
            call('Task_labels_workflow_4249_V14.1.yaml', 'w', encoding='utf-8')
        ]

    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_extractor_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_reducer_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.open')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.yaml.dump')
    def test_config_workflow_cl(self, mock_yaml_dump, mock_open, mock_reducer_config, mock_extractor_config):
        '''Test command line config workflow creates the correct number of yaml files with the correct names'''
        mock_extractor_config.return_value = self.mock_extractor_config_14_18
        mock_reducer_config.return_value = self.mock_reducer_config_14_18

        panoptes_aggregation.scripts.config_workflow_panoptes.config_workflow(
            self.workflow_data_dump,
            4249
        )
        dump_calls = [
            call(
                self.expected_extractor_config_14_18,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                self.expected_reducer_config_14_18,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                self.expected_strings_14_18,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            )
        ]
        mock_yaml_dump.assert_has_calls(dump_calls, any_order=False)
        mock_open.assert_has_calls(self.open_calls_14_18, any_order=True)

    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_extractor_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_reducer_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.open')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.yaml.dump')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.warnings.warn')
    def test_config_workflow_cl_with_major_version(self, mock_warn, mock_yaml_dump, mock_open, mock_reducer_config, mock_extractor_config):
        '''Test command line config workflow creates the correct number of yaml files with the correct names with major version specified'''
        mock_extractor_config.return_value = self.mock_extractor_config_14_18
        mock_reducer_config.return_value = self.mock_reducer_config_14_18
        panoptes_aggregation.scripts.config_workflow_panoptes.config_workflow(
            self.workflow_data_dump,
            4249,
            version='14',
            verbose=True
        )
        expected_extractor_config_14 = {
            'workflow_id': 4249,
            'workflow_version': '14',
            'extractor_config': self.mock_extractor_config_14_18
        }
        dump_calls = [
            call(
                expected_extractor_config_14,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                self.expected_reducer_config_14_18,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                self.expected_strings_14_18,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            )
        ]
        mock_yaml_dump.assert_has_calls(dump_calls, any_order=False)
        mock_open.assert_has_calls(self.open_calls_14_18, any_order=True)
        warning_calls = [
            call('A workflow range was specified, configuration is based on 14.18'),
        ]
        mock_warn.assert_has_calls(warning_calls, any_order=False)

    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_extractor_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_reducer_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.open')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.yaml.dump')
    def test_config_workflow_cl_with_version(self, mock_yaml_dump, mock_open, mock_reducer_config, mock_extractor_config):
        '''Test command line config workflow creates the correct number of yaml files with the correct names when a version is given'''
        mock_extractor_config.return_value = self.mock_extractor_config_14_1
        mock_reducer_config.return_value = self.mock_reducer_config_14_1
        panoptes_aggregation.scripts.config_workflow_panoptes.config_workflow(
            self.workflow_data_dump,
            4249,
            version='14.1'
        )
        dump_calls = [
            call(
                self.expected_extractor_config_14_1,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                self.expected_reducer_config_14_1,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                self.expected_strings_14_1,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            )
        ]
        mock_yaml_dump.assert_has_calls(dump_calls, any_order=False)
        mock_open.assert_has_calls(self.open_calls_14_1, any_order=True)

    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_extractor_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_reducer_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.open')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.yaml.dump')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.warnings.warn')
    def test_config_workflow_cl_with_min_version(self, mock_warn, mock_yaml_dump, mock_open, mock_reducer_config, mock_extractor_config):
        '''Test command line config workflow creates the correct number of yaml files with the correct names when a min_version is given'''
        mock_extractor_config.return_value = self.mock_extractor_config_14_18
        mock_reducer_config.return_value = self.mock_reducer_config_14_18
        panoptes_aggregation.scripts.config_workflow_panoptes.config_workflow(
            self.workflow_data_dump,
            4249,
            min_version='14.1',
            verbose=True
        )
        expected_extractor_config_14_min = {
            'workflow_id': 4249,
            'workflow_version': {
                'min': '14.1'
            },
            'extractor_config': self.mock_extractor_config_14_18
        }
        dump_calls = [
            call(
                expected_extractor_config_14_min,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                self.expected_reducer_config_14_18,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                self.expected_strings_14_18,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            )
        ]
        mock_yaml_dump.assert_has_calls(dump_calls, any_order=False)
        mock_open.assert_has_calls(self.open_calls_14_18, any_order=True)
        warning_calls = [
            call('A workflow range was specified, configuration is based on 14.18'),
        ]
        mock_warn.assert_has_calls(warning_calls, any_order=False)

    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_extractor_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_reducer_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.open')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.yaml.dump')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.warnings.warn')
    def test_config_workflow_cl_with_max_version(self, mock_warn, mock_yaml_dump, mock_open, mock_reducer_config, mock_extractor_config):
        '''Test command line config workflow creates the correct number of yaml files with the correct names when a max_version is given'''
        mock_extractor_config.return_value = self.mock_extractor_config_14_1
        mock_reducer_config.return_value = self.mock_reducer_config_14_1
        panoptes_aggregation.scripts.config_workflow_panoptes.config_workflow(
            self.workflow_data_dump,
            4249,
            max_version='14.1',
            verbose=True
        )
        expected_extractor_config_14_min = {
            'workflow_id': 4249,
            'workflow_version': {
                'max': '14.1'
            },
            'extractor_config': self.mock_extractor_config_14_1
        }
        dump_calls = [
            call(
                expected_extractor_config_14_min,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                self.expected_reducer_config_14_1,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                self.expected_strings_14_1,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            )
        ]
        mock_yaml_dump.assert_has_calls(dump_calls, any_order=False)
        mock_open.assert_has_calls(self.open_calls_14_1, any_order=True)
        warning_calls = [
            call('A workflow range was specified, configuration is based on 14.1'),
        ]
        mock_warn.assert_has_calls(warning_calls, any_order=False)

    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.yaml.dump')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_extractor_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_reducer_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.open')
    def test_config_workflow_cl_with_dir(self, mock_open, mock_reducer_config, mock_extractor_config, *_):
        '''Test command line config workflow saves to specified directory'''
        mock_extractor_config.return_value = self.mock_extractor_config_14_18
        mock_reducer_config.return_value = self.mock_reducer_config_14_18
        panoptes_aggregation.scripts.config_workflow_panoptes.config_workflow(
            self.workflow_data_dump,
            4249,
            output_dir='home'
        )
        open_calls = [
            call(os.path.join('home', 'Extractor_config_workflow_4249_V14.18.yaml'), 'w', encoding='utf-8'),
            call(os.path.join('home', 'Reducer_config_workflow_4249_V14.18_question_extractor.yaml'), 'w', encoding='utf-8'),
            call(os.path.join('home', 'Task_labels_workflow_4249_V14.18.yaml'), 'w', encoding='utf-8')
        ]
        mock_open.assert_has_calls(open_calls, any_order=True)

    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.yaml.dump')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.open')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_extractor_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_reducer_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.warnings.warn')
    def test_config_workflow_cl_with_verbose(self, mock_warn, mock_reducer_config, mock_extractor_config, *_):
        '''Test command line config workflow verbose mode creates warnings'''
        mock_extractor_config.return_value = {'question_extractor': [{'task': 'T0'}, {'task': 'T1'}]}
        mock_reducer_config.return_value = [{'question_reducer': {}}]
        panoptes_aggregation.scripts.config_workflow_panoptes.config_workflow(
            self.workflow_data_dump,
            4249,
            verbose=True
        )
        warning_calls = [
            call('No workflow version was specified, defaulting to version 14.18'),
        ]
        mock_warn.assert_has_calls(warning_calls, any_order=False)

    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_extractor_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_reducer_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.open')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.yaml.dump')
    def test_config_workflow_cl_multiple_reducers(self, mock_yaml_dump, mock_open, mock_reducer_config, mock_extractor_config):
        '''Test command line config workflow with two reducers'''
        mock_extractor_config.return_value = {
            'question_extractor': [{'task': 'T0'}],
            'shortcut_extractor': [{'task': 'T1'}]
        }
        mock_reducer_config.return_value = [
            {'question_reducer': {}},
            {'shortcut_reducer': {}}
        ]
        panoptes_aggregation.scripts.config_workflow_panoptes.config_workflow(
            self.workflow_data_dump,
            4249
        )
        expected_extractor_config = {
            'workflow_id': 4249,
            'workflow_version': '14.18',
            'extractor_config': mock_extractor_config.return_value
        }
        expected_reducer_config_0 = {
            'reducer_config': mock_reducer_config.return_value[0]
        }
        expected_reducer_config_1 = {
            'reducer_config': mock_reducer_config.return_value[1]
        }
        dump_calls = [
            call(
                expected_extractor_config,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                expected_reducer_config_0,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                expected_reducer_config_1,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                self.expected_strings_14_18,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            )
        ]
        mock_yaml_dump.assert_has_calls(dump_calls, any_order=False)
        open_calls = [
            call('Extractor_config_workflow_4249_V14.18.yaml', 'w', encoding='utf-8'),
            call('Reducer_config_workflow_4249_V14.18_question_extractor.yaml', 'w', encoding='utf-8'),
            call('Reducer_config_workflow_4249_V14.18_shortcut_extractor.yaml', 'w', encoding='utf-8'),
            call('Task_labels_workflow_4249_V14.18.yaml', 'w', encoding='utf-8')
        ]
        mock_open.assert_has_calls(open_calls, any_order=True)
