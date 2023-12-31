from redis import Redis
from base_db import BaseDB
from base_db import DecimalEncoder
import json


class RedisDB (BaseDB):

    def __init__(self, file_name='instrument.json', threads=10, records=20):

        super().__init__(file_name, threads, records)

        self.json_data = json.dumps(
            self.json_data, cls=DecimalEncoder).encode()

        redis_host = 'instruments.<your own>.clustercfg.use1.cache.amazonaws.com'

        self.redis = Redis(host=redis_host, port=6379, decode_responses=True)

    def create_record(self, key):

        self.redis.set(key, self.json_data)

    def read_record(self, key):

        self.redis.get(key)


if __name__ == "__main__":

    RedisDB().execute()
