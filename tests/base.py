import logging

from decouple import config
from mongoengine import connect
from tornado.testing import AsyncHTTPTestCase
from tornado.escape import json_decode

from models.User import User
from models.Invitation import Invitation
from models.News import News
from models.Topic import Topic
from models.Tweet import Tweet

from app import WatchtowerNewsApp


class BaseTestCase(AsyncHTTPTestCase):
    def get_app(self):
        app = WatchtowerNewsApp(testing=True)
        return app

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)
        logger = logging.getLogger()
        logger.disabled = True
        connect(
            config('MONGODB_TEST_DB'),
            username=config('MONGODB_USER'),
            password=config('MONGODB_PASSWORD'),
            host=config('MONGODB_HOST'),
            port=config('MONGODB_PORT', cast=int),
            authentication_source='admin',
            connect=False
        )

        User.drop_collection()
        Invitation.drop_collection()
        News.drop_collection()
        Topic.drop_collection()
        Tweet.drop_collection()

    def fetch(self, url, api_token=None, *r, **kw):
        headers = {
            'Content-Type': 'application/json'
        }
        if api_token:
            headers['X-API-Key'] = api_token
        resp = AsyncHTTPTestCase.fetch(self, url, headers=headers, *r, **kw)
        if resp.body:
            resp._body = json_decode(resp.body)
        return resp
