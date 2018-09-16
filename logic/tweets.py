import logging
import json

from mongoengine import DoesNotExist

from models.Topic import Topic
from models.Tweet import Tweet

__author__ = 'Enis Simsar'


def get_tweet(user_id, tweet_id):
    logging.info("user_id: {0}, tweet_id: {1}".format(user_id, tweet_id))
    if type(tweet_id) is not str:
        return {'error': 'tweet_id must be string!'}

    try:
        tweet = Tweet.objects.get(id=tweet_id)
    except DoesNotExist:
        return {}
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    if tweet is None:
        return {}

    return tweet.to_dict()


def get_tweets(user_id, topic_id, skip, limit, order_by):
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
        tweets = Tweet.objects.filter(topic_id=topic.id).order_by(order_by)[skip: skip + limit]
    except DoesNotExist:
        return {}
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    if tweets is None:
        return json.dumps([])

    tweets_json = []

    for tweet in tweets:
        tweets_json.append(tweet.to_dict())

    return json.dumps(tweets_json)


def delete_tweet(user_id, tweet_id):
    logging.info("user_id: {0}, tweet_id: {1}".format(user_id, tweet_id))
    if type(tweet_id) is not str:
        return {'error': 'tweet_id must be string!'}

    try:
        tweet = Tweet.objects.get(id=tweet_id)
    except DoesNotExist:
        return {
            'message': 'tweet not found',
            'response': False
        }
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    tweet.delete()

    return {'response': True}
