"""
Topic Handlers for Watchtower News
"""
from handlers.base import JsonAuthHandler
from logic.topics import get_topic, get_topics, post_topic, post_topic_is_active, delete_topic, update_topic

__author__ = 'Enis Simsar'


class TopicHandler(JsonAuthHandler):
    def data_received(self, chunk):
        pass

    def get(self, topic_id=None):
        if topic_id:
            self.response = get_topic(self.user_id, topic_id)
        else:
            self.response = get_topics(self.user_id)

        self.write_json()

    def post(self, topic_id=None):
        request = self.request.arguments
        if topic_id:
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
        else:
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

    def put(self, topic_id):
        if 'is_active' not in self.request.arguments:
            self.response = {'error': 'is_active is required!'}
            self.write_json()
            return

        is_active = self.request.arguments['is_active']
        self.response = post_topic_is_active(self.user_id, topic_id, is_active)
        self.write_json()

    def delete(self, topic_id):
        self.response = delete_topic(self.user_id, topic_id)
        self.write_json()
