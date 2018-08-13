"""
Auth Handlers for Watchtower News
"""

__author__ = 'Enis Simsar'

from .base import JsonHandler, JsonAuthHandler
from logic.auth import register_user, get_user_profile, refresh_api_token, login_user


class AuthHandler(JsonHandler):
    def data_received(self, chunk):
        pass

    def post(self, register=False):
        if register:
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
        else:
            self.response = None
            if 'username' not in self.request.arguments:
                self.response = {'error': 'username is required!'}
            if 'password' not in self.request.arguments:
                self.response = {'error': 'password is required!'}

            if self.response is None:
                username = self.request.arguments['username']
                password = self.request.arguments['password']
                self.response = login_user(username, password)

        self.write_json()


class UserHandler(JsonAuthHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.response = get_user_profile(self.user_id)
        self.write_json()

    def post(self, refresh_token=False):
        if refresh_token:
            self.response = refresh_api_token(self.user_id)
            print(self.response)
            self.write_json()
