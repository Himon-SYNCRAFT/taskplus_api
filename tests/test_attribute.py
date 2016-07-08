from tests.base import Base
from tests.utils import is_json
from flask import json
from models import TaskAttribute, TaskAttributeValue
from database import db_session
from exceptions import ValidationError
import unittest


class TestAttribute(Base):

    def test_can_get_attribute(self):
        attribute = TaskAttribute.query.first()
        response = self.client.get('/task/attribute/' + str(attribute.id))

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        data = json.loads(response.get_data())

        self.assertEqual(data, attribute.to_dict())

    def test_404_if_attribute_not_exist_or_attribute_id_is_invalid(self):
        response = self.client.get('/task/attribute/' + 'sdfs')
        self.assertStatus(response, 404)

        response = self.client.get('/task/attribute/' + str(1000000))
        self.assertStatus(response, 404)

    def test_update_from_dict(self):
        attribute = TaskAttribute.query.first()
        attribute_id = attribute.id

        attribute_dict = dict(
            name='Indeks'
        )

        attribute.update_from_dict(attribute_dict)
        db_session.add(attribute)
        db_session.commit()

        attribute = TaskAttribute.query.filter_by(id=attribute_id).first()

        self.assertIsNotNone(attribute)
        self.assertEqual(attribute_dict['name'], attribute.name)

    def test_update_from_dict_invalid_type(self):
        attribute = TaskAttribute.query.first()
        attribute_id = attribute.id

        attribute_list = [
            'Indeks'
        ]

        with self.assertRaises(TypeError):
            attribute.update_from_dict(attribute_list)
            db_session.add(attribute)
            db_session.commit()

        attribute2 = TaskAttribute.query.filter_by(name='Indeks').first()
        new_attribute = TaskAttribute.query.filter_by(id=attribute_id).first()

        self.assertIsNone(attribute2)
        self.assertEqual(new_attribute, attribute)

    def test_create_attribute_from_dict(self):
        count_before_insert = TaskAttribute.query.count()

        attribute_dict = dict(
            name='Indeks',
            type_id=1
        )

        attribute = TaskAttribute.create_from_dict(attribute_dict)
        db_session.add(attribute)
        db_session.commit()

        count_after_insert = TaskAttribute.query.count()

        self.assertEqual(count_before_insert + 1, count_after_insert)

        attribute = TaskAttribute.query.filter_by(name='Indeks').first()

        self.assertIsNotNone(attribute)
        self.assertEqual(attribute_dict['name'], attribute.name)

    def test_create_attribute_from_dict_invalid_type(self):
        count_before_insert = TaskAttribute.query.count()

        attribute_list = [
            'Indeks'
        ]

        with self.assertRaises(TypeError):
            attribute = TaskAttribute.create_from_dict(attribute_list)
            db_session.add(attribute)
            db_session.commit()

        count_after_insert = TaskAttribute.query.count()

        attribute = TaskAttribute.query.filter_by(name='Indeks').first()

        self.assertIsNone(attribute)
        self.assertEqual(count_before_insert, count_after_insert)

    def test_create_attribute_from_dict_invalid_data(self):
        count_before_insert = TaskAttribute.query.count()

        attribute_dict = dict()

        with self.assertRaises(ValidationError):
            attribute = TaskAttribute.create_from_dict(attribute_dict)
            db_session.add(attribute)
            db_session.commit()

        count_after_insert = TaskAttribute.query.count()

        self.assertEqual(count_before_insert, count_after_insert)

    def test_update_attribute(self):
        attribute = TaskAttribute.query.first()

        attribute_dict = dict(
            name='Indeks'
        )

        response = self.client.put(
            '/task/attribute/' + str(attribute.id),
            data=json.dumps(attribute_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        attribute = TaskAttribute.query.filter_by(name='Indeks').first()

        self.assertIsNotNone(attribute)

        data = json.loads(response.get_data())

        self.assertEqual(data, attribute.to_dict())

    def test_update_not_existing_attribute(self):
        attribute = TaskAttribute.query.first()

        attribute_dict = dict(
            name='Indeks',
        )

        response = self.client.put(
            '/task/attribute/' + '123124134',
            data=json.dumps(attribute_dict),
            headers={'Content-Type': 'application/json'}
        )
        self.assertStatus(response, 404)

        response = self.client.put(
            '/task/attribute/' + 'abc', data=json.dumps(attribute_dict))
        self.assertStatus(response, 404)

        attribute = TaskAttribute.query.filter_by(name='Indeks').first()
        self.assertIsNone(attribute)

    def test_update_attribute_duplicate_data(self):
        attribute_dict = dict(
            name='Indeks',
            type_id=1,
        )

        attribute = TaskAttribute.create_from_dict(attribute_dict)
        db_session.add(attribute)
        db_session.commit()

        attribute2 = TaskAttribute.query.first()

        response = self.client.put(
            '/task/attribute/' + str(attribute2.id),
            data=json.dumps(attribute_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 409)

        attribute2 = TaskAttribute.query.first()

        self.assertNotEqual(attribute2.name, attribute_dict['name'])

    def test_update_attribute_invalid_data(self):
        attribute_dict = dict(name=True)

        attribute = TaskAttribute.query.first()

        response = self.client.put(
            '/task/attribute/' + str(attribute.id),
            data=json.dumps(attribute_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)

        attribute = TaskAttribute.query.filter_by(
            name=attribute_dict['name']).first()
        self.assertIsNone(attribute)

    def test_create_attribute(self):
        count_before_insert = TaskAttribute.query.count()

        attribute_dict = dict(
            name='Indeks',
            type_id=1
        )

        response = self.client.post(
            '/task/attribute',
            data=json.dumps(attribute_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskAttribute.query.count()

        self.assertStatus(response, 201)

        attribute = TaskAttribute.query.filter_by(name='Indeks').first()

        self.assertEqual(count_before_insert + 1, count_after_insert)
        self.assertIsNotNone(attribute)
        self.assertEqual(json.loads(response.get_data()), attribute.to_dict())

    def test_create_attribute_invalid_data(self):
        count_before_insert = TaskAttribute.query.count()

        attribute_dict = dict(
            name=True,
        )

        response = self.client.post(
            '/task/attribute',
            data=json.dumps(attribute_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskAttribute.query.count()

        self.assertStatus(response, 400)

        attribute = TaskAttribute.query.filter_by(name='Indeks').first()

        self.assertEqual(count_before_insert, count_after_insert)
        self.assertIsNone(attribute)

    def test_create_attribute_duplicate(self):
        attribute_dict = dict(
            name='Indeks',
            type_id=1
        )

        attribute = TaskAttribute.create_from_dict(attribute_dict)
        db_session.add(attribute)
        db_session.commit()

        count_before_insert = TaskAttribute.query.count()

        response = self.client.post(
            '/task/attribute',
            data=json.dumps(attribute_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskAttribute.query.count()

        self.assertStatus(response, 409)
        self.assertEqual(count_before_insert, count_after_insert)

    def test_delete_attribute(self):
        attribute = TaskAttribute(name='Indeks', type_id=1)
        db_session.add(attribute)
        db_session.commit()

        attribute_id = attribute.id

        count_before_delete = TaskAttribute.query.count()
        response = self.client.delete('/task/attribute/' + str(attribute.id))
        count_after_delete = TaskAttribute.query.count()

        self.assertStatus(response, 204)
        self.assertIsNone(TaskAttribute.query.filter_by(
            id=attribute_id).first())
        self.assertEqual(count_before_delete, count_after_delete + 1)

    def test_delete_not_existing_attribute(self):
        count_before_delete = TaskAttribute.query.count()
        response = self.client.delete('/task/attribute/' + str(234234234))
        count_after_delete = TaskAttribute.query.count()

        self.assertStatus(response, 404)
        self.assertEqual(count_before_delete, count_after_delete)

    @unittest.skip("This test fail in sqlite but work in postgres. Don't know why.")
    def test_delete_attribute_which_cant_be_deleted(self):
        attribute_value = TaskAttributeValue.query.first()
        attribute = TaskAttribute.query.get(attribute_value.task_attribute_id)

        count_before_delete = TaskAttribute.query.count()
        response = self.client.delete('/task/attribute/' + str(attribute.id))
        count_after_delete = TaskAttribute.query.count()

        self.assertStatus(response, 409)
        self.assertIsNotNone(
            TaskAttribute.query.filter_by(id=attribute.id).first())
        self.assertEqual(count_before_delete, count_after_delete)

    def test_get_attribute_list(self):
        response = self.client.get('/task/attributes')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        count = TaskAttribute.query.count()

        self.assertEqual(len(data), count)

    def test_get_attribute_list_by(self):
        response = self.client.get('/task/attributes?type_id=3&name=Cena&id=2')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        attributes = TaskAttribute.query.filter_by(type_id=3, name='Cena', id=2).all()

        attributes_list = [attribute.to_dict() for attribute in attributes]

        self.assertEqual(len(data), len(attributes))
        self.assertListEqual(data, attributes_list)

    def test_get_attribute_list_by_invalid_parameter(self):
        response = self.client.get(
            '/task/types?attributename=admin&first_name=Daniel')

        self.assertStatus(response, 400)
