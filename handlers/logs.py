"""
Logs Handlers for Watchtower News
"""
from handlers.base import JsonAuthHandler
from logic.logs import get_log, get_logs, delete_log

__author__ = 'Enis Simsar'


class LogsHandler(JsonAuthHandler):
    def get(self):
        """Logs GET endpoint.
        ---
        tags:
            ['Log']
        description: Get Logs
        summary: Get Logs
        responses:
            200:
                description: Get Logs
                schema:
                    type: array
                    items:
                        type: string
        security:
            [apiKey: []]
        """
        self.response = get_logs(self.user_id)

        self.write_json()


class LogHandler(JsonAuthHandler):
    def get(self, log_file_name=None):
        """Log GET endpoint.
        ---
        tags:
            ['Log']
        description: Get A Log
        summary: Get A Log
        parameters:
            - in: path
              name: log_file_name
              schema:
                type: string
        responses:
            200:
                description: Get A Log
        security:
            [apiKey: []]
        """
        self.response = get_log(self.user_id, log_file_name)
        self.write_json()

    def delete(self, log_file_name=None):
        """Log DELETE endpoint.
        ---
        tags:
            ['Log']
        description: Delete A Log
        summary: Delete A Log
        parameters:
            - in: path
              name: log_file_name
              schema:
                type: string
        responses:
            200:
                description: Delete A Log
        security:
            [apiKey: []]
        """
        self.response = delete_log(self.user_id, log_file_name)
        self.write_json()
