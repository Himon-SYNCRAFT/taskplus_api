from tests.base import Base
from tests.utils import is_json
from flask import json
from models import TaskAttributeToTaskType, TaskAttribute
from database import db_session
from exceptions import ValidationError
import unittest


class TestAttributeToType(Base):

    def test_can_get_attribute_to_type(self):
        attribute_to_type = TaskAttributeToTaskType.query.first()
        response = self.client.get(
            '/task/attribute-to-type/' + "{0}/{1}".format(attribute_to_type.task_type_id, attribute_to_type.task_attribute_id))

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        data = json.loads(response.get_data())

        self.assertEqual(data, attribute_to_type.to_dict())

    def test_404_if_attribute_to_type_not_exist_or_attribute_to_type_id_is_invalid(self):
        response = self.client.get('/task/attribute-to-type/' + 'sdfs')
        self.assertStatus(response, 404)

        response = self.client.get('/task/attribute-to-type/' + str(1000000))
        self.assertStatus(response, 404)

    def test_update_from_dict(self):
        attribute_to_type = TaskAttributeToTaskType.query.first()
        task_type_id = attribute_to_type.task_type_id
        task_attribute_id = attribute_to_type.task_attribute_id

        attribute_to_type_dict = dict(
            sort=5,
            rules=''
        )

        attribute_to_type.update_from_dict(attribute_to_type_dict)
        db_session.add(attribute_to_type)
        db_session.commit()

        attribute_to_type = TaskAttributeToTaskType.query.get(
            (task_type_id, task_attribute_id))

        self.assertIsNotNone(attribute_to_type)
        self.assertEqual(attribute_to_type_dict['sort'],
                             attribute_to_type.sort)
        self.assertEqual(attribute_to_type_dict['rules'],
                             attribute_to_type.rules)

    def test_update_from_dict_invalid_type(self):
        attribute_to_type = TaskAttributeToTaskType.query.first()
        task_type_id = attribute_to_type.task_type_id
        task_attribute_id = attribute_to_type.task_attribute_id

        attribute_to_type_list = []

        with self.assertRaises(TypeError):
            attribute_to_type.update_from_dict(attribute_to_type_list)
            db_session.add(attribute_to_type)
            db_session.commit()

        attribute_to_type2 = TaskAttributeToTaskType.query.filter_by(
            task_type_id=1,
            task_attribute_id=3,
            sort=5,
            rules=''
        ).first()

        new_attribute_to_type = TaskAttributeToTaskType.query.get(
            (task_type_id, task_attribute_id))

        self.assertIsNone(attribute_to_type2)
        self.assertEqual(new_attribute_to_type, attribute_to_type)

    def test_create_attribute_to_type_from_dict(self):
        count_before_insert = TaskAttributeToTaskType.query.count()

        attribute_to_type_dict = dict(
            task_type_id=1,
            task_attribute_id=3,
            sort=5,
            rules=''
        )

        attribute_to_type = TaskAttributeToTaskType.create_from_dict(
            attribute_to_type_dict)
        db_session.add(attribute_to_type)
        db_session.commit()

        count_after_insert = TaskAttributeToTaskType.query.count()

        self.assertEqual(count_before_insert + 1, count_after_insert)

        attribute_to_type = TaskAttributeToTaskType.query.filter_by(
            **attribute_to_type_dict).first()

        self.assertIsNotNone(attribute_to_type)
        self.assertDictEqual(attribute_to_type.to_dict(),
                             attribute_to_type_dict)

    def test_create_attribute_to_type_from_dict_invalid_type(self):
        count_before_insert = TaskAttributeToTaskType.query.count()

        attribute_to_type_list = []

        with self.assertRaises(TypeError):
            attribute_to_type = TaskAttributeToTaskType.create_from_dict(
                attribute_to_type_list)
            db_session.add(attribute_to_type)
            db_session.commit()

        count_after_insert = TaskAttributeToTaskType.query.count()
        self.assertEqual(count_before_insert, count_after_insert)

    def test_create_attribute_to_type_from_dict_invalid_data(self):
        count_before_insert = TaskAttributeToTaskType.query.count()

        attribute_to_type_dict = dict()

        with self.assertRaises(ValidationError):
            attribute_to_type = TaskAttributeToTaskType.create_from_dict(
                attribute_to_type_dict)
            db_session.add(attribute_to_type)
            db_session.commit()

        count_after_insert = TaskAttributeToTaskType.query.count()

        self.assertEqual(count_before_insert, count_after_insert)

    def test_update_attribute_to_type(self):
        attribute_to_type = TaskAttributeToTaskType.query.first()

        attribute_to_type_dict = dict(
            sort=5,
            rules=''
        )

        response = self.client.put(
            '/task/attribute-to-type/' +
            "{}/{}".format(attribute_to_type.task_type_id,
                           attribute_to_type.task_attribute_id),
            data=json.dumps(attribute_to_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        attribute_to_type = TaskAttributeToTaskType.query.filter_by(
            **attribute_to_type_dict).first()

        self.assertIsNotNone(attribute_to_type)

        data = json.loads(response.get_data())

        self.assertEqual(data, attribute_to_type.to_dict())

    def test_update_not_existing_attribute_to_type(self):
        attribute_to_type = TaskAttributeToTaskType.query.first()

        attribute_to_type_dict = dict(
            sort=5,
            rules=''
        )

        response = self.client.put(
            '/task/attribute-to-type/123124134/123124134',
            data=json.dumps(attribute_to_type_dict),
            headers={'Content-Type': 'application/json'}
        )
        self.assertStatus(response, 404)

        response = self.client.put(
            '/task/attribute-to-type/' + 'abc', data=json.dumps(attribute_to_type_dict))
        self.assertStatus(response, 404)

        attribute_to_type = TaskAttributeToTaskType.query.filter_by(
            **attribute_to_type_dict).first()
        self.assertIsNone(attribute_to_type)

    def test_update_attribute_to_type_duplicate_data(self):
        attribute_to_type_dict = dict(
            task_type_id=1,
            task_attribute_id=3,
            sort=5,
            rules=''
        )

        attribute_to_type = TaskAttributeToTaskType.create_from_dict(
            attribute_to_type_dict)
        db_session.add(attribute_to_type)
        db_session.commit()

        attribute_to_type2 = TaskAttributeToTaskType.query.filter(
            TaskAttributeToTaskType.task_type_id != attribute_to_type.task_type_id,
            TaskAttributeToTaskType.task_attribute_id != attribute_to_type.task_attribute_id
        ).first()

        response = self.client.put(
            "/task/attribute-to-type/{}/{}".format(attribute_to_type2.task_type_id,
                                                   attribute_to_type2.task_attribute_id),
            data=json.dumps(attribute_to_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 409)

        attribute_to_type2 = TaskAttributeToTaskType.query.filter(
            TaskAttributeToTaskType.task_type_id == attribute_to_type2.task_type_id,
            TaskAttributeToTaskType.task_attribute_id == attribute_to_type2.task_attribute_id
        ).first()

        self.assertNotEqual(attribute_to_type2.sort,
                            attribute_to_type_dict['sort'])
        self.assertNotEqual(attribute_to_type2.rules,
                            attribute_to_type_dict['rules'])

    def test_update_attribute_to_type_invalid_data(self):
        attribute_to_type_dict = dict(
            sort=True,
            rules=True
        )

        attribute_to_type = TaskAttributeToTaskType.query.first()

        response = self.client.put(
            "/task/attribute-to-type/{}/{}".format(attribute_to_type.task_type_id,
                                                   attribute_to_type.task_attribute_id),
            data=json.dumps(attribute_to_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        self.assertStatus(response, 400)

        attribute_to_type = TaskAttributeToTaskType.query.filter_by(
            **attribute_to_type_dict).first()
        self.assertIsNone(attribute_to_type)

    def test_create_attribute_to_type(self):
        count_before_insert = TaskAttributeToTaskType.query.count()

        attribute_to_type_dict = dict(
            task_type_id=1,
            task_attribute_id=3,
            sort=5,
            rules=''
        )

        response = self.client.post(
            '/task/attribute-to-type',
            data=json.dumps(attribute_to_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskAttributeToTaskType.query.count()

        self.assertStatus(response, 201)

        attribute_to_type = TaskAttributeToTaskType.query.filter_by(
            **attribute_to_type_dict).first()

        self.assertEqual(count_before_insert + 1, count_after_insert)
        self.assertIsNotNone(attribute_to_type)
        self.assertEqual(json.loads(response.get_data()),
                         attribute_to_type.to_dict())

    def test_create_attribute_to_type_invalid_data(self):
        count_before_insert = TaskAttributeToTaskType.query.count()

        attribute_to_type_dict = dict(
            task_type_id='asd',
            task_attribute_id='asds',
            sort=True,
            rules=''
        )

        response = self.client.post(
            '/task/attribute-to-type',
            data=json.dumps(attribute_to_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskAttributeToTaskType.query.count()

        self.assertStatus(response, 400)

        self.assertEqual(count_before_insert, count_after_insert)

    def test_create_attribute_to_type_duplicate(self):
        attribute_to_type_dict = dict(
            task_type_id=1,
            task_attribute_id=3,
            sort=5,
            rules=''
        )

        attribute_to_type = TaskAttributeToTaskType.create_from_dict(
            attribute_to_type_dict)
        db_session.add(attribute_to_type)
        db_session.commit()

        count_before_insert = TaskAttributeToTaskType.query.count()

        response = self.client.post(
            '/task/attribute-to-type',
            data=json.dumps(attribute_to_type_dict),
            headers={'Content-Type': 'application/json'}
        )

        count_after_insert = TaskAttributeToTaskType.query.count()

        self.assertStatus(response, 409)
        self.assertEqual(count_before_insert, count_after_insert)

    def test_delete_attribute_to_type(self):
        attribute_to_type = TaskAttributeToTaskType(
            task_type_id=1,
            task_attribute_id=3,
            sort=5,
            rules=''
        )
        db_session.add(attribute_to_type)
        db_session.commit()

        count_before_delete = TaskAttributeToTaskType.query.count()
        response = self.client.delete(
            '/task/attribute-to-type/' + "{}/{}".format(attribute_to_type.task_type_id, attribute_to_type.task_attribute_id))
        count_after_delete = TaskAttributeToTaskType.query.count()

        self.assertStatus(response, 204)
        self.assertIsNone(TaskAttributeToTaskType.query.filter_by(
            task_type_id=1,
            task_attribute_id=3,
            sort=5,
            rules=''
        ).first())
        self.assertEqual(count_before_delete, count_after_delete + 1)

    def test_delete_not_existing_attribute_to_type(self):
        count_before_delete = TaskAttributeToTaskType.query.count()
        response = self.client.delete(
            '/task/attribute-to-type/234234234/234234234')
        count_after_delete = TaskAttributeToTaskType.query.count()

        self.assertStatus(response, 404)
        self.assertEqual(count_before_delete, count_after_delete)

    def test_get_attribute_to_type_list(self):
        response = self.client.get('/task/attribute-to-types')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        count = TaskAttributeToTaskType.query.count()

        self.assertEqual(len(data), count)

    def test_get_attribute_to_type_list_by(self):
        response = self.client.get('/task/attribute-to-types?task_type_id=1')

        self.assertStatus(response, 200)

        data = json.loads(response.get_data())
        attribute_to_types = TaskAttributeToTaskType.query.filter_by(
            task_type_id=1).all()

        attribute_to_types_list = [attribute_to_type.to_dict()
                                   for attribute_to_type in attribute_to_types]

        self.assertEqual(len(data), len(attribute_to_types))
        self.assertListEqual(data, attribute_to_types_list)

    def test_get_attribute_to_type_list_by_invalid_parameter(self):
        response = self.client.get(
            '/task/attribute-to-types?attribute_to_typename=admin&first_name=Daniel')

        self.assertStatus(response, 400)
