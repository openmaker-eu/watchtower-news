import logging
import json

from mongoengine import DoesNotExist

from models.Topic import Topic
from models.News import News

__author__ = 'Enis Simsar'


def get_single_news(user_id, news_id):
    logging.info("user_id: {0}, news_id: {1}".format(user_id, news_id))
    if type(news_id) is not str:
        return {'error': 'news_id must be string!'}

    try:
        single_news = News.objects.get(id=news_id)
    except DoesNotExist:
        return {}
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    if single_news is None:
        return {}

    return single_news.to_dict()


def get_news(user_id, topic_id, skip, limit, order_by):
    logging.info(
        "user_id: {0}, topic_id: {1}, skip: {2}, limit: {3}, order_by: {4}".format(user_id, topic_id, skip, limit,
                                                                                   order_by))

    try:
        topic = Topic.objects.get(id=topic_id, user_id=user_id)
    except DoesNotExist:
        return []
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    try:
        news = News.objects.filter(topic_id=topic.id).order_by(order_by)[skip: skip + limit]
    except DoesNotExist:
        return {}
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    if news is None:
        return json.dumps([])

    news_json = []

    for single_news in news:
        news_json.append(single_news.to_dict())

    return json.dumps(news_json)


def delete_single_news(user_id, news_id):
    logging.info("user_id: {0}, news_id: {1}".format(user_id, news_id))
    if type(news_id) is not str:
        return {'error': 'news_id must be string!'}

    try:
        single_news = News.objects.get(id=news_id)
    except DoesNotExist:
        return {
            'message': 'news not found',
            'response': False
        }
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    single_news.delete()

    return {'response': True}
