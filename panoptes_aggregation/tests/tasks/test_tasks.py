# try:
#     import panoptes_aggregation.routes as routes
#     OFFLINE = False
# except ImportError:
#     OFFLINE = True
import unittest
# import json


from panoptes_aggregation.tasks import add
import unittest
class TestAddTask(unittest.TestCase):
    def test_add_task(self):
        assert add.run(x=3, y=5) == 8

# @unittest.skipIf(OFFLINE, 'Installed in offline mode')
# class TasksTest(unittest.TestCase):
#     def test_task_status(celery_worker):
#         application = routes.make_application()
#         client = application.test_client()
#         resp = client.post(
#             "/tasks",
#             data=json.dumps({"type": 1}),
#             content_type='application/json'
#         )
#         content = json.loads(resp.data.decode())
#         task_id = content["task_id"]
#         assert resp.status_code == 202
#         assert task_id

#         resp = client.get(f"tasks/{task_id}")
#         content = json.loads(resp.data.decode())
#         assert content == {"task_id": task_id, "task_status": "PENDING", "task_result": None}
#         assert resp.status_code == 200

        # while content["task_status"] == "PENDING":
        #     resp = client.get(f"tasks/{task_id}")
        #     content = json.loads(resp.data.decode())
        # assert content == {"task_id": task_id, "task_status": "SUCCESS", "task_result": True}
