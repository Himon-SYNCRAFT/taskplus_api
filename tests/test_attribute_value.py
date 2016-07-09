from tests.base import Base
from tests.utils import is_json
from flask import json
from models import TaskAttributeValue, TaskAttribute
from database import db_session
from exceptions import ValidationError
from utils import query_from_dict
import unittest


class TestAttributeValue(Base):

    def test_can_get_attribute_value(self):
        attribute_value = TaskAttributeValue.query.first()
        response = self.client.get(
            '/task/attribute/value/' + "{0}/{1}".format(attribute_value.task_id, attribute_value.task_attribute_id))

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        data = json.loads(response.get_data())

        self.assertEqual(data, attribute_value.to_dict())

    def test_404_if_attribute_value_not_exist_or_attribute_value_id_is_invalid(self):
        response = self.client.get('/task/attribute/value/' + 'sdfs')
        self.assertStatus(response, 404)

        response = self.client.get('/task/attribute/value/' + str(1000000))
        self.assertStatus(response, 404)

    def test_update_from_dict(self):
        attribute_value = TaskAttributeValue.query.first()

        attribute_value_dict = dict(
            value='tmp',
            task_id=1,
            task_attribute_id=1
        )

        attribute_value.update_from_dict(attribute_value_dict)
        db_session.add(attribute_value)
        db_session.commit()

        attribute_value = TaskAttributeValue.query.filter_by(
            **attribute_value_dict).first()

        self.assertIsNotNone(attribute_value)
        self.assertEqual(attribute_value_dict['value'], attribute_value.value)

    def test_update_from_dict_invalid_type(self):
        attribute_value = TaskAttributeValue.query.first()
        task_id = attribute_value.task_id
        task_attribute_id = attribute_value.task_attribute_id

        attribute_value_list = [
            'tmp'
        ]

        with self.assertRaises(TypeError):
            attribute_value.update_from_dict(attribute_value_list)
            db_session.add(attribute_value)
            db_session.commit()

        attribute_value2 = TaskAttributeValue.query.filter_by(
            value='tmp').first()
        new_attribute_value = TaskAttributeValue.query.get(
            (task_id, task_attribute_id))

        self.assertIsNone(attribute_value2)
        self.assertEqual(new_attribute_value, attribute_value)

    def test_create_attribute_value_from_dict(self):
        count_before_insert = TaskAttributeValue.query.count()

        attribute_value_dict = dict(
            value='tmp',
            task_id=1,
            task_attribute_id=1
        )

        attribute_value = TaskAttributeValue.create_from_dict(
            attribute_value_dict)
        db_session.add(attribute_value)
        db_session.commit()

        count_after_insert = TaskAttributeValue.query.count()

        self.assertEqual(count_before_insert + 1, count_after_insert)

        attribute_value = TaskAttributeValue.query.filter_by(
            value='tmp',
            task_id=1,
            task_attribute_id=1
        ).first()

        self.assertIsNotNone(attribute_value)
        self.assertEqual(attribute_value_dict['value'], attribute_value.value)
        self.assertEqual(attribute_value_dict[
                         'task_id'], attribute_value.task_id)
        self.assertEqual(attribute_value_dict[
                         'task_attribute_id'], attribute_value.task_attribute_id)

    def test_create_attribute_value_from_dict_invalid_type(self):
        count_before_insert = TaskAttributeValue.query.count()

        attribute_value_list = [
            'tmp'
        ]

        with self.assertRaises(TypeError):
            attribute_value = TaskAttributeValue.create_from_dict(
                attribute_value_list)
            db_session.add(attribute_value)
            db_session.commit()

        count_after_insert = TaskAttributeValue.query.count()

        attribute_value = TaskAttributeValue.query.filter_by(
            value='tmp').first()

        self.assertIsNone(attribute_value)
        self.assertEqual(count_before_insert, count_after_insert)

    def test_create_attribute_value_from_dict_invalid_data(self):
        count_before_insert = TaskAttributeValue.query.count()

        attribute_value_dict = dict()

        with self.assertRaises(ValidationError):
            attribute_value = TaskAttributeValue.create_from_dict(
                attribute_value_dict)
            db_session.add(attribute_value)
            db_session.commit()

        count_after_insert = TaskAttributeValue.query.count()

        self.assertEqual(count_before_insert, count_after_insert)

    def test_update_attribute_value(self):
        attribute_value = TaskAttributeValue.query.first()

        attribute_value_dict = dict(
            value='tmp',
            task_id=1,
            task_attribute_id=1
        )

        response = self.client.put(
            '/task/attribute/value/' +
            "{}/{}".format(attribute_value.task_id,
                           attribute_value.task_attribute_id),
            data=json.dumps(attribute_value_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        attribute_value = TaskAttributeValue.query.filter_by(
            **attribute_value_dict).first()

        self.assertIsNotNone(attribute_value)

        data = json.loads(response.get_data())

        self.assertEqual(data, attribute_value.to_dict())

    def test_update_not_existing_attribute_value(self):
        attribute_value = TaskAttributeValue.query.first()

        attribute_value_dict = dict(
            value='tmp',
            task_id=1,
            task_attribute_id=1
        )

        response = self.client.put(
            '/task/attribute/value/' + '123124134/123124134',
            data=json.dumps(attribute_value_dict),
            headers={'Content-Type': 'application/json'}
        )
        self.assertStatus(response, 404)

        response = self.client.put(
            '/task/attribute/value/' + 'abc', data=json.dumps(attribute_value_dict))
        self.assertStatus(response, 404)

        attribute_value = TaskAttributeValue.query.filter_by(
            **attribute_value_dict).first()
        self.assertIsNone(attribute_value)

    def test_update_attribute_value_duplicate_data(self):
        attribute_value_dict = dict(
            value='tmp',
            task_id=1,
            task_attribute_id=1
        )

        attribute_value = TaskAttributeValue.create_from_dict(
            attribute_value_dict)
        db_session.add(attribute_value)
        db_session.commit()

        attribute_value2 = TaskAttributeValue.query.filter(
            TaskAttributeValue.task_id != 1, TaskAttributeValue.task_attribute_id != 1).first()

        response = self.client.put(
            "/task/attribute/value/{}/{}".format(attribute_value2.task_id,
                                                 attribute_value2.task_attribute_id),
            data=json.dumps(attribute_value_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 409)

        attribute_value2 = TaskAttributeValue.query.filter(
            TaskAttributeValue.task_id == attribute_value2.task_id,
            TaskAttributeValue.task_attribute_id == attribute_value2.task_attribute_id
        ).first()

        self.assertNotEqual(attribute_value2.value,
                            attribute_value_dict['value'])
        self.assertNotEqual(attribute_value2.task_id,
                            attribute_value_dict['task_id'])
        self.assertNotEqual(attribute_value2.task_attribute_id,
                            attribute_value_dict['task_attribute_id'])

    def test_update_attribute_value_invalid_data(self):
        attribute_value_dict = dict(value=True)

        attribute_value = TaskAttributeValue.query.first()

        response = self.client.put(
            "/task/attribute/value/{}/{}".format(attribute_value.task_id,
                                                 attribute_value.task_attribute_id),
            data=json.dumps(attribute_value_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)

        attribute_value = TaskAttributeValue.query.filter_by(
            value=attribute_value_dict['value']).first()
        self.assertIsNone(attribute_value)

    def test_update_attribute_value_invalid_indices(self):
        attribute_value_dict = dict(
            value='tmp',
            task_id=100,
            task_attribute_id=100
        )

        attribute_value = TaskAttributeValue.query.first()

        response = self.client.put(
            "/task/attribute/value/{}/{}".format(attribute_value.task_id,
                                                 attribute_value.task_attribute_id),
            data=json.dumps(attribute_value_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 409)

        attribute_value = TaskAttributeValue.query.filter_by(
            **attribute_value_dict).first()
        self.assertIsNone(attribute_value)

    def test_create_attribute_value(self):
        count_before_insert = TaskAttributeValue.query.count()

        attribute_value_dict = dict(
            value='tmp',
            task_id=1,
            task_attribute_id=1
        )

        response = self.client.post(
            '/task/attribute/value',
            data=json.dumps(attribute_value_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskAttributeValue.query.count()

        self.assertStatus(response, 201)

        attribute_value = TaskAttributeValue.query.filter_by(
            **attribute_value_dict).first()

        self.assertEqual(count_before_insert + 1, count_after_insert)
        self.assertIsNotNone(attribute_value)
        self.assertEqual(json.loads(response.get_data()),
                         attribute_value.to_dict())

    def test_create_attribute_value_invalid_data(self):
        count_before_insert = TaskAttributeValue.query.count()

        attribute_value_dict = dict(
            value=True,
        )

        response = self.client.post(
            '/task/attribute/value',
            data=json.dumps(attribute_value_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskAttributeValue.query.count()

        self.assertStatus(response, 400)

        attribute_value = TaskAttributeValue.query.filter_by(
            **attribute_value_dict).first()

        self.assertEqual(count_before_insert, count_after_insert)
        self.assertIsNone(attribute_value)

    def test_create_attribute_value_invalid_indices(self):
        count_before_insert = TaskAttributeValue.query.count()

        attribute_value_dict = dict(
            value='tmp',
            task_id=100,
            task_attribute_id=100
        )

        response = self.client.post(
            '/task/attribute/value',
            data=json.dumps(attribute_value_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskAttributeValue.query.count()

        self.assertStatus(response, 409)

        attribute_value = TaskAttributeValue.query.filter_by(
            **attribute_value_dict).first()

        self.assertEqual(count_before_insert, count_after_insert)
        self.assertIsNone(attribute_value)

    def test_create_attribute_value_duplicate(self):
        attribute_value_dict = dict(
            value='tmp',
            task_id=1,
            task_attribute_id=1
        )

        attribute_value = TaskAttributeValue.create_from_dict(
            attribute_value_dict)
        db_session.add(attribute_value)
        db_session.commit()

        count_before_insert = TaskAttributeValue.query.count()

        response = self.client.post(
            '/task/attribute/value',
            data=json.dumps(attribute_value_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskAttributeValue.query.count()

        self.assertStatus(response, 409)
        self.assertEqual(count_before_insert, count_after_insert)

    def test_delete_attribute_value(self):
        attribute_value = TaskAttributeValue(value='tmp',
                                             task_id=1,
                                             task_attribute_id=1)
        db_session.add(attribute_value)
        db_session.commit()

        count_before_delete = TaskAttributeValue.query.count()
        response = self.client.delete(
            '/task/attribute/value/' + "{}/{}".format(attribute_value.task_id, attribute_value.task_attribute_id))
        count_after_delete = TaskAttributeValue.query.count()

        self.assertStatus(response, 204)
        self.assertIsNone(TaskAttributeValue.query.filter_by(
            value='tmp',
            task_id=1,
            task_attribute_id=1
        ).first())
        self.assertEqual(count_before_delete, count_after_delete + 1)

    def test_delete_not_existing_attribute_value(self):
        count_before_delete = TaskAttributeValue.query.count()
        response = self.client.delete(
            '/task/attribute/value/234234234/234234234')
        count_after_delete = TaskAttributeValue.query.count()

        self.assertStatus(response, 404)
        self.assertEqual(count_before_delete, count_after_delete)

    def test_get_attribute_value_list(self):
        response = self.client.get('/task/attribute/values')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        count = TaskAttributeValue.query.count()

        self.assertEqual(len(data), count)

    def test_get_attribute_value_list_by(self):
        response = self.client.get('/task/attribute/values?task_id=1')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        attribute_values = TaskAttributeValue.query.filter_by(
            task_id=1).all()

        attribute_values_list = [attribute_value.to_dict()
                                 for attribute_value in attribute_values]

        self.assertEqual(len(data), len(attribute_values))
        self.assertListEqual(data, attribute_values_list)

    def test_get_attribute_value_list_by_invalid_parameter(self):
        response = self.client.get(
            '/task/attribute/values?attribute_valuename=admin&first_name=Daniel')

        self.assertStatus(response, 400)

    def test_get_value_list_complex(self):
        data = dict(
            value=dict(value='10.00', operator='!=')
        )

        values = query_from_dict(TaskAttributeValue, data)
        values_list = [value.to_dict() for value in values]

        response = self.client.post(
            '/task/attribute/values',
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )

        data = json.loads(response.get_data())

        self.assertStatus(response, 200)
        self.assertEqual(data, values_list)

    def test_get_value_list_complex_invalid_parameter(self):
        data = dict(
            first_name=dict(value='Daniel', operator='!=')
        )

        response = self.client.post(
            '/task/attribute/values',
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)

        data = dict(
            value=dict(value1='Daniel', operator='!=')
        )

        response = self.client.post(
            '/task/attribute/values',
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)

    def test_get_value_list_complex_invalid_type(self):
        data = dict(
            task_id=dict(value='Daniel', operator='!=')
        )

        response = self.client.post(
            '/task/attribute/values',
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)
