"""
Watchtower Web Server
"""
__author__ = ['Enis Simsar', 'Kemal Berk Kocabagli']

import tornado.ioloop
from tornado.options import options
import tornado.web

from decouple import config

from settings import settings
from urls import url_patterns
from utils.general import Logger

logger = Logger('watchtower.' + __name__ + '.log')


class WatchtowerApp(tornado.web.Application):
    def __init__(self):
        super(WatchtowerApp, self).__init__(url_patterns, **settings, autoreload=True)


def main():
    options.parse_command_line()
    app = WatchtowerApp()
    try:
        app.listen(options.port)
        logger.log_and_print("Listening on port " + str(options.port))
    except SystemError as err:
        logger.log_and_print(err)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
