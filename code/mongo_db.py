import time
import json
from pymongo import MongoClient
from base_db import BaseDB
from base_db import DecimalEncoder


class MongoDB(BaseDB):

    def __init__(self, file_name, threads, records):

        super().__init__(file_name=file_name, threads=threads, records=records)

        self.json_data = DecimalEncoder().encode(self.json_data)

        client = MongoClient('mongodb://dbperformance:dbperformance@docdb-2023-10-19-21-49-56.cluster-cvhepjn9lnot.us-east-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false')

        # Specify the database to be used
        db = client.dbperformance

        # Specify the collection to be used
        self.collection = db.dbperformance

    def create_record(self, key):

        data = {
            "key": key,
            "data": self.json_data
        }

        self.collection.insert_one(data)

    def read_record(self, key):

        self.collection.find_one({'key': key})


if __name__ == "__main__":

    file_name = 'instrument.json'
    MongoDB(file_name=file_name, threads=10, records=20).execute()
