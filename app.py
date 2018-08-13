"""
Watchtower Web Server
"""
__author__ = 'Enis Simsar'

import tornado.ioloop
from tornado.options import options
import tornado.web

from decouple import config

from urls import url_patterns
from logging import handlers
import logging
from mongoengine import connect
import time

secret_key = 'PEO+{+RlTK[3~}TS-F%[9J/sIp>W7!r*]YV75GZV)e;Q8lAdNE{m@oWK.+u-&z*-p>~Xa!Z8j~{z,BVv.e0GChY{(1.KVForO#rQ'

app_settings = dict(
    xsrf_cookies=False,
    cookie_secret=secret_key,
    port=config("HOST_PORT")
)

log_file = "./logs/daily_" + time.strftime("%d-%m-%Y") + ".log"

daily_handler = handlers.TimedRotatingFileHandler(
    log_file,
    when='midnight',
    interval=1,
    backupCount=7
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s %(asctime)s file:%(filename)s func:%(funcName)s line:%(lineno)s] %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    handlers=[
        daily_handler,
        logging.StreamHandler()
    ],
)


class WatchtowerNewsApp(tornado.web.Application):
    def __init__(self):
        super(WatchtowerNewsApp, self).__init__(url_patterns, **app_settings, autoreload=True)


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
