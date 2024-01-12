import redis
import json

const_redis = {
    'catalogs_temp_db': {
        'host': 'localhost',
        'port': 6379,
        'db': 1,
        'decode_responses': True
    },
}


class RedisClient:
    def __init__(self, config):
        config = const_redis[config]
        self.redis_client = redis.StrictRedis(
            host=config['host'],
            port=config['port'],
            db=config['db'],
            decode_responses=config['decode_responses']
        )

    def clear_db(self):
        self.redis_client.flushdb()

    def delete_key(self, key):
        self.redis_client.delete(key)

    def set_key(self, key, value):
        self.redis_client.set(key, json.dumps(value))

    def get_key(self, key):
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)

