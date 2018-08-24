"""
Invitation Handlers for Watchtower News
"""

from handlers.base import JsonAuthHandler
from logic.invitation import get_invitation, get_invitations, post_invitation_is_active, delete_invitation, \
    post_invitation

__author__ = 'Enis Simsar'


class InvitationsHandler(JsonAuthHandler):
    def get(self):
        """Invitations GET endpoint.
        ---
        tags:
            ['Invitation']
        description: Get Invitations for logged User
        summary: Get Invitations for logged User
        responses:
            200:
                description: Get Invitations for logged User
                schema:
                    type: array
                    items: InvitationSchema
        security:
            [apiKey: []]
        """
        self.response = get_invitations(self.user_id)

        self.write_json()


class InvitationPostHandler(JsonAuthHandler):
    def post(self):
        """Invitation POST endpoint.
        ---
        tags:
            ['Invitation']
        description: Create A Invitation
        summary: Create A Invitation
        responses:
            200:
                description: Create A Invitation
        security:
            [apiKey: []]
        """
        self.response = post_invitation(self.user_id)
        self.write_json()


class InvitationHandler(JsonAuthHandler):
    def get(self, invitation_id=None):
        """Invitation GET endpoint.
        ---
        tags:
            ['Invitation']
        description: Get A Invitation
        summary: Get A Invitation
        parameters:
            - in: path
              name: invitation_id
              schema:
                type: string
        responses:
            200:
                description: Get A Invitation
                schema: InvitationSchema
        security:
            [apiKey: []]
        """
        self.response = get_invitation(self.user_id, invitation_id)
        self.write_json()

    def put(self, invitation_id=None):
        """Invitation PUT endpoint.
        ---
        tags:
            ['Invitation']
        description: Update A Invitation
        summary: Update A Invitation
        parameters:
            - in: path
              name: invitation_id
              schema:
                type: string
            - in: body
              name: body
              schema:
                type: object
                required:
                    - is_active
                properties:
                    is_active:
                        type: boolean
        responses:
            200:
                description: Update A Invitation
        security:
            [apiKey: []]
        """
        if 'is_active' not in self.request.arguments:
            self.response = {'error': 'is_active is required!'}
            self.write_json()
            return

        is_active = self.request.arguments['is_active']
        self.response = post_invitation_is_active(self.user_id, invitation_id, is_active)
        self.write_json()

    def delete(self, invitation_id=None):
        """Invitation DELETE endpoint.
        ---
        tags:
            ['Invitation']
        description: Delete A Invitation
        summary: Delete A Invitation
        parameters:
            - in: path
              name: invitation_id
              schema:
                type: string
        responses:
            200:
                description: Delete A Invitation
        security:
            [apiKey: []]
        """
        self.response = delete_invitation(self.user_id, invitation_id)
        self.write_json()
