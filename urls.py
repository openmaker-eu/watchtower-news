"""
Endpoints
"""
from handlers.auth import AuthHandler, UserHandler
from handlers.invitations import InvitationHandler
from handlers.logs import LogHandler
from handlers.topics import TopicHandler
from handlers.news import NewsHandler
from handlers.main import MainHandler

__author__ = 'Enis Simsar'

url_patterns = [
    # MAIN - DOC
    (r"/", MainHandler),

    # AUTH
    (r"/auth", AuthHandler),
    (r"/auth/(register)$", AuthHandler),
    (r"/user", UserHandler),
    (r"/user/(refresh_token)$", UserHandler),

    # TOPIC
    (r"/topics", TopicHandler),
    (r"/topics/(.+$)", TopicHandler),

    # NEWS
    (r"/News", NewsHandler),

    # INVITATIONS
    (r'/invitations', InvitationHandler),
    (r'/invitations/(.+$)', InvitationHandler),

    # LOGS
    (r'/logs', LogHandler),
    (r'/logs/(.+$)', LogHandler),
]
