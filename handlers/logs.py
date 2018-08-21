"""
Logs Handlers for Watchtower News
"""
from handlers.base import JsonAuthHandler
from logic.logs import get_log, get_logs, delete_log

__author__ = 'Enis Simsar'


class LogHandler(JsonAuthHandler):
    def data_received(self, chunk):
        pass

    def get(self, log_file_name=None):
        if log_file_name:
            self.response = get_log(self.user_id, log_file_name)
        else:
            self.response = get_logs(self.user_id)

        self.write_json()

    def delete(self, log_file_name):
        self.response = delete_log(self.user_id, log_file_name)
        self.write_json()
