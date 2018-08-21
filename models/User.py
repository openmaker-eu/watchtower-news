import random
import string

from mongoengine import StringField, ListField, ObjectIdField

from models.Base import BaseDocument, BaseSchema

__author__ = 'Enis Simsar'


class User(BaseDocument):
    username = StringField(max_length=20, unique=True)
    password = StringField()
    api_token = StringField(max_length=40, default=''.join(
        [random.choice(string.ascii_letters + string.digits) for _ in range(40)]))
    meta = {'collection': 'users'}

    def schema(self):
        return UserSchema()


class UserSchema(BaseSchema):
    class Meta:
        model = User
        model_fields_kwargs = {'password': {'load_only': True}}
