from mongoengine import CASCADE, ReferenceField, StringField, ListField, BooleanField

from models.User import User
from models.Base import BaseDocument, BaseSchema

__author__ = 'Enis Simsar'


class Topic(BaseDocument):
    user_id = ReferenceField(User, reverse_delete_rule=CASCADE)
    name = StringField(max_length=20, required=True)
    description = StringField(max_length=400, required=True)
    keywords = ListField(StringField(), max_length=10, required=True)
    languages = ListField(StringField(max_length=2), max_length=5, required=True)
    is_active = BooleanField()

    meta = {'collection': 'topics'}

    def schema(self):
        return TopicSchema()


class TopicSchema(BaseSchema):
    class Meta:
        model = Topic

