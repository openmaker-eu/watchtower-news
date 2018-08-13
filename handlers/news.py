"""
News Handlers for Watchtower News
"""
from handlers.base import JsonAuthHandler

__author__ = 'Enis Simsar'


class NewsHandler(JsonAuthHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        pass