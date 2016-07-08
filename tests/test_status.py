from tests.base import Base
from tests.utils import is_json
from flask import json
from models import TaskStatus, Task
from database import db_session
from exceptions import ValidationError


class TestStatus(Base):

    def test_can_get_status(self):
        status = TaskStatus.query.first()
        response = self.client.get('/task/status/' + str(status.id))

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        data = json.loads(response.get_data())

        self.assertEqual(data, status.to_dict())

    def test_404_if_status_not_exist_or_status_id_is_invalid(self):
        response = self.client.get('/task/status/' + 'sdfs')
        self.assertStatus(response, 404)

        response = self.client.get('/task/status/' + str(1000000))
        self.assertStatus(response, 404)

    def test_update_from_dict(self):
        status = TaskStatus.query.first()
        status_id = status.id

        status_dict = dict(
            name='Odroczone'
        )

        status.update_from_dict(status_dict)
        db_session.add(status)
        db_session.commit()

        status = TaskStatus.query.filter_by(id=status_id).first()

        self.assertIsNotNone(status)
        self.assertEqual(status_dict['name'], status.name)

    def test_update_from_dict_invalid_type(self):
        status = TaskStatus.query.first()
        status_id = status.id

        status_list = [
            'Odroczone'
        ]

        with self.assertRaises(TypeError):
            status.update_from_dict(status_list)
            db_session.add(status)
            db_session.commit()

        status2 = TaskStatus.query.filter_by(name='Odroczone').first()
        new_status = TaskStatus.query.filter_by(id=status_id).first()

        self.assertIsNone(status2)
        self.assertEqual(new_status, status)

    def test_create_status_from_dict(self):
        count_before_insert = TaskStatus.query.count()

        status_dict = dict(
            name='Odroczone'
        )

        status = TaskStatus.create_from_dict(status_dict)
        db_session.add(status)
        db_session.commit()

        count_after_insert = TaskStatus.query.count()

        self.assertEqual(count_before_insert + 1, count_after_insert)

        status = TaskStatus.query.filter_by(name='Odroczone').first()

        self.assertIsNotNone(status)
        self.assertEqual(status_dict['name'], status.name)

    def test_create_status_from_dict_invalid_type(self):
        count_before_insert = TaskStatus.query.count()

        status_list = [
            'Odroczone'
        ]

        with self.assertRaises(TypeError):
            status = TaskStatus.create_from_dict(status_list)
            db_session.add(status)
            db_session.commit()

        count_after_insert = TaskStatus.query.count()

        status = TaskStatus.query.filter_by(name='Odroczone').first()

        self.assertIsNone(status)
        self.assertEqual(count_before_insert, count_after_insert)

    def test_create_status_from_dict_invalid_data(self):
        count_before_insert = TaskStatus.query.count()

        status_dict = dict()

        with self.assertRaises(ValidationError):
            status = TaskStatus.create_from_dict(status_dict)
            db_session.add(status)
            db_session.commit()

        count_after_insert = TaskStatus.query.count()

        self.assertEqual(count_before_insert, count_after_insert)

    def test_update_status(self):
        status = TaskStatus.query.first()

        status_dict = dict(
            name='Odroczone'
        )

        response = self.client.put(
            '/task/status/' + str(status.id),
            data=json.dumps(status_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        status = TaskStatus.query.filter_by(name='Odroczone').first()

        self.assertIsNotNone(status)

        data = json.loads(response.get_data())

        self.assertEqual(data, status.to_dict())

    def test_update_not_existing_status(self):
        status = TaskStatus.query.first()

        status_dict = dict(
            name='Odroczone',
        )

        response = self.client.put(
            '/task/status/' + '123124134',
            data=json.dumps(status_dict),
            headers={'Content-Type': 'application/json'}
        )
        self.assertStatus(response, 404)

        response = self.client.put(
            '/task/status/' + 'abc', data=json.dumps(status_dict))
        self.assertStatus(response, 404)

        status = TaskStatus.query.filter_by(name='Odroczone').first()
        self.assertIsNone(status)

    def test_update_status_duplicate_data(self):
        status_dict = dict(
            name='Odroczone',
        )

        status = TaskStatus.create_from_dict(status_dict)
        db_session.add(status)
        db_session.commit()

        status2 = TaskStatus.query.first()

        response = self.client.put(
            '/task/status/' + str(status2.id),
            data=json.dumps(status_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 409)

        status2 = TaskStatus.query.first()

        self.assertNotEqual(status2.name, status_dict['name'])

    def test_update_status_invalid_data(self):
        status_dict = dict(name=True)

        status = TaskStatus.query.first()

        response = self.client.put(
            '/task/status/' + str(status.id),
            data=json.dumps(status_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)

        status = TaskStatus.query.filter_by(name=status_dict['name']).first()
        self.assertIsNone(status)

    def test_create_status(self):
        count_before_insert = TaskStatus.query.count()

        status_dict = dict(
            name='Odroczone',
        )

        response = self.client.post(
            '/task/status',
            data=json.dumps(status_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskStatus.query.count()

        self.assertStatus(response, 201)

        status = TaskStatus.query.filter_by(name='Odroczone').first()

        self.assertEqual(count_before_insert + 1, count_after_insert)
        self.assertIsNotNone(status)
        self.assertEqual(json.loads(response.get_data()), status.to_dict())

    def test_create_status_invalid_data(self):
        count_before_insert = TaskStatus.query.count()

        status_dict = dict(
            name=True,
        )

        response = self.client.post(
            '/task/status',
            data=json.dumps(status_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskStatus.query.count()

        self.assertStatus(response, 400)

        status = TaskStatus.query.filter_by(name='Odroczone').first()

        self.assertEqual(count_before_insert, count_after_insert)
        self.assertIsNone(status)

    def test_create_status_duplicate(self):
        status_dict = dict(
            name='Odroczone',
        )

        status = TaskStatus.create_from_dict(status_dict)
        db_session.add(status)
        db_session.commit()

        count_before_insert = TaskStatus.query.count()

        response = self.client.post(
            '/task/status',
            data=json.dumps(status_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskStatus.query.count()

        self.assertStatus(response, 409)
        self.assertEqual(count_before_insert, count_after_insert)

    def test_delete_status(self):
        status = TaskStatus(name='Odroczone')
        db_session.add(status)
        db_session.commit()

        status_id = status.id

        count_before_delete = TaskStatus.query.count()
        response = self.client.delete('/task/status/' + str(status.id))
        count_after_delete = TaskStatus.query.count()

        self.assertStatus(response, 204)
        self.assertIsNone(TaskStatus.query.filter_by(id=status_id).first())
        self.assertEqual(count_before_delete, count_after_delete + 1)

    def test_delete_not_existing_status(self):
        count_before_delete = TaskStatus.query.count()
        response = self.client.delete('/task/status/' + str(234234234))
        count_after_delete = TaskStatus.query.count()

        self.assertStatus(response, 404)
        self.assertEqual(count_before_delete, count_after_delete)

    def test_delete_status_which_cant_be_deleted(self):
        task = Task.query.first()
        status = task.status

        count_before_delete = TaskStatus.query.count()
        response = self.client.delete('/task/status/' + str(status.id))
        count_after_delete = TaskStatus.query.count()

        self.assertStatus(response, 409)
        self.assertIsNotNone(TaskStatus.query.filter_by(id=status.id).first())
        self.assertEqual(count_before_delete, count_after_delete)

    def test_get_status_list(self):
        response = self.client.get('/task/statuses')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        count = TaskStatus.query.count()

        self.assertEqual(len(data), count)

    def test_get_status_list_by(self):
        response = self.client.get('/task/statuses?name=Nowe&id=1')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        statuss = TaskStatus.query.filter_by(name='Nowe', id=1).all()

        statuss_list = [status.to_dict() for status in statuss]

        self.assertEqual(len(data), len(statuss))
        self.assertListEqual(data, statuss_list)

    def test_get_status_list_by_invalid_parameter(self):
        response = self.client.get(
            '/task/statuses?statusname=admin&first_name=Daniel')

        self.assertStatus(response, 400)
