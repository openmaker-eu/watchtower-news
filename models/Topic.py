from mongoengine import CASCADE, ReferenceField, StringField, ListField, BooleanField, DateTimeField

from marshmallow_mongoengine import fields

from models.User import User
from models.Base import BaseDocument, BaseSchema

__author__ = 'Enis Simsar'


class Topic(BaseDocument):
    user_id = ReferenceField(User, reverse_delete_rule=CASCADE)
    name = StringField(max_length=20, required=True)
    description = StringField(max_length=400, required=True)
    keywords = ListField(StringField(), max_length=10, required=True)
    languages = ListField(StringField(max_length=2), max_length=5, required=True)
    is_active = BooleanField(default=True)
    last_tweet_at = DateTimeField(default=None)
    last_news_at = DateTimeField(default=None)

    meta = {'collection': 'topics'}

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
