__author__ = ['Enis Simsar']

from utils.Connections import Connection
from models.Model import Model


class Topic(Model):
    __slots__ = ['topic_id', 'topic_name', 'topic_description', 'keywords', 'languages', 'creation_time', 'type',
                 'last_tweet_date', 'is_running' 'last_news_date', 'is_masked_location', 'news_count', 'tweet_count']

    @staticmethod
    def fields():
        return [
            'topic_id',
            'topic_name',
            'topic_description',
            'keywords',
            'languages',
            'creation_time',
            'last_tweet_date',
            'is_running',
            'last_news_date',
            'is_masked_location'
        ]

    @staticmethod
    def table_name():
        return "topics"

    @staticmethod
    def model_id_column():
        return "topic_id"

    @staticmethod
    def hidden_fields():
        pass

    # TODO: Change MongoDB calls
    def __getattribute__(self, item):
        if item in ['keywords', 'languages']:
            return object.__getattribute__(self, item).split(',')
        if item == 'news_count':
            return Connection.Instance().newsPoolDB[
                str(object.__getattribute__(self, self.model_id_column()))].find().count()
        if item == 'tweet_count':
            return Connection.Instance().db[
                str(object.__getattribute__(self, self.model_id_column()))].find().count()
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            return None

    def __init__(self, model):
        super().__init__(model)
