from tests.base import Base
from tests.utils import is_json
import models



class TestUser(Base):

    def test_can_get_user(self):
        user = models.User.query.first()
        response = self.client.get('/user/' + str(user.id))

        self.assertStatus(response, 200)
        self.assertTrue(is_json(response.get_data()), 'Response is not json')
