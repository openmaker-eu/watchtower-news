import json

from models.Invitation import InvitationFactory
from models.User import UserFactory
from tests.base import BaseTestCase


class AuthTestCase(BaseTestCase):
    def test_register(self):
        invitation = InvitationFactory.create()
        invitation.save()
        body = {
            'username': 'admin',
            'password': '123456',
            'invitation_code': invitation.code
        }
        response = self.fetch('/api/auth', method='POST', body=json.dumps(body))
        self.assertEqual(response.code, 200)

    def test_login(self):
            user = UserFactory.create()
            user.save()
            url = '/api/auth?username={0}&password={1}'.format(user.username, '123456')
            response = self.fetch(url)
            self.assertEqual(response.code, 200)
            expected_result = {'response': True, 'api_token': user.api_token}
            self.assertDictEqual(expected_result, response.body)
