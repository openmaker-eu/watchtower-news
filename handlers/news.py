"""
News Handlers for Watchtower News
"""

__author__ = ['Enis Simsar', 'Kemal Berk Kocabagli']

import tornado.web
import tornado.escape


class NewsHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        pass