"""
Tweets Handlers for Watchtower News
"""
from handlers.base import JsonAuthHandler
from logic.tweets import get_tweet, get_tweets, delete_tweet

__author__ = 'Enis Simsar'


class TweetsHandler(JsonAuthHandler):
    def get(self):
        """Tweets GET endpoint.
        ---
        tags:
            ['Tweet']
        description: Get Tweets for logged User
        summary: Get Tweets for logged User
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
                description: Get Tweets for logged User
                schema:
                    type: array
                    items: TweetSchema
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

            self.response = get_tweets(self.user_id, topic_id, skip, limit, order_by)

        self.write_json()


class TweetHandler(JsonAuthHandler):
    def get(self, tweet_id=None):
        """Tweet GET endpoint.
        ---
        tags:
            ['Tweet']
        description: Get A Tweet
        summary: Get A Tweet
        parameters:
            - in: path
              name: tweet_id
              schema:
                type: string
        responses:
            200:
                description: Get A Tweet
                schema: TweetSchema
        security:
            [apiKey: []]
        """
        self.response = get_tweet(self.user_id, tweet_id)

        self.write_json()

    def delete(self, tweet_id=None):
        """Tweet DELETE endpoint.
        ---
        tags:
            ['Tweet']
        description: Delete A Tweet
        summary: Delete A Tweet
        parameters:
            - in: path
              name: tweet_id
              schema:
                type: string
        responses:
            200:
                description: Delete A Tweet
        security:
            [apiKey: []]
        """
        self.response = delete_tweet(self.user_id, tweet_id)
        self.write_json()
