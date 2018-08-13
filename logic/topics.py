import json
import logging

from mongoengine import DoesNotExist

from models.Topic import Topic

__author__ = 'Enis Simsar'


def get_topic(user_id, topic_id):
    logging.info("user_id: {0}, topic_id: {1}".format(user_id, topic_id))
    if type(topic_id) is not str:
        return {'error': 'topic_id must be string!'}

    try:
        topic = Topic.objects.get(id=topic_id, user_id=user_id)
    except DoesNotExist:
        return {}
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    if topic is None:
        return {}

    return topic.to_dict()


def get_topics(user_id):
    logging.info("user_id: {0}".format(user_id))
    try:
        topics = Topic.objects.filter(user_id=user_id)
    except DoesNotExist:
        return {}
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    if topics is None:
        return json.dumps([])

    topics_json = []

    for topic in topics:
        topics_json.append(topic.to_dict())

    return json.dumps(topics_json)


def post_topic(user_id, payload):
    logging.info("user_id: {0}, payload: {1}".format(user_id, payload))

    data = {
        'user_id': user_id,
        'name': payload['name'],
        'description': payload['description'],
        'keywords': payload['keywords'],
        'languages': payload['languages'],
        'is_active': payload['is_active']
    }
    try:
        topic = Topic(**data)
        topic.save()
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    return {
        'response': True,
        'topic_id': topic.to_dict()['id']
    }


def update_topic(user_id, topic_id, payload):
    logging.info("user_id: {0}, topic_id: {1}, payload: {2}".format(user_id, topic_id, payload))

    try:
        topic = Topic.objects.get(id=topic_id, user_id=user_id)
    except DoesNotExist:
        return {
            'message': 'topic not found',
            'response': False
        }
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    if 'name' in payload:
        topic.name = payload['name']

    if 'description' in payload:
        topic.description = payload['description']

    if 'keywords' in payload:
        topic.keywords = payload['keywords']

    if 'languages' in payload:
        topic.languages = payload['languages']

    if 'is_active' in payload:
        topic.is_active = payload['is_active']

    try:
        topic.save()
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    return {
        'response': True,
    }


def delete_topic(user_id, topic_id):
    logging.info("user_id: {0}, invitation_id: {1}".format(user_id, topic_id))
    if type(topic_id) is not str:
        return {'error': 'topic_id must be string!'}

    try:
        topic = Topic.objects.get(id=topic_id, user_id=user_id)
    except DoesNotExist:
        return {
            'message': 'topic not found',
            'response': False
        }
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    topic.delete()

    return {'response': True}


def post_topic_is_active(user_id, topic_id, is_active):
    logging.info("user_id: {0}, topic_id: {1}".format(user_id, topic_id))
    if type(topic_id) is not str:
        return {'error': 'topic_id must be string!'}

    try:
        topic = Topic.objects.get(id=topic_id, user_id=user_id)
    except DoesNotExist:
        return {
            'message': 'topic not found',
            'response': False
        }
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    topic.is_active = is_active

    topic.save()

    return {'response': True}
