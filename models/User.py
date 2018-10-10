import hashlib
import random
import string
import uuid

from mongoengine import StringField

from models.Base import BaseDocument, BaseSchema, BaseFactory

__author__ = 'Enis Simsar'


# from http://www.pythoncentral.io/hashing-strings-with-python/
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


class User(BaseDocument):
    username = StringField(max_length=20, unique=True)
    password = StringField()
    api_token = StringField(max_length=40, min_length=20, default=''.join(
        [random.choice(string.ascii_letters + string.digits) for _ in range(40)]))
    meta = {'collection': 'users'}

    def schema(self):
        return UserSchema()


class UserSchema(BaseSchema):
    class Meta:
        model = User
        model_fields_kwargs = {'password': {'load_only': True}}


class UserFactory(BaseFactory):
    class Meta:
        model = User

    username = 'admin'
    password = hash_password('123456')
    api_token = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(40)])
