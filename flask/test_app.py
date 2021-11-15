# test_app.py
import unittest
import os
import json

from application.app import create_app
from application.app import db

class TaskTestCase(unittest.TestCase):
    """This class represents the task test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.tasklist = json.dumps({"title": "Task 1","description":"hello testing"})
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_task_creation(self):
        """Test API can create a tasklist (POST request)"""
        res = self.client().post('/task/api/v1.0/tasks', data=self.tasklist, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.content_type, "application/json")

    def test_get_all_task(self):
        """Test API can get a tasklist (GET request)."""
        res = self.client().post('/task/api/v1.0/tasks', data=self.tasklist, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.content_type, "application/json")
        res = self.client().get('/task/api/v1.0/tasks')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, "application/json")

    def test_get_tasklist_by_id(self):
        """Test API can get a single tasklist by using it's id."""
        res = self.client().post('/task/api/v1.0/tasks', data=self.tasklist, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.content_type, "application/json")
        result_in_json = json.loads(res.data)
        task_id = result_in_json['tasks']['id']
        result = self.client().get('/task/api/v1.0/tasks/{}'.format(task_id))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(res.content_type, "application/json")

    def test_tasklist_edit(self):
        """Test API can edit an existing tasklist. (PUT request)"""
        res = self.client().post('/task/api/v1.0/tasks', data=self.tasklist, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.content_type, "application/json")
        res = self.client().put('/task/api/v1.0/tasks/1', data=json.dumps({"title": "Hello testing again!","description":"hello testing","done":True}), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, "application/json")
        res = self.client().get('/task/api/v1.0/tasks/1')
        result_in_json = json.loads(res.data)
        self.assertIn('Hello testing again!', str(result_in_json['tasks']['title']))

    def test_tasklist_deletion(self):
        """Test API can delete an existing tasklist. (DELETE request)."""
        res = self.client().post('/task/api/v1.0/tasks',data=self.tasklist, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.content_type, "application/json")
        res = self.client().delete('/task/api/v1.0/tasks/1')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, "application/json")

        # Test to see if it exists, should return a 404
        result = self.client().get('/task/api/v1.0/tasks/1')
        self.assertEqual(result.status_code, 404)
        self.assertEqual(res.content_type, "application/json")

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
