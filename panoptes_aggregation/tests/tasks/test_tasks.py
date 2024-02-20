import unittest
from panoptes_aggregation.tasks import add

class TestAddTask(unittest.TestCase):
    def test_add_task(self):
        assert add.run(x=3, y=5) == 8
