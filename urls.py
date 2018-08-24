"""
Endpoints
"""
from handlers.auth import UserHandler, AuthHandler
from handlers.base import StaticHandler
from handlers.invitations import InvitationHandler, InvitationsHandler, InvitationPostHandler
from handlers.logs import LogHandler, LogsHandler
from handlers.swagger import SwaggerHandler
from handlers.topics import TopicHandler, TopicsHandler, TopicPostHandler
from handlers.news import NewsHandler

from settings import app_settings

__author__ = 'Enis Simsar'

url_patterns = [
    # ----- API ENDPOINTS ----- #

    # AUTH
    (r"/api/auth", AuthHandler),
    (r"/api/user", UserHandler),

    # TOPIC
    (r"/api/topic", TopicPostHandler),
    (r"/api/topic/(.*)$", TopicHandler),
    (r"/api/topics", TopicsHandler),

    # NEWS
    (r"/News", NewsHandler),

    # INVITATIONS
    (r"/api/invitation", InvitationPostHandler),
    (r"/api/invitation/(.*)$", InvitationHandler),
    (r"/api/invitations", InvitationsHandler),

    # LOGS
    (r'/api/logs', LogsHandler),
    (r'/api/log/(.*)$', LogHandler),


    # ----- UI ENDPOINTS ----- #

    (r'/', SwaggerHandler),

    (r"/static/(.*)", StaticHandler, {'path': app_settings['template_path']}),
]
