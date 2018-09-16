import json

from models.Topic import TopicFactory, Topic
from models.User import UserFactory
from tests.base import BaseTestCase


class TopicTestCase(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.user = UserFactory.create()
        self.user.save()

    def test_get_topic(self):
        topic = TopicFactory.create(user_id=self.user.id)
        url = '/api/topic/{0}'.format(str(topic.id))
        response = self.fetch(url, api_token=self.user.api_token)
        self.assertEqual(response.code, 200)
        self.assertTrue('id' in response.body)
        if 'id' in response.body:
            self.assertEqual(response.body['id'], str(topic.id))

    def test_delete_topic(self):
        topic = TopicFactory.create(user_id=self.user.id)
        url = '/api/topic/{0}'.format(str(topic.id))
        response = self.fetch(url, api_token=self.user.api_token, method='DELETE')
        self.assertEqual(response.code, 200)
        self.assertEqual({'response': True}, response.body)

    def test_put_topic(self):
        topic = TopicFactory.create(user_id=self.user.id)
        url = '/api/topic/{0}'.format(str(topic.id))
        body = {
            'description': 'Lorem-ipsum',
            'is_active': False
        }
        response = self.fetch(url, api_token=self.user.api_token, method='PUT', body=json.dumps(body))
        self.assertEqual(response.code, 200)
        self.assertEqual({'response': True}, response.body)

    def test_post_topic(self):
        url = '/api/topic'
        body = {
            'name': 'Additional Topic',
            'description': 'Lorem Ipsum',
            'keywords': ['lorem', 'ipsum'],
            'languages': ['tr', 'en'],
            'is_active': False
        }
        response = self.fetch(url, api_token=self.user.api_token, method='POST', body=json.dumps(body))
        self.assertEqual(response.code, 200)

    def test_get_topics(self):
        topic_1 = TopicFactory.create(user_id=self.user.id)
        topic_2 = TopicFactory.create(user_id=self.user.id)
        url = '/api/topics'
        response = self.fetch(url, api_token=self.user.api_token)
        self.assertEqual(response.code, 200)
        self.assertTrue(type(response.body) is list)

        expected_topic_ids = [str(topic_1.id), str(topic_2.id)]
        self.assertEqual(expected_topic_ids, [topic['id'] for topic in response.body])
