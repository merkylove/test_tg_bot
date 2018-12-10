import ujson
import redis
import os

from constants import REDIS_COLLECTION_NAME


class RedisDAO(object):
    def __init__(self, client, collection_name):
        self.client = client
        self.collection_name = collection_name

    def get_users(self):
        return self.client.hscan(self.collection_name)[1]

    def get_user(self, user_id):
        result = self.client.hget(self.collection_name, user_id)
        if result is not None:
            return ujson.loads(result)

    def save_user(self, id, data):
        self.client.hset(self.collection_name, id, ujson.dumps(data))

    def delete_user(self, id):
        return self.client.hdel(self.collection_name, id)


def get_default_redis_dao_object():

    REDIS_HOST = os.environ['REDIS_HOST']
    REDIS_PORT = os.environ['REDIS_PORT']

    return RedisDAO(
        client=redis.Redis(host=REDIS_HOST, port=REDIS_PORT),
        collection_name=REDIS_COLLECTION_NAME
    )
