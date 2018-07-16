"""
Endpoints
"""
__author__ = ['Enis Simsar', 'Kemal Berk Kocabagli']

import tornado.web

from settings import settings

from handlers.topics import TopicHandler
from handlers.news import NewsHandler
from handlers.main import MainHandler

url_patterns = [
    # MAIN - DOC
    (r"/", MainHandler),

    # TOPIC
    (r"/Topic", TopicHandler),

    # NEWS
    (r"/News", NewsHandler),
]
