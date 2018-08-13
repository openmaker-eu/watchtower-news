"""
Topic Handlers for Watchtower News
"""
from handlers.base import JsonAuthHandler

__author__ = 'Enis Simsar'


class TopicHandler(JsonAuthHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        pass