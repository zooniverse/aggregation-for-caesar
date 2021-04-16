import unittest
from unittest.mock import patch, call
from io import StringIO
import panoptes_aggregation.scripts.config_workflow_panoptes


class TestConfigDropdownWorkflowCL(unittest.TestCase):
    def setUp(self):
        self.workflow_data_dump = StringIO('''workflow_id,version,first_task,tasks,strings,minor_version
        18259,3,T0,"{""T0"":{""help"":""T0.help"",""type"":""dropdown"",""selects"":[{""id"":""2f9a5716761878"",""title"":""Main Dropdown"",""options"":{""*"":[{""label"":""T0.selects.0.options.*.0.label"",""value"":""10c4674f90d0d8""},{""label"":""T0.selects.0.options.*.1.label"",""value"":""dfcb43c0a2d0b8""},{""label"":""T0.selects.0.options.*.2.label"",""value"":""6867636603c12""},{""label"":""T0.selects.0.options.*.3.label"",""value"":""68817dd91be9a8""}]},""required"":true,""allowCreate"":false}],""instruction"":""T0.instruction""}}","{""T0.help"":"""",""T0.instruction"":""Select or type an option"",""T0.selects.0.options.*.0.label"":""1"",""T0.selects.0.options.*.1.label"":""2"",""T0.selects.0.options.*.2.label"":""3"",""T0.selects.0.options.*.3.label"":""4""}",3''')

    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_extractor_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.workflow_reducer_config')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.open')
    @patch('panoptes_aggregation.scripts.config_workflow_panoptes.yaml.dump')
    def test_config_workflow_cl(self, mock_yaml_dump, mock_open, mock_reducer_config, mock_extractor_config):
        '''Test command line config for a dropdown workflow creates the correct number of yaml files with the correct names'''
        mock_extractor_config.return_value = {'dropdown_extractor': [{'task': 'T0'}]}
        mock_reducer_config.return_value = [{'dropdown_reducer': {}}]
        panoptes_aggregation.scripts.config_workflow_panoptes.config_workflow(
            self.workflow_data_dump,
            18259
        )
        expected_extractor_config = {
            'workflow_id': 18259,
            'workflow_version': '3.3',
            'extractor_config': mock_extractor_config.return_value
        }
        expected_reducer_config = {
            'reducer_config': mock_reducer_config.return_value[0]
        }
        expected_strings = {
            'T0.instruction': 'Select or type an option',
            'T0.selects.0.options.*.0.label': {'10c4674f90d0d8': '1'},
            'T0.selects.0.options.*.1.label': {'dfcb43c0a2d0b8': '2'},
            'T0.selects.0.options.*.2.label': {'6867636603c12': '3'},
            'T0.selects.0.options.*.3.label': {'68817dd91be9a8': '4'}
        }
        dump_calls = [
            call(
                expected_extractor_config,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                expected_reducer_config,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            ),
            call(
                expected_strings,
                stream=mock_open.return_value.__enter__(),
                default_flow_style=False,
                indent=4
            )
        ]
        mock_yaml_dump.assert_has_calls(dump_calls, any_order=False)
        open_calls = [
            call('Extractor_config_workflow_18259_V3.3.yaml', 'w', encoding='utf-8'),
            call('Reducer_config_workflow_18259_V3.3_dropdown_extractor.yaml', 'w', encoding='utf-8'),
            call('Task_labels_workflow_18259_V3.3.yaml', 'w', encoding='utf-8')
        ]
        mock_open.assert_has_calls(open_calls, any_order=True)
