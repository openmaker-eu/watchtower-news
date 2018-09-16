"""
Watchtower Web Server
"""

__author__ = 'Enis Simsar'

import json

from models.Invitation import InvitationSchema
from models.News import NewsSchema
from models.Topic import TopicSchema
from models.Tweet import TweetSchema
from models.User import UserSchema

import tornado.ioloop
from tornado.options import options
import tornado.web

from decouple import config
from settings import app_settings

from urls import url_patterns
from logging import handlers
import logging
from mongoengine import connect
import time
import os

from apispec import APISpec
from apispec.ext.tornado import TornadoPlugin
from apispec.ext.marshmallow import MarshmallowPlugin

os.makedirs('./logs', exist_ok=True)

log_file = "./logs/daily_" + time.strftime("%d-%m-%Y") + ".log"

daily_handler = handlers.TimedRotatingFileHandler(
    log_file,
    when='midnight',
    interval=1,
    backupCount=7
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s %(asctime)s %(pathname)s@%(funcName)s:%(lineno)s] %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    handlers=[
        daily_handler,
        logging.StreamHandler()
    ],
)

spec = APISpec(
    title='WatchTower News API',
    version='1.0.0',
    openapi_version='2.0',
    plugins=(
        TornadoPlugin(),
        MarshmallowPlugin(),
    ),
    info=dict(
        description='WatchTower News API'
    ),
    securityDefinitions=dict(
        apiKey={
            'type': 'apiKey',
            'name': 'X-API-Key',
            'in': 'header',
            'description': 'API Key for Authorization'
        }
    ),
    options={
        'consumes': ['application/json'],
        'produces': ['application/json']
    }
)

spec.definition('User', schema=UserSchema)
spec.definition('Topic', schema=TopicSchema)
spec.definition('Invitation', schema=InvitationSchema)
spec.definition('News', schema=NewsSchema)
spec.definition('Tweet', schema=TweetSchema)

for url_path in url_patterns:
    if 'api' in url_path[0]:
        spec.add_path(urlspec=url_path)
    continue

with open('./static/data.json', 'w') as outfile:
    json.dump(spec.to_dict(), outfile)


class WatchtowerNewsApp(tornado.web.Application):
    def __init__(self, testing=False):
        super(WatchtowerNewsApp, self).__init__(url_patterns, **app_settings, autoreload=not testing)


def main():
    options.parse_command_line()

    logging.getLogger('tornado.access').disabled = True

    app = WatchtowerNewsApp()
    app.listen(app_settings["port"])

    connect(
        config('MONGODB_DB'),
        username=config('MONGODB_USER'),
        password=config('MONGODB_PASSWORD'),
        host=config('MONGODB_HOST'),
        port=config('MONGODB_PORT', cast=int),
        authentication_source='admin',
        connect=False
    )

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
