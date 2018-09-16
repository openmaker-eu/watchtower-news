import json

from models.Topic import TopicFactory
from models.News import NewsFactory
from models.User import UserFactory
from tests.base import BaseTestCase


class NewsTestCase(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.user = UserFactory.create()
        self.user.save()
        self.topic = TopicFactory.create(user_id=self.user.id)
        self.topic.save()

    def test_get_tweet(self):
        news = NewsFactory.create(topic_id=self.topic.id)
        url = '/api/single_news/{0}'.format(str(news.id))
        response = self.fetch(url, api_token=self.user.api_token)
        self.assertEqual(response.code, 200)
        self.assertTrue('id' in response.body)
        if 'id' in response.body:
            self.assertEqual(response.body['id'], str(news.id))

    def test_delete_tweet(self):
        news = NewsFactory.create(topic_id=self.topic.id)
        url = '/api/single_news/{0}'.format(str(news.id))
        response = self.fetch(url, api_token=self.user.api_token, method='DELETE')
        self.assertEqual(response.code, 200)
        self.assertEqual({'response': True}, response.body)

    def test_get_tweets(self):
        news_1 = NewsFactory.create(topic_id=self.topic.id)
        news_2 = NewsFactory.create(topic_id=self.topic.id)
        url = '/api/news?topic_id={0}'.format(str(self.topic.id))
        response = self.fetch(url, api_token=self.user.api_token)
        self.assertEqual(response.code, 200)
        self.assertTrue(type(response.body) is list)

        expected_topic_ids = [str(news_1.id), str(news_2.id)]
        self.assertEqual(expected_topic_ids, [topic['id'] for topic in response.body])
