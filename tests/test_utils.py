from tests.base import Base
from utils import query_from_dict
from models import User


class TestUtils(Base):

    def test_query_from_dict(self):
        user_dict = dict(
            first_name=dict(value='Daniel', operator='!='),
            id=dict(value=1, operator='>')
        )

        users = query_from_dict(User, user_dict)
        users2 = User.query.filter(User.first_name != 'Daniel', User.id>1).all()

        self.assertEqual(users, users2)

    def test_query_from_dict_invalid_type(self):
        data = [('first_name', 'Daniel', '!=')]

        with self.assertRaises(TypeError):
            users = query_from_dict(User, data)

        data = dict(
            first_name=('Daniel', '!=')
        )

        with self.assertRaises(TypeError):
            users = query_from_dict(User, data)

        with self.assertRaises(TypeError):
            users = query_from_dict(data, data)

    def test_query_from_dict_default_operator(self):
        user_dict = dict(
            first_name=dict(value='Daniel'),
        )

        users = query_from_dict(User, user_dict)
        users2 = User.query.filter(User.first_name == 'Daniel').all()

        self.assertEqual(users, users2)

    def test_query_from_dict_invalid_operator(self):
        user_dict = dict(
            first_name=dict(value='Daniel', operator='!!'),
        )

        users = query_from_dict(User, user_dict)
        users2 = User.query.filter(User.first_name == 'Daniel').all()

        self.assertEqual(users, users2)
