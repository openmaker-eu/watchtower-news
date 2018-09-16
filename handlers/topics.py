"""
Topic Handlers for Watchtower News
"""
import logging

from handlers.base import JsonAuthHandler
from logic.topics import get_topic, get_topics, post_topic, post_topic_is_active, delete_topic, update_topic

__author__ = 'Enis Simsar'


class TopicsHandler(JsonAuthHandler):
    def get(self):
        """Topics GET endpoint.
        ---
        tags:
            ['Topic']
        description: Get Topics for logged User
        summary: Get Topics for logged User
        responses:
            200:
                description: Get Topics for logged User
                schema:
                    type: array
                    items: TopicSchema
        security:
            [apiKey: []]
        """
        self.response = get_topics(self.user_id)

        self.write_json()


class TopicPostHandler(JsonAuthHandler):
    def post(self):
        """Topic POST endpoint.
        ---
        tags:
            ['Topic']
        description: Create A Topic
        summary: Create A Topic
        parameters:
            - in: body
              name: body
              schema:
                type: object
                required:
                    - name
                    - description
                    - keywords
                    - languages
                properties:
                    name:
                        type: string
                    description:
                        type: string
                    keywords:
                        type: array
                        items:
                          type: string
                    languages:
                        type: array
                        items:
                          type: string
                    is_active:
                        type: boolean
        responses:
            200:
                description: Create A Topic
        security:
            [apiKey: []]
        """
        request = self.request.arguments

        def check_field(field_name):
            if field_name not in request:
                self.response = {'error': '{0} is required!'.format(field_name)}
                return False
            return True

        fields = ['name', 'description', 'keywords', 'languages']

        validate_field = True
        for field in fields:
            validate_field = check_field(field)
            if not validate_field:
                break

        if validate_field:
            payload = {
                'name': request['name'],
                'description': request['description'],
                'keywords': request['keywords'],
                'languages': request['languages'],
                'is_active': request['is_active'] if 'is_active' in request else True,
                'domain_filter': request['domain_filter'] if 'domain_filter' in request else []
            }

            self.response = post_topic(self.user_id, payload)

        self.write_json()


class TopicHandler(JsonAuthHandler):
    def get(self, topic_id=None):
        """Topic GET endpoint.
        ---
        tags:
            ['Topic']
        description: Get A Topic
        summary: Get A Topic
        parameters:
            - in: path
              name: topic_id
              schema:
                type: string
        responses:
            200:
                description: Get A Topic
                schema: TopicSchema
        security:
            [apiKey: []]
        """
        self.response = get_topic(self.user_id, topic_id)

        self.write_json()

    def put(self, topic_id=None):
        """Topic PUT endpoint.
        ---
        tags:
            ['Topic']
        description: Update A Topic
        summary: Update A Topic
        parameters:
            - in: path
              name: topic_id
              schema:
                type: string
            - in: body
              name: body
              schema:
                type: object
                properties:
                    name:
                        type: string
                    description:
                        type: string
                    keywords:
                        type: array
                        items:
                          type: string
                    languages:
                        type: array
                        items:
                          type: string
                    is_active:
                        type: boolean
        responses:
            200:
                description: Update A Topic
        security:
            [apiKey: []]
        """
        request = self.request.arguments
        payload = {}
        if 'name' in request:
            payload['name'] = request['name']

        if 'description' in request:
            payload['description'] = request['description']

        if 'keywords' in request:
            payload['keywords'] = request['keywords']

        if 'languages' in request:
            payload['languages'] = request['languages']

        if 'domain_filter' in request:
            payload['domain_filter'] = request['domain_filter']

        if 'is_active' in request:
            payload['is_active'] = request['is_active']

        self.response = update_topic(self.user_id, topic_id, payload)
        self.write_json()

    def delete(self, topic_id=None):
        """Topic DELETE endpoint.
        ---
        tags:
            ['Topic']
        description: Delete A Topic
        summary: Delete A Topic
        parameters:
            - in: path
              name: topic_id
              schema:
                type: string
        responses:
            200:
                description: Delete A Topic
        security:
            [apiKey: []]
        """
        self.response = delete_topic(self.user_id, topic_id)
        self.write_json()
