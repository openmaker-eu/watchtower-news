"""
Auth Handlers for Watchtower News
"""

__author__ = 'Enis Simsar'

from .base import JsonHandler, JsonAuthHandler
from logic.auth import register_user, get_user_profile, refresh_api_token, login_user


class AuthHandler(JsonHandler):
    def get(self):
        """Login endpoint.
        ---
        tags:
            ['Auth']
        description: Get API key
        summary: Get API key
        parameters:
            - in: query
              required: true
              name: username
              schema:
                type: string
            - in: query
              required: true
              name: password
              schema:
                type: string
        responses:
            200:
                description: Get API key for user.
        """
        self.response = None
        if not self.get_argument('username', None):
            self.response = {'error': 'username is required!'}
        if not self.get_argument('password', None):
            self.response = {'error': 'password is required!'}

        if self.response is None:
            username = self.get_argument('username', None)
            password = self.get_argument('password', None)
            self.response = login_user(username, password)

        self.write_json()

    def post(self):
        """Register endpoint.
        ---
        tags:
            ['Auth']
        description: Create A User
        summary: Create A User
        parameters:
            - in: body
              name: body
              schema:
                type: object
                required:
                  - username
                  - password
                  - invitation_code
                properties:
                    username:
                        type: string
                    password:
                        type: string
                    invitation_code:
                        type: string
                        min_length: 40
                        max_length: 40
        responses:
            200:
                description: Create A User
        """
        self.response = None
        if 'username' not in self.request.arguments:
            self.response = {'error': 'username is required!'}
        if 'password' not in self.request.arguments:
            self.response = {'error': 'password is required!'}
        if 'invitation_code' not in self.request.arguments:
            self.response = {'error': 'invitation_code is required!'}

        if self.response is None:
            username = self.request.arguments['username']
            password = self.request.arguments['password']
            invitation_code = self.request.arguments['invitation_code']
            self.response = register_user(invitation_code, username, password)

        self.write_json()


class UserHandler(JsonAuthHandler):
    def get(self):
        """User GET endpoint.
        ---
        tags:
            ['User']
        description: Get User Profile
        summary: Get User Profile
        responses:
            200:
                description: Get User Profile
                schema: UserSchema
        security:
            [apiKey: []]
        """
        self.response = get_user_profile(self.user_id)
        self.write_json()

    def post(self):
        """User POST endpoint.
        ---
        tags:
            ['User']
        description: Refresh User API Token
        summary: Refresh User API Token
        responses:
            200:
                description: Refresh User API Token
        security:
            [apiKey: []]
        """
        self.response = refresh_api_token(self.user_id)
        self.write_json()
