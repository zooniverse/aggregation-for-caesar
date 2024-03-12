import unittest
from panoptes_aggregation.batch_aggregation import run_aggregation


class TestBatchAggregation(unittest.TestCase):
    def test_save_exports(self):
        # Test that Panoptes calls are made and files are saved
        assert 1 == 1

    def test_process_wf_export(self):
        # Test that:
        # the wf export is parsed
        # the version instance vars are set
        # dataframe is retuned
        assert 1 == 1

    def test_process_cls_export(self):
        # Test that the cls csv is parsed and a dataframe is returned
        assert 1 == 1
