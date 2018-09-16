from marshmallow_mongoengine import fields
from mongoengine import ReferenceField, DateTimeField, DictField, CASCADE

from models.Topic import Topic
from models.Base import BaseDocument, BaseSchema

from decouple import config
from redis import Redis, ConnectionPool
from rq import Queue

from utils import link_parser

__author__ = 'Enis Simsar'

pool = ConnectionPool(host='db', port=6379, password=config("REDIS_PASSWORD"), db=0)
redis_conn = Redis(connection_pool=pool)
q = Queue(connection=redis_conn)  # no args implies the default queue


class Tweet(BaseDocument):
    topic_id = ReferenceField(Topic, reverse_delete_rule=CASCADE)
    entry = DictField(required=True)
    published_at = DateTimeField(required=True)
    meta = {
        'collection': 'tweets',
        'index_background': True,
        'auto_create_index': True,
        'indexes': [
            'topic_id',
            'published_at'
        ]
    }

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        if document.entry['entities']['urls']:
            data = {
                'user_id': document.entry['user']['id_str'],
                'tweet_id': document.entry['id_str'],
                'timestamp_ms': int(document.entry['timestamp_ms']),
                'language': document.entry['user']['lang'],
                'location': document.entry['user']['location'],
                'urls': [url['expanded_url'] for url in document.entry['entities']['urls'] if 'expanded_url' in url]
            }
            q.enqueue_call(func=link_parser.parse_links,
                           args=(document.topic_id, data),
                           at_front=True,
                           timeout=20)

    def schema(self):
        return TweetSchema()


class TweetSchema(BaseSchema):
    class Meta:
        model = Tweet

    published_at = fields.Method(serialize="_published_at_serializer", deserialize="_published_at_deserializer")

    @staticmethod
    def _published_at_serializer(obj):
        return obj.published_at.timestamp()
