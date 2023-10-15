import time
from redis import Redis
from base_db import BaseDB


class RedisDB (BaseDB):

    def __init__(self, file_name, threads, records):

        super().__init__(file_name, threads, records)

        # Redis configuration
        self.redis_host = 'instruments.otxqy9.ng.0001.use1.cache.amazonaws.com'
        self.redis_port = 6379  # Default Redis port
        # self.redis_db = 0  # Redis database number
        # self.redis_password = 'your_redis_password'

        self.r = Redis(host=self.redis_host, port=self.redis_port)

    # Function to create records in DynamoDB
    def create_records(self, thread_id, instrument_json):

        for i in range(1, self.num_records):
            key = int(thread_id * 100 + i)
            start_time = time.time()
            self.r.set(key, instrument_json)
            end_time = time.time()
            execution_time = end_time - start_time
            self.performance_data[key] = {'Create Time': execution_time}

    # Function to read records from Redis
    def read_records(self, thread_id):
     
        for key in self.performance_data.keys():
            start_time = time.time()
            value = r.get(key)
            end_time = time.time()
            execution_time = end_time - start_time
            self.performance_data[key]['Read Time'] = execution_time


if __name__ == "__main__":

    file_name = 'instrument.json'
    RedisDB(file_name=file_name, threads=10, records=20).execute()
