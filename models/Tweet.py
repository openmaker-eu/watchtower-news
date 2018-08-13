from mongoengine import IntField, BooleanField

from models.Base import BaseDocument, BaseSchema

__author__ = 'Enis Simsar'


class Tweet(BaseDocument):
    tweetDBId = IntField()
    redis = BooleanField()
    meta = {'collection': 'tweets'}

    def schema(self):
        return TweetSchema()


class TweetSchema(BaseSchema):
    class Meta:
        model = Tweet
