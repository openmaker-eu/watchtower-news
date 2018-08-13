from mongoengine import CASCADE, ReferenceField, StringField, ListField, BooleanField

from models.User import User
from models.Base import BaseDocument, BaseSchema

__author__ = 'Enis Simsar'


class Topic(BaseDocument):
    user_id = ReferenceField(User, dbref=True, reverse_delete_rule=CASCADE)
    topic_name = StringField(max_length=20)
    topic_desc = StringField(max_length=400)
    keywords = ListField(StringField(), max_length=10)
    languages = ListField()
    is_active = BooleanField()

    meta = {'collection': 'topics'}

    def schema(self):
        return TopicSchema()


class TopicSchema(BaseSchema):
    class Meta:
        model = Topic

