from datetime import datetime

from marshmallow_mongoengine import ModelSchema, fields
from mongoengine import Document, DateTimeField
from factory.mongoengine import MongoEngineFactory

__author__ = 'Enis Simsar'


class BaseDocument(Document):
    meta = {
        'abstract': True
    }

    # last updated timestamp
    updated_at = DateTimeField(default=datetime.now)

    # timestamp of when entry was created
    created_at = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(BaseDocument, self).save(*args, **kwargs)

    def to_dict(self):
        return self.schema().dump(self).data

    def schema(self):
        raise NotImplementedError


class BaseSchema(ModelSchema):
    class Meta:
        pass

    created_at = fields.Method(serialize="_created_at_serializer", deserialize="_created_at_deserializer")
    updated_at = fields.Method(serialize="_updated_at_serializer", deserialize="_updated_at_deserializer")

    @staticmethod
    def _created_at_serializer(obj):
        return obj.created_at.timestamp()

    @staticmethod
    def _updated_at_serializer(obj):
        return obj.updated_at.timestamp()


class BaseFactory(MongoEngineFactory):
    class Meta:
        pass
