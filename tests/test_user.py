from models.User import UserFactory
from tests.base import BaseTestCase


class UserTestCase(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.user = UserFactory.create()
        self.user.save()

    def test_get_profile(self):
        url = '/api/user'
        response = self.fetch(url, api_token=self.user.api_token)
        self.assertEqual(response.code, 200)

    def test_refresh_token(self):
        url = '/api/user'
        response = self.fetch(url, api_token=self.user.api_token, method='POST', body="")
        self.assertEqual(response.code, 200)
