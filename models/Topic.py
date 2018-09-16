from mongoengine import CASCADE, ReferenceField, StringField, ListField, BooleanField, DateTimeField

from marshmallow_mongoengine import fields

from models.User import User
from models.Base import BaseDocument, BaseSchema, BaseFactory

__author__ = 'Enis Simsar'


class Topic(BaseDocument):
    user_id = ReferenceField(User, reverse_delete_rule=CASCADE)
    name = StringField(max_length=20, required=True)
    description = StringField(max_length=400, required=True)
    keywords = ListField(StringField(), max_length=10, required=True)
    languages = ListField(StringField(max_length=2), max_length=5, required=True)
    is_active = BooleanField(default=True)
    domain_filter = ListField(StringField(), default=[])
    last_tweet_at = DateTimeField(default=None)
    last_news_at = DateTimeField(default=None)

    meta = {
        'collection': 'topics',
        'index_background': True,
        'auto_create_index': True,
        'indexes': [
            'user_id'
        ]
    }

    def schema(self):
        return TopicSchema()


class TopicSchema(BaseSchema):
    class Meta:
        model = Topic

    last_tweet_at = fields.Method(serialize="_last_tweet_at_serializer", deserialize="_last_tweet_at_deserializer")
    last_news_at = fields.Method(serialize="_last_news_at_serializer", deserialize="_last_news_at_deserializer")

    @staticmethod
    def _last_tweet_at_serializer(obj):
        return obj.last_tweet_at.timestamp()

    @staticmethod
    def _last_news_at_serializer(obj):
        return obj.last_news_at.timestamp()


class TopicFactory(BaseFactory):
    class Meta:
        model = Topic

    name = 'Topic Name'
    description = 'Lorem Ipsum.'
    keywords = ['Lorem', 'ipsum']
    languages = ['tr', 'en']
    is_active = False
