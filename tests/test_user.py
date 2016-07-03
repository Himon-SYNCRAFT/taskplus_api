from tests.base import Base
from tests.utils import is_json
from flask import json
from models import User
from database import db_session
from exceptions import ValidationError


class TestUser(Base):

    def test_can_get_user(self):
        user = User.query.first()
        response = self.client.get('/user/' + str(user.id))

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        data = json.loads(response.get_data())

        self.assertEqual(data, user.to_dict())

    def test_404_if_user_not_exist_or_user_id_is_invalid(self):
        response = self.client.get('/user/' + 'sdfs')
        self.assertStatus(response, 404)

        response = self.client.get('/user/' + str(1000000))
        self.assertStatus(response, 404)

    def test_update_from_dict(self):
        user = User.query.first()
        user_id = user.id

        user_dict = dict(
            login='konbis',
            first_name='Konrad',
            last_name='Biś',
            is_creator=True,
            is_contractor=True,
            is_admin=False,
            junk='abcd'
        )

        user.update_from_dict(user_dict)
        db_session.add(user)
        db_session.commit()

        user = User.query.filter_by(id=user_id).first()

        self.assertIsNotNone(user)
        self.assertEqual(user_dict['login'], user.login)
        self.assertEqual(user_dict['first_name'], user.first_name)
        self.assertEqual(user_dict['last_name'], user.last_name)
        self.assertEqual(user_dict['is_creator'], user.is_creator)
        self.assertEqual(user_dict['is_contractor'], user.is_contractor)
        self.assertEqual(user_dict['is_admin'], user.is_admin)

    def test_update_from_dict_invalid_type(self):
        user = User.query.first()
        user_id = user.id

        user_list = [
            'konbis',
            'Konrad',
            'Biś',
            True,
            True,
            False,
            'abcd'
        ]

        with self.assertRaises(TypeError):
            user.update_from_dict(user_list)
            db_session.add(user)
            db_session.commit()

        user2 = User.query.filter_by(login='konbis').first()
        new_user = User.query.filter_by(id=user_id).first()

        self.assertIsNone(user2)
        self.assertEqual(new_user, user)

    def test_create_user_from_dict(self):
        count_before_insert = User.query.count()

        user_dict = dict(
            login='konbis',
            first_name='Konrad',
            last_name='Biś',
            password='secret',
            is_creator=True,
            is_contractor=True,
            is_admin=False
        )

        user = User.create_from_dict(user_dict)
        db_session.add(user)
        db_session.commit()

        count_after_insert = User.query.count()

        self.assertEqual(count_before_insert + 1, count_after_insert)

        user = User.query.filter_by(login='konbis').first()

        self.assertIsNotNone(user)
        self.assertEqual(user_dict['login'], user.login)
        self.assertEqual(user_dict['first_name'], user.first_name)
        self.assertEqual(user_dict['last_name'], user.last_name)
        self.assertEqual(user_dict['is_creator'], user.is_creator)
        self.assertEqual(user_dict['is_contractor'], user.is_contractor)
        self.assertEqual(user_dict['is_admin'], user.is_admin)

    def test_create_user_from_dict_invalid_type(self):
        count_before_insert = User.query.count()

        user_list = [
            'konbis',
            'Konrad',
            'Biś',
            True,
            True,
            False,
            'abcd'
        ]

        with self.assertRaises(TypeError):
            user = User.create_from_dict(user_list)
            db_session.add(user)
            db_session.commit()

        count_after_insert = User.query.count()

        user = User.query.filter_by(login='konbis').first()

        self.assertIsNone(user)
        self.assertEqual(count_before_insert, count_after_insert)

    def test_create_user_from_dict_invalid_data(self):
        count_before_insert = User.query.count()

        user_dict = dict(
            login='konbis',
            last_name='Biś',
            is_creator=True,
            is_contractor=True,
            is_admin=False
        )

        with self.assertRaises(ValidationError):
            user = User.create_from_dict(user_dict)
            db_session.add(user)
            db_session.commit()

        count_after_insert = User.query.count()

        user = User.query.filter_by(login='konbis').first()

        self.assertIsNone(user)
        self.assertEqual(count_before_insert, count_after_insert)

    def test_update_user(self):
        user = User.query.first()

        user_dict = dict(
            login='konbis',
            first_name='Konrad',
            last_name='Biś',
            is_creator=True,
            is_contractor=True,
            is_admin=False,
            junk='abcd'
        )

        response = self.client.put(
            '/user/' + str(user.id), data=json.dumps(user_dict))

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')

        user = User.query.filter_by(login='konbis').first()

        self.assertIsNotNone(user)

        data = json.loads(response.get_data())

        self.assertEqual(data, user.to_dict())

    def test_update_not_existing_user(self):
        user = User.query.first()

        user_dict = dict(
            login='konbis',
            first_name='Konrad',
            last_name='Biś',
            is_creator=True,
            is_contractor=True,
            is_admin=False,
            junk='abcd'
        )

        response = self.client.put(
            '/user/' + '123124134', data=json.dumps(user_dict))
        self.assertStatus(response, 404)

        response = self.client.put(
            '/user/' + 'abc', data=json.dumps(user_dict))
        self.assertStatus(response, 404)

        user = User.query.filter_by(login='konbis').first()
        self.assertIsNone(user)

    def test_update_user_duplicate_data(self):
        user_dict = dict(
            login='konbis',
            first_name='Konrad',
            last_name='Biś',
            is_creator=True,
            is_contractor=True,
            is_admin=False,
            password='secret',
            junk='abcd'
        )

        user = User.create_from_dict(user_dict)
        db_session.add(user)
        db_session.commit()

        user2 = User.query.first()

        response = self.client.put(
            '/user/' + str(user2.id), data=json.dumps(user_dict))

        print(response.get_data())

        self.assertStatus(response, 409)

        user2 = User.query.first()

        self.assertNotEqual(user2.login, user_dict['login'])
