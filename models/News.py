from mongoengine import ReferenceField, CASCADE

from models.Topic import Topic
from models.Base import BaseDocument, BaseSchema

__author__ = 'Enis Simsar'


class News(BaseDocument):
    topic_id = ReferenceField(Topic, dbref=True, reverse_delete_rule=CASCADE)
    meta = {'collection': 'news'}

    def schema(self):
        return NewsSchema()


class NewsSchema(BaseSchema):
    class Meta:
        model = News
