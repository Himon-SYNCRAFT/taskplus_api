from tests.base import Base
from tests.utils import is_json
from flask import json
from models import TaskType, Task
from database import db_session
from exceptions import ValidationError
from utils import query_from_dict


class TestType(Base):

    def test_can_get_task_type(self):
        task_type = TaskType.query.first()
        response = self.client.get('/task/type/' + str(task_type.id))

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        data = json.loads(response.get_data())

        self.assertEqual(data, task_type.to_dict())

    def test_404_if_task_type_not_exist_or_task_type_id_is_invalid(self):
        response = self.client.get('/task/type/' + 'sdfs')
        self.assertStatus(response, 404)

        response = self.client.get('/task/type/' + str(1000000))
        self.assertStatus(response, 404)

    def test_update_from_dict(self):
        task_type = TaskType.query.first()
        task_type_id = task_type.id

        task_type_dict = dict(
            name='Usuń'
        )

        task_type.update_from_dict(task_type_dict)
        db_session.add(task_type)
        db_session.commit()

        task_type = TaskType.query.filter_by(id=task_type_id).first()

        self.assertIsNotNone(task_type)
        self.assertEqual(task_type_dict['name'], task_type.name)

    def test_update_from_dict_invalid_type(self):
        task_type = TaskType.query.first()
        task_type_id = task_type.id

        task_type_list = [
            'Usuń'
        ]

        with self.assertRaises(TypeError):
            task_type.update_from_dict(task_type_list)
            db_session.add(task_type)
            db_session.commit()

        task_type2 = TaskType.query.filter_by(name='Usuń').first()
        new_task_type = TaskType.query.filter_by(id=task_type_id).first()

        self.assertIsNone(task_type2)
        self.assertEqual(new_task_type, task_type)

    def test_create_task_type_from_dict(self):
        count_before_insert = TaskType.query.count()

        task_type_dict = dict(
            name='Usuń'
        )

        task_type = TaskType.create_from_dict(task_type_dict)
        db_session.add(task_type)
        db_session.commit()

        count_after_insert = TaskType.query.count()

        self.assertEqual(count_before_insert + 1, count_after_insert)

        task_type = TaskType.query.filter_by(name='Usuń').first()

        self.assertIsNotNone(task_type)
        self.assertEqual(task_type_dict['name'], task_type.name)

    def test_create_task_type_from_dict_invalid_type(self):
        count_before_insert = TaskType.query.count()

        task_type_list = [
            'Usuń'
        ]

        with self.assertRaises(TypeError):
            task_type = TaskType.create_from_dict(task_type_list)
            db_session.add(task_type)
            db_session.commit()

        count_after_insert = TaskType.query.count()

        task_type = TaskType.query.filter_by(name='Usuń').first()

        self.assertIsNone(task_type)
        self.assertEqual(count_before_insert, count_after_insert)

    def test_create_task_type_from_dict_invalid_data(self):
        count_before_insert = TaskType.query.count()

        task_type_dict = dict()

        with self.assertRaises(ValidationError):
            task_type = TaskType.create_from_dict(task_type_dict)
            db_session.add(task_type)
            db_session.commit()

        count_after_insert = TaskType.query.count()

        self.assertEqual(count_before_insert, count_after_insert)

    def test_update_task_type(self):
        task_type = TaskType.query.first()

        task_type_dict = dict(
            name='Usuń'
        )

        response = self.client.put(
            '/task/type/' + str(task_type.id),
            data=json.dumps(task_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        task_type = TaskType.query.filter_by(name='Usuń').first()

        self.assertIsNotNone(task_type)

        data = json.loads(response.get_data())

        self.assertEqual(data, task_type.to_dict())

    def test_update_not_existing_task_type(self):
        task_type = TaskType.query.first()

        task_type_dict = dict(
            name='Usuń',
        )

        response = self.client.put(
            '/task/type/' + '123124134',
            data=json.dumps(task_type_dict),
            headers={'Content-Type': 'application/json'}
        )
        self.assertStatus(response, 404)

        response = self.client.put(
            '/task/type/' + 'abc', data=json.dumps(task_type_dict))
        self.assertStatus(response, 404)

        task_type = TaskType.query.filter_by(name='Usuń').first()
        self.assertIsNone(task_type)

    def test_update_task_type_duplicate_data(self):
        task_type_dict = dict(
            name='Usuń',
        )

        task_type = TaskType.create_from_dict(task_type_dict)
        db_session.add(task_type)
        db_session.commit()

        task_type2 = TaskType.query.first()

        response = self.client.put(
            '/task/type/' + str(task_type2.id),
            data=json.dumps(task_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 409)

        task_type2 = TaskType.query.first()

        self.assertNotEqual(task_type2.name, task_type_dict['name'])

    def test_update_task_type_invalid_data(self):
        task_type_dict = dict(name=True)

        task_type = TaskType.query.first()

        response = self.client.put(
            '/task/type/' + str(task_type.id),
            data=json.dumps(task_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)

        task_type = TaskType.query.filter_by(
            name=task_type_dict['name']).first()
        self.assertIsNone(task_type)

    def test_create_task_type(self):
        count_before_insert = TaskType.query.count()

        task_type_dict = dict(
            name='Usuń',
        )

        response = self.client.post(
            '/task/type',
            data=json.dumps(task_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskType.query.count()

        self.assertStatus(response, 201)

        task_type = TaskType.query.filter_by(name='Usuń').first()

        self.assertEqual(count_before_insert + 1, count_after_insert)
        self.assertIsNotNone(task_type)
        self.assertEqual(json.loads(response.get_data()), task_type.to_dict())

    def test_create_task_type_invalid_data(self):
        count_before_insert = TaskType.query.count()

        task_type_dict = dict(
            name=True,
        )

        response = self.client.post(
            '/task/type',
            data=json.dumps(task_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskType.query.count()

        self.assertStatus(response, 400)

        task_type = TaskType.query.filter_by(name='Usuń').first()

        self.assertEqual(count_before_insert, count_after_insert)
        self.assertIsNone(task_type)

    def test_create_task_type_duplicate(self):
        task_type_dict = dict(
            name='Usuń',
        )

        task_type = TaskType.create_from_dict(task_type_dict)
        db_session.add(task_type)
        db_session.commit()

        count_before_insert = TaskType.query.count()

        response = self.client.post(
            '/task/type',
            data=json.dumps(task_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskType.query.count()

        self.assertStatus(response, 409)
        self.assertEqual(count_before_insert, count_after_insert)

    def test_delete_task_type(self):
        task_type = TaskType(name='Usuń')
        db_session.add(task_type)
        db_session.commit()

        task_type_id = task_type.id

        count_before_delete = TaskType.query.count()
        response = self.client.delete('/task/type/' + str(task_type.id))
        count_after_delete = TaskType.query.count()

        self.assertStatus(response, 204)
        self.assertIsNone(TaskType.query.filter_by(id=task_type_id).first())
        self.assertEqual(count_before_delete, count_after_delete + 1)

    def test_delete_not_existing_task_type(self):
        count_before_delete = TaskType.query.count()
        response = self.client.delete('/task/type/' + str(234234234))
        count_after_delete = TaskType.query.count()

        self.assertStatus(response, 404)
        self.assertEqual(count_before_delete, count_after_delete)

    def test_delete_task_type_which_cant_be_deleted(self):
        task = Task.query.first()
        task_type = task.type

        count_before_delete = TaskType.query.count()
        response = self.client.delete('/task/type/' + str(task_type.id))
        count_after_delete = TaskType.query.count()

        self.assertStatus(response, 409)
        self.assertIsNotNone(TaskType.query.filter_by(id=task_type.id).first())
        self.assertEqual(count_before_delete, count_after_delete)

    def test_get_task_type_list(self):
        response = self.client.get('/task/types')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        count = TaskType.query.count()

        self.assertEqual(len(data), count)

    def test_get_task_type_list_by(self):
        response = self.client.get('/task/types?name=Zmiana%20ceny&id=1')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        task_types = TaskType.query.filter_by(name='Zmiana ceny', id=1).all()

        task_types_list = [task_type.to_dict() for task_type in task_types]

        self.assertEqual(len(data), len(task_types))
        self.assertListEqual(data, task_types_list)

    def test_get_task_type_list_by_invalid_parameter(self):
        response = self.client.get(
            '/task/types?task_typename=admin&first_name=Daniel')

        self.assertStatus(response, 400)

    def test_get_task_type_list_complex(self):
        data = dict(
            name=dict(value='Dodaj nowy produkt', operator='!=')
        )

        task_types = query_from_dict(TaskType, data)
        task_types_list = [task_type.to_dict() for task_type in task_types]

        response = self.client.post(
            '/task/types',
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )

        data = json.loads(response.get_data())

        self.assertStatus(response, 200)
        self.assertEqual(data, task_types_list)

    def test_get_task_type_list_complex_invalid_parameter(self):
        data = dict(
            first_name=dict(value='Daniel', operator='!=')
        )

        response = self.client.post(
            '/task/types',
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)

        data = dict(
            name=dict(value1='Daniel', operator='!=')
        )

        response = self.client.post(
            '/task/types',
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)

    def test_get_task_type_list_complex_invalid_type(self):
        data = dict(
            id=dict(value='Daniel', operator='!=')
        )

        response = self.client.post(
            '/task/types',
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)
