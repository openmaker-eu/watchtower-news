import os

import tornado.web
import tornado
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from settings import app_settings
from logic.auth import get_user_with_api_token

__author__ = 'Enis Simsar'


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass


class JinjaCustomFilter:
    @classmethod
    def debug(cls, text):
        print(str(text))
        return


class TemplateRendering:
    @classmethod
    def render_template(cls, template_name, variables=None):
        if variables is None:
            variables = {}
        env = Environment(loader=FileSystemLoader(app_settings['template_path']))
        jcf = JinjaCustomFilter()
        env.filters['debug'] = jcf.debug
        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)

        content = template.render(variables)
        return content


class StaticHandler(tornado.web.StaticFileHandler):
    def data_received(self, chunk):
        pass

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')


class JsonHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        self.response = None
        super().__init__(application, request, **kwargs)

    """Request handler where requests and responses speak JSON."""

    def prepare(self):
        if self.request.body and ('Content-Type' not in self.request.headers or self.request.headers['Content-Type'] != 'application/json'):
            message = 'Please add "Content-Type: application/json" header.'
            self.send_error(400, message=message)  # Bad Request
        # Incorporate request JSON into arguments dictionary.
        if self.request.body:
            try:
                json_data = tornado.escape.json_decode(self.request.body)
                self.request.arguments.update(json_data)
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message)  # Bad Request

        # Set up response dictionary.
        self.response = dict()

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type, api_key, authorization')
        self.set_header('Access-Control-Allow-Methods', "GET, POST, DELETE, PUT, PATCH, OPTIONS")
        self.set_header('Content-Type', 'application/json')

    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405:
                kwargs['message'] = 'Invalid HTTP method.'
            else:
                kwargs['message'] = 'Unknown error.'

        self.response = kwargs
        self.write_json()

    def write_json(self):
        output = self.response
        self.write(output)


def require_basic_auth(handler_class):
    def wrap_execute(handler_execute):
        def check_basic_auth(handler):
            auth_header = handler.request.headers.get('X-API-Key')

            user = get_user_with_api_token(auth_header)

            if user['response']:
                handler.user_id = user['id']
                return True

            handler.set_status(403)
            handler._transforms = []
            handler.finish()
            return False

        def _execute(self, transforms, *args, **kwargs):
            if self.user_id is None and not check_basic_auth(self):
                return False
            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)

    # return the modified class
    return handler_class


@require_basic_auth
class JsonAuthHandler(JsonHandler):
    def __init__(self, application, request, **kwargs):
        self.user_id = None
        super().__init__(application, request, **kwargs)

    def prepare(self):
        super(JsonAuthHandler, self).prepare()

    def get_user_id(self):
        return self.user_id

