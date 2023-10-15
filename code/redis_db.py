import time
import redis from Redis
from base_db import BaseDB


class RedisDB (BaseDB):

    def __init__(self, file_name, threads, records):
        # Redis configuration
        self.redis_host = 'your_redis_endpoint'
        self.redis_port = 6379  # Default Redis port
        self.redis_db = 0  # Redis database number
        self.redis_password = 'your_redis_password'

        self.r = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db, password=self.redis_password)

 
        super().__init__(file_name, threads, records)


    # Function to create records in DynamoDB
    def create_records(self, thread_id, instrument_json):

        for i in range(1, 11):
            key = str(thread_id * 10 + i)
            start_time = time.time()
            self.r.set(key, f'Some data for key {key}')
            end_time = time.time()
            execution_time = end_time - start_time
            super().performance_data[key] = {'Create Time': execution_time}

    # Function to read records from Redis
    def read_records(self, thread_id):
     
        for key in super().performance_data.keys():
            start_time = time.time()
            value = r.get(key)
            end_time = time.time()
            execution_time = end_time - start_time
            super().performance_data[key]['Read Time'] = execution_time


if __name__ == "__main__":

    file_name = 'instrument.json'
    RedisDB(file_name=file_name, threads=10, records=20).execute()
