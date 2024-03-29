"""
News Handlers for Watchtower News
"""
from handlers.base import JsonAuthHandler
from logic.news import get_news, get_single_news, delete_single_news

__author__ = 'Enis Simsar'


class NewsHandler(JsonAuthHandler):
    def get(self):
        """News GET endpoint.
        ---
        tags:
            ['News']
        description: Get News for logged User
        summary: Get News for logged User
        parameters:
            - in: query
              name: topic_id
              required: true
              schema:
                type: string
            - in: query
              name: skip
              schema:
                type: integer
            - in: query
              name: limit
              schema:
                type: integer
            - in: query
              name: order_field
              schema:
                type: string
                enum: [_id, topic_id, published_at]
            - in: query
              name: order_dir
              schema:
                type: string
                enum: [asc, desc]
        responses:
            200:
                description: Get News for logged User
                schema:
                    type: array
                    items: NewsSchema
        security:
            [apiKey: []]
        """
        self.response = None
        if not self.get_argument('topic_id', None):
            self.response = {'error': 'topic_id is required!'}

        if self.response is None:
            topic_id = self.get_argument('topic_id')
            skip = int(self.get_argument('skip', 0))
            limit = int(self.get_argument('limit', 50))
            order_field = self.get_argument('order_field', '_id')
            order_dir = self.get_argument('order_dir', 'asc')

            if order_dir == 'asc':
                order_by = '+' + order_field
            else:
                order_by = '-' + order_field

            self.response = get_news(self.user_id, topic_id, skip, limit, order_by)

        self.write_json()


class SingleNewsHandler(JsonAuthHandler):
    def get(self, news_id=None):
        """News GET endpoint.
        ---
        tags:
            ['News']
        description: Get A News
        summary: Get A News
        parameters:
            - in: path
              name: news_id
              schema:
                type: string
        responses:
            200:
                description: Get A News
                schema: NewsSchema
        security:
            [apiKey: []]
        """
        self.response = get_single_news(self.user_id, news_id)

        self.write_json()

    def delete(self, news_id=None):
        """News DELETE endpoint.
        ---
        tags:
            ['News']
        description: Delete A News
        summary: Delete A News
        parameters:
            - in: path
              name: news_id
              schema:
                type: string
        responses:
            200:
                description: Delete A News
        security:
            [apiKey: []]
        """
        self.response = delete_single_news(self.user_id, news_id)
        self.write_json()
