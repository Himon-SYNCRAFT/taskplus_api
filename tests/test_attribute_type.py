from tests.base import Base
from tests.utils import is_json
from flask import json
from models import TaskAttributeType, TaskAttribute
from database import db_session
from exceptions import ValidationError
import unittest


class TestAttributeType(Base):

    def test_can_get_attribute_type(self):
        attribute_type = TaskAttributeType.query.first()
        response = self.client.get('/task/attribute/type/' + str(attribute_type.id))

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        data = json.loads(response.get_data())

        self.assertEqual(data, attribute_type.to_dict())

    def test_404_if_attribute_type_not_exist_or_attribute_type_id_is_invalid(self):
        response = self.client.get('/task/attribute/type/' + 'sdfs')
        self.assertStatus(response, 404)

        response = self.client.get('/task/attribute/type/' + str(1000000))
        self.assertStatus(response, 404)

    def test_update_from_dict(self):
        attribute_type = TaskAttributeType.query.first()
        attribute_type_id = attribute_type.id

        attribute_type_dict = dict(
            name='bool'
        )

        attribute_type.update_from_dict(attribute_type_dict)
        db_session.add(attribute_type)
        db_session.commit()

        attribute_type = TaskAttributeType.query.filter_by(id=attribute_type_id).first()

        self.assertIsNotNone(attribute_type)
        self.assertEqual(attribute_type_dict['name'], attribute_type.name)

    def test_update_from_dict_invalid_type(self):
        attribute_type = TaskAttributeType.query.first()
        attribute_type_id = attribute_type.id

        attribute_type_list = [
            'Usuń'
        ]

        with self.assertRaises(TypeError):
            attribute_type.update_from_dict(attribute_type_list)
            db_session.add(attribute_type)
            db_session.commit()

        attribute_type2 = TaskAttributeType.query.filter_by(name='bool').first()
        new_attribute_type = TaskAttributeType.query.filter_by(id=attribute_type_id).first()

        self.assertIsNone(attribute_type2)
        self.assertEqual(new_attribute_type, attribute_type)

    def test_create_attribute_type_from_dict(self):
        count_before_insert = TaskAttributeType.query.count()

        attribute_type_dict = dict(
            name='bool'
        )

        attribute_type = TaskAttributeType.create_from_dict(attribute_type_dict)
        db_session.add(attribute_type)
        db_session.commit()

        count_after_insert = TaskAttributeType.query.count()

        self.assertEqual(count_before_insert + 1, count_after_insert)

        attribute_type = TaskAttributeType.query.filter_by(name='bool').first()

        self.assertIsNotNone(attribute_type)
        self.assertEqual(attribute_type_dict['name'], attribute_type.name)

    def test_create_attribute_type_from_dict_invalid_type(self):
        count_before_insert = TaskAttributeType.query.count()

        attribute_type_list = [
            'Usuń'
        ]

        with self.assertRaises(TypeError):
            attribute_type = TaskAttributeType.create_from_dict(attribute_type_list)
            db_session.add(attribute_type)
            db_session.commit()

        count_after_insert = TaskAttributeType.query.count()

        attribute_type = TaskAttributeType.query.filter_by(name='bool').first()

        self.assertIsNone(attribute_type)
        self.assertEqual(count_before_insert, count_after_insert)

    def test_create_attribute_type_from_dict_invalid_data(self):
        count_before_insert = TaskAttributeType.query.count()

        attribute_type_dict = dict()

        with self.assertRaises(ValidationError):
            attribute_type = TaskAttributeType.create_from_dict(attribute_type_dict)
            db_session.add(attribute_type)
            db_session.commit()

        count_after_insert = TaskAttributeType.query.count()

        self.assertEqual(count_before_insert, count_after_insert)

    def test_update_attribute_type(self):
        attribute_type = TaskAttributeType.query.first()

        attribute_type_dict = dict(
            name='bool'
        )

        response = self.client.put(
            '/task/attribute/type/' + str(attribute_type.id),
            data=json.dumps(attribute_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        attribute_type = TaskAttributeType.query.filter_by(name='bool').first()

        self.assertIsNotNone(attribute_type)

        data = json.loads(response.get_data())

        self.assertEqual(data, attribute_type.to_dict())

    def test_update_not_existing_attribute_type(self):
        attribute_type = TaskAttributeType.query.first()

        attribute_type_dict = dict(
            name='bool',
        )

        response = self.client.put(
            '/task/attribute/type/' + '123124134',
            data=json.dumps(attribute_type_dict),
            headers={'Content-Type': 'application/json'}
        )
        self.assertStatus(response, 404)

        response = self.client.put(
            '/task/attribute/type/' + 'abc', data=json.dumps(attribute_type_dict))
        self.assertStatus(response, 404)

        attribute_type = TaskAttributeType.query.filter_by(name='bool').first()
        self.assertIsNone(attribute_type)

    def test_update_attribute_type_duplicate_data(self):
        attribute_type_dict = dict(
            name='bool',
        )

        attribute_type = TaskAttributeType.create_from_dict(attribute_type_dict)
        db_session.add(attribute_type)
        db_session.commit()

        attribute_type2 = TaskAttributeType.query.first()

        response = self.client.put(
            '/task/attribute/type/' + str(attribute_type2.id),
            data=json.dumps(attribute_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 409)

        attribute_type2 = TaskAttributeType.query.first()

        self.assertNotEqual(attribute_type2.name, attribute_type_dict['name'])

    def test_update_attribute_type_invalid_data(self):
        attribute_type_dict = dict(name=True)

        attribute_type = TaskAttributeType.query.first()

        response = self.client.put(
            '/task/attribute/type/' + str(attribute_type.id),
            data=json.dumps(attribute_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)

        attribute_type = TaskAttributeType.query.filter_by(
            name=attribute_type_dict['name']).first()
        self.assertIsNone(attribute_type)

    def test_create_attribute_type(self):
        count_before_insert = TaskAttributeType.query.count()

        attribute_type_dict = dict(
            name='bool',
        )

        response = self.client.post(
            '/task/attribute/type',
            data=json.dumps(attribute_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskAttributeType.query.count()

        self.assertStatus(response, 201)

        attribute_type = TaskAttributeType.query.filter_by(name='bool').first()

        self.assertEqual(count_before_insert + 1, count_after_insert)
        self.assertIsNotNone(attribute_type)
        self.assertEqual(json.loads(response.get_data()), attribute_type.to_dict())

    def test_create_attribute_type_invalid_data(self):
        count_before_insert = TaskAttributeType.query.count()

        attribute_type_dict = dict(
            name=True,
        )

        response = self.client.post(
            '/task/attribute/type',
            data=json.dumps(attribute_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskAttributeType.query.count()

        self.assertStatus(response, 400)

        attribute_type = TaskAttributeType.query.filter_by(name='bool').first()

        self.assertEqual(count_before_insert, count_after_insert)
        self.assertIsNone(attribute_type)

    def test_create_attribute_type_duplicate(self):
        attribute_type_dict = dict(
            name='bool',
        )

        attribute_type = TaskAttributeType.create_from_dict(attribute_type_dict)
        db_session.add(attribute_type)
        db_session.commit()

        count_before_insert = TaskAttributeType.query.count()

        response = self.client.post(
            '/task/attribute/type',
            data=json.dumps(attribute_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskAttributeType.query.count()

        self.assertStatus(response, 409)
        self.assertEqual(count_before_insert, count_after_insert)

    def test_delete_attribute_type(self):
        attribute_type = TaskAttributeType(name='bool')
        db_session.add(attribute_type)
        db_session.commit()

        attribute_type_id = attribute_type.id

        count_before_delete = TaskAttributeType.query.count()
        response = self.client.delete('/task/attribute/type/' + str(attribute_type.id))
        count_after_delete = TaskAttributeType.query.count()

        self.assertStatus(response, 204)
        self.assertIsNone(TaskAttributeType.query.filter_by(id=attribute_type_id).first())
        self.assertEqual(count_before_delete, count_after_delete + 1)

    def test_delete_not_existing_attribute_type(self):
        count_before_delete = TaskAttributeType.query.count()
        response = self.client.delete('/task/attribute/type/' + str(234234234))
        count_after_delete = TaskAttributeType.query.count()

        self.assertStatus(response, 404)
        self.assertEqual(count_before_delete, count_after_delete)

    @unittest.skip("Test fail in sqlite. Work properly on postgres")
    def test_delete_attribute_type_which_cant_be_deleted(self):
        task_attribute = TaskAttribute.query.first()
        attribute_type = TaskAttributeType.query.get(task_attribute.type_id)

        count_before_delete = TaskAttributeType.query.count()
        response = self.client.delete('/task/attribute/type/' + str(attribute_type.id))
        count_after_delete = TaskAttributeType.query.count()

        self.assertStatus(response, 409)
        self.assertIsNotNone(TaskAttributeType.query.filter_by(id=attribute_type.id).first())
        self.assertEqual(count_before_delete, count_after_delete)

    def test_get_attribute_type_list(self):
        response = self.client.get('/task/attribute/types')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        count = TaskAttributeType.query.count()

        self.assertEqual(len(data), count)

    def test_get_attribute_type_list_by(self):
        response = self.client.get('/task/attribute/types?name=json')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        attribute_types = TaskAttributeType.query.filter_by(name='json').all()

        attribute_types_list = [attribute_type.to_dict() for attribute_type in attribute_types]

        self.assertEqual(len(data), len(attribute_types))
        self.assertListEqual(data, attribute_types_list)

    def test_get_attribute_type_list_by_id(self):
        response = self.client.get('/task/attribute/types?id=1')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        attribute_types = TaskAttributeType.query.filter_by(id=1).all()

        attribute_types_list = [attribute_type.to_dict() for attribute_type in attribute_types]

        self.assertEqual(len(data), len(attribute_types))
        self.assertListEqual(data, attribute_types_list)

    def test_get_attribute_type_list_by_invalid_parameter(self):
        response = self.client.get(
            '/task/attribute/types?attribute_typename=admin&first_name=Daniel')

        self.assertStatus(response, 400)
