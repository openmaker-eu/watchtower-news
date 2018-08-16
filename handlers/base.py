import tornado.web
import json
from logic.auth import get_user_with_api_token

__author__ = 'Enis Simsar'


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass


class JsonHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        self.response = None
        super().__init__(application, request, **kwargs)

    """Request handler where requests and responses speak JSON."""

    def prepare(self):
        if 'Content-Type' not in self.request.headers or self.request.headers['Content-Type'] != 'application/json':
            message = 'Please add "Content-Type: application/json" header.'
            self.send_error(400, message=message)  # Bad Request
        # Incorporate request JSON into arguments dictionary.
        if self.request.body:
            try:
                json_data = json.loads(self.request.body)
                self.request.arguments.update(json_data)
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message)  # Bad Request

        # Set up response dictionary.
        self.response = dict()

    def set_default_headers(self):
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
            auth_header = handler.request.headers.get('Authorization')
            if auth_header is None or not auth_header.startswith('Basic '):
                handler.set_status(401)
                handler.set_header('WWW-Authenticate', 'Basic realm=Restricted')  # noqa
                handler._transforms = []
                handler.finish()
                return False

            api_token = auth_header[6:]

            user = get_user_with_api_token(api_token)

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

