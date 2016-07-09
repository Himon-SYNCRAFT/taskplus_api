from tests.base import Base
from tests.utils import is_json
from flask import json
from models import Task, Task
from database import db_session
from exceptions import ValidationError
from utils import query_from_dict
from sqlalchemy.exc import IntegrityError


class TestTask(Base):

    def test_can_get_task(self):
        task = Task.query.first()
        response = self.client.get('/task/' + str(task.id))

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        data = json.loads(response.get_data())

        self.assertEqual(data, task.to_dict())

    def test_404_if_task_not_exist_or_task_id_is_invalid(self):
        response = self.client.get('/task/' + 'sdfs')
        self.assertStatus(response, 404)

        response = self.client.get('/task/' + str(1000000))
        self.assertStatus(response, 404)

    def test_update_from_dict(self):
        task = Task.query.first()
        task_id = task.id

        task_dict = dict(
            name='Usuń'
        )

        task.update_from_dict(task_dict)
        db_session.add(task)
        db_session.commit()

        task = Task.query.filter_by(id=task_id).first()

        self.assertIsNotNone(task)
        self.assertEqual(task_dict['name'], task.name)

    def test_update_from_dict_invalid_type(self):
        task = Task.query.first()
        task_id = task.id

        task_list = [
            'Usuń'
        ]

        with self.assertRaises(TypeError):
            task.update_from_dict(task_list)
            db_session.add(task)
            db_session.commit()

        task2 = Task.query.filter_by(name='Usuń').first()
        new_task = Task.query.filter_by(id=task_id).first()

        self.assertIsNone(task2)
        self.assertEqual(new_task, task)

    def test_create_task_from_dict(self):
        count_before_insert = Task.query.count()

        task_dict = dict(name='tmp', type_id=1, status_id=1, creator_id=1)

        task = Task.create_from_dict(task_dict)
        db_session.add(task)
        db_session.commit()

        count_after_insert = Task.query.count()

        self.assertEqual(count_before_insert + 1, count_after_insert)

        task = Task.query.filter_by(
            name='tmp', type_id=1, status_id=1, creator_id=1).first()

        self.assertIsNotNone(task)
        self.assertEqual(task_dict['name'], task.name)

    def test_create_task_from_dict_invalid_type(self):
        count_before_insert = Task.query.count()

        task_list = [
            'Usuń'
        ]

        with self.assertRaises(TypeError):
            task = Task.create_from_dict(task_list)
            db_session.add(task)
            db_session.commit()

        count_after_insert = Task.query.count()

        self.assertEqual(count_before_insert, count_after_insert)

    def test_create_task_from_dict_invalid_data(self):
        count_before_insert = Task.query.count()

        task_dict = dict()

        with self.assertRaises(ValidationError):
            task = Task.create_from_dict(task_dict)
            db_session.add(task)
            db_session.commit()

        count_after_insert = Task.query.count()

    def test_create_task_from_dict_invalid_indices(self):
        count_before_insert = Task.query.count()

        task_dict = dict(name='tmp', type_id=10, status_id=10, creator_id=10)

        with self.assertRaises(IntegrityError):
            task = Task.create_from_dict(task_dict)
            db_session.add(task)
            db_session.commit()

        db_session.rollback()

        count_after_insert = Task.query.count()

        self.assertEqual(count_before_insert, count_after_insert)

    def test_update_task(self):
        task = Task.query.first()

        task_dict = dict(name='tmp', type_id=1, status_id=1, creator_id=1)

        response = self.client.put(
            '/task/' + str(task.id),
            data=json.dumps(task_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        task = Task.query.filter_by(**task_dict).first()

        self.assertIsNotNone(task)

        data = json.loads(response.get_data())

        self.assertEqual(data, task.to_dict())

    def test_update_not_existing_task(self):
        task = Task.query.first()

        task_dict = dict(name='tmp', type_id=1, status_id=1, creator_id=1)

        response = self.client.put(
            '/task/' + '123124134',
            data=json.dumps(task_dict),
            headers={'Content-Type': 'application/json'}
        )
        self.assertStatus(response, 404)

        response = self.client.put(
            '/task/' + 'abc', data=json.dumps(task_dict))
        self.assertStatus(response, 404)

        task = Task.query.filter_by(**task_dict).first()
        self.assertIsNone(task)

    def test_update_task_invalid_data(self):
        task_dict = dict(name=True)

        task = Task.query.first()

        response = self.client.put(
            '/task/' + str(task.id),
            data=json.dumps(task_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)

        task = Task.query.filter_by(
            name=task_dict['name']).first()
        self.assertIsNone(task)

    def test_update_task_invalid_indices(self):
        task_dict = dict(name='tmp', type_id=10, status_id=10, creator_id=10)

        task = Task.query.first()

        response = self.client.put(
            '/task/' + str(task.id),
            data=json.dumps(task_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 409)

        task = Task.query.filter_by(
            name=task_dict['name']).first()
        self.assertIsNone(task)

    def test_create_task(self):
        count_before_insert = Task.query.count()

        task_dict = dict(name='tmp', type_id=1, status_id=1, creator_id=1)

        response = self.client.post(
            '/task',
            data=json.dumps(task_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = Task.query.count()

        self.assertStatus(response, 201)

        task = Task.query.filter_by(**task_dict).first()

        self.assertEqual(count_before_insert + 1, count_after_insert)
        self.assertIsNotNone(task)
        self.assertEqual(json.loads(response.get_data()), task.to_dict())

    def test_create_task_invalid_data(self):
        count_before_insert = Task.query.count()

        task_dict = dict(
            name=True,
        )

        response = self.client.post(
            '/task',
            data=json.dumps(task_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = Task.query.count()

        self.assertStatus(response, 400)

        task = Task.query.filter_by(**task_dict).first()

        self.assertEqual(count_before_insert, count_after_insert)
        self.assertIsNone(task)

    def test_create_task_invalid_indices(self):
        count_before_insert = Task.query.count()

        task_dict = dict(name='tmp', type_id=10, status_id=10, creator_id=10)

        response = self.client.post(
            '/task',
            data=json.dumps(task_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = Task.query.count()

        self.assertStatus(response, 409)

        task = Task.query.filter_by(**task_dict).first()

        self.assertEqual(count_before_insert, count_after_insert)
        self.assertIsNone(task)

    def test_delete_task(self):
        task = Task(name='tmp', type_id=1, status_id=1, creator_id=1)
        db_session.add(task)
        db_session.commit()

        task_id = task.id

        count_before_delete = Task.query.count()
        response = self.client.delete('/task/' + str(task.id))
        count_after_delete = Task.query.count()

        self.assertStatus(response, 204)
        self.assertIsNone(Task.query.get(task_id))
        self.assertEqual(count_before_delete, count_after_delete + 1)

    def test_delete_not_existing_task(self):
        count_before_delete = Task.query.count()
        response = self.client.delete('/task/' + str(234234234))
        count_after_delete = Task.query.count()

        self.assertStatus(response, 404)
        self.assertEqual(count_before_delete, count_after_delete)

    def test_delete_task_which_cant_be_deleted(self):
        task = Task.query.first()
        task = task.type

        count_before_delete = Task.query.count()
        response = self.client.delete('/task/' + str(task.id))
        count_after_delete = Task.query.count()

        self.assertStatus(response, 409)
        self.assertIsNotNone(Task.query.filter_by(id=task.id).first())
        self.assertEqual(count_before_delete, count_after_delete)

    def test_get_task_list(self):
        response = self.client.get('/tasks')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        count = Task.query.count()

        self.assertEqual(len(data), count)

    def test_get_task_list_by(self):
        response = self.client.get('/tasks?name=Dodaj%20cos%20tam&id=2')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        tasks = Task.query.filter_by(name='Dodaj cos tam', id=2).all()

        tasks_list = [task.to_dict() for task in tasks]

        self.assertEqual(len(data), len(tasks))
        self.assertListEqual(data, tasks_list)

    def test_get_task_list_by_invalid_parameter(self):
        response = self.client.get(
            '/tasks?taskname=admin&first_name=Daniel')

        self.assertStatus(response, 400)

    def test_get_task_list_complex(self):
        data = dict(
            name=dict(value='Dodaj nowy produkt', operator='!=')
        )

        tasks = query_from_dict(Task, data)
        tasks_list = [task.to_dict() for task in tasks]

        response = self.client.post(
            '/tasks',
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )

        data = json.loads(response.get_data())

        self.assertStatus(response, 200)
        self.assertEqual(data, tasks_list)

    def test_get_task_list_complex_invalid_parameter(self):
        data = dict(
            first_name=dict(value='Daniel', operator='!=')
        )

        response = self.client.post(
            '/tasks',
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)

        data = dict(
            name=dict(value1='Daniel', operator='!=')
        )

        response = self.client.post(
            '/tasks',
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)

    def test_get_task_list_complex_invalid_type(self):
        data = dict(
            id=dict(value='Daniel', operator='!=')
        )

        response = self.client.post(
            '/tasks',
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)
