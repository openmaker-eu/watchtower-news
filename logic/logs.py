import os
import logging
import glob

__author__ = 'Enis Simsar'


def get_logs_names():
    log_file_names = glob.glob("./logs/*.log")

    log_file_names = [log_file_name.split("/")[-1] for log_file_name in log_file_names]

    return log_file_names


def get_log(user_id, log_file_name):
    logging.info("user_id: {0}, log_file_name: {1}".format(user_id, log_file_name))

    if type(log_file_name) is not str:
        return {'error': 'log_file_name must be string!'}

    if '.log' not in log_file_name:
        return {'error': 'log_file_name is invalid!'}

    log_file_names = get_logs_names()
    if log_file_name not in log_file_names:
        return {'error': 'log_file_name does not exist!'}

    try:
        log_file = "./logs/" + log_file_name
        file = open(log_file, "r")
        data = file.read()
        file.close()
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    return {'data': data}


def get_logs(user_id):
    logging.info("user_id: {0}".format(user_id))

    log_file_names = get_logs_names()

    return {'log_file_names': log_file_names}


def delete_log(user_id, log_file_name):
    logging.info("user_id: {0}, log_file_name: {1}".format(user_id, log_file_name))

    if type(log_file_name) is not str:
        return {'error': 'log_file_name must be string!'}

    if '.log' not in log_file_name:
        return {'error': 'log_file_name is invalid!'}

    log_file_names = get_logs_names()
    if log_file_name not in log_file_names:
        return {'error': 'log_file_name does not exist!'}

    log_file = "./logs/" + log_file_name

    if os.path.exists(log_file):
        os.remove(log_file)
        return {'response': True}
    else:
        return {
            'message': 'log not found',
            'response': False
        }
