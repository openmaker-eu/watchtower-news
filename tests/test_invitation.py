import json

from models.Invitation import InvitationFactory
from models.User import UserFactory
from tests.base import BaseTestCase


class InvitationTestCase(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.user = UserFactory.create()
        self.user.save()

    def test_get_invitation(self):
        invitation = InvitationFactory.create(user_id=self.user.id)
        url = '/api/invitation/{0}'.format(str(invitation.id))
        response = self.fetch(url, api_token=self.user.api_token)
        self.assertEqual(response.code, 200)
        self.assertTrue('id' in response.body)
        if 'id' in response.body:
            self.assertEqual(response.body['id'], str(invitation.id))

    def test_delete_invitation(self):
        topic = InvitationFactory.create(user_id=self.user.id)
        url = '/api/invitation/{0}'.format(str(topic.id))
        response = self.fetch(url, api_token=self.user.api_token, method='DELETE')
        self.assertEqual(response.code, 200)
        self.assertEqual({'response': True}, response.body)

    def test_put_invitation(self):
        topic = InvitationFactory.create(user_id=self.user.id)
        url = '/api/invitation/{0}'.format(str(topic.id))
        body = {
            'is_active': False
        }
        response = self.fetch(url, api_token=self.user.api_token, method='PUT', body=json.dumps(body))
        self.assertEqual(response.code, 200)
        self.assertEqual({'response': True}, response.body)

    def test_post_invitation(self):
        url = '/api/invitation'
        response = self.fetch(url, api_token=self.user.api_token, method='POST', body="")
        self.assertEqual(response.code, 200)

    def test_get_invitations(self):
        invitation_1 = InvitationFactory.create(user_id=self.user.id)
        invitation_2 = InvitationFactory.create(user_id=self.user.id)
        url = '/api/invitations'
        response = self.fetch(url, api_token=self.user.api_token)
        self.assertEqual(response.code, 200)
        self.assertTrue(type(response.body) is list)

        expected_topic_ids = [str(invitation_1.id), str(invitation_2.id)]
        self.assertEqual(expected_topic_ids, [topic['id'] for topic in response.body])
