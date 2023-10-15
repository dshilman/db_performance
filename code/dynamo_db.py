import time
import boto3
from base_db import BaseDB

class DynamoDB (BaseDB):

    def __init__(self, file_name, threads, records):

        # AWS DynamoDB configuration
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table_name = 'Instruments'
        self.table = self.dynamodb.Table(self.table_name)
        super().__init__(file_name, threads, records)

    # Function to create records in DynamoDB
    def create_records(self, thread_id, instrument_json):

        for i in range(1, super().records):
            key = str(thread_id * 10 + i)
            item = {
                'Key': key,
                'Data': instrument_json
            }

            start_time = time.time()
            self.table.put_item(Item=item)
            end_time = time.time()
            execution_time = end_time - start_time
            super().performance_data[key] = {'Create Time': execution_time}

    # Function to read records from DynamoDB
    def read_records(self, thread_id):
        for key in super().performance_data.keys():
            start_time = time.time()
            response = self.table.get_item(Key={'Key': key})
            end_time = time.time()
            execution_time = end_time - start_time
            super().performance_data[key]['Read Time'] = execution_time

if __name__ == "__main__":

    file_name = 'instrument.json'
    DynamoDB(file_name=file_name, threads=2, records=2).execute()
