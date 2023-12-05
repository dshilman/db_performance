import boto3
from base_db import BaseDB


class DynamoDB (BaseDB):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    def __init__(self, file_name='instrument.json', threads=10, records=20):

        super().__init__(file_name, threads, records)

        table_name = 'Instruments'
        self.table = DynamoDB.dynamodb.Table(table_name)

    def create_record(self, key):

        item = {
            'key': key,
            'data': self.json_data
        }
        self.table.put_item(Item=item)

    def read_record(self, key):

        self.table.get_item(Key={'key': key})


if __name__ == "__main__":

    DynamoDB().execute()
