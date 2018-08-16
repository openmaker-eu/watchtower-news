from mongoengine import ReferenceField, CASCADE, StringField, URLField, DateTimeField, ListField, DictField

from models.Topic import Topic
from models.Base import BaseDocument, BaseSchema

__author__ = 'Enis Simsar'


class News(BaseDocument):
    topic_id = ReferenceField(Topic, reverse_delete_rule=CASCADE)
    title = StringField()
    full_text = StringField()
    summary = StringField()
    published_at = DateTimeField(null=True)
    image = URLField()
    url = URLField()
    source = StringField()
    domain = StringField()
    authors = ListField(StringField())
    language = StringField()
    mentions = ListField(DictField())
    short_links = ListField(URLField())
    meta = {'collection': 'news'}

    def schema(self):
        return NewsSchema()


class NewsSchema(BaseSchema):
    class Meta:
        model = News
