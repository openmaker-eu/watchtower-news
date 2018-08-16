from decouple import config
from mongoengine import connect

connect(
    config('MONGODB_DB'),
    username=config('MONGODB_USER'),
    password=config('MONGODB_PASSWORD'),
    host=config('MONGODB_HOST'),
    port=config('MONGODB_PORT', cast=int),
    authentication_source='admin',
    connect=False
)

redis_url = 'redis://:{0}@db:6379/0'.format(config("REDIS_PASSWORD"))

REDIS_URL = redis_url
RQ_REDIS_URL = REDIS_URL
