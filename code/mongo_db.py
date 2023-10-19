import time
import json
from pymongo import MongoClient
from base_db import BaseDB
from base_db import DecimalEncoder


class MongoDB(BaseDB):

    def __init__(self, file_name, threads, records):

        super().__init__(file_name=file_name, threads=threads, records=records)

        # MongoDB Atlas configuration
        mongo_uri = 'your_mongodb_uri'
        database_name = 'your_database_name'
        collection_name = 'your_collection_name'

        client = MongoClient('mongodb://dbperformance:dbperformance@docdb-2023-10-19-21-49-56.cluster-cvhepjn9lnot.us-east-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false')

        # Specify the database to be used
        db = client.dbperformance

        # Specify the collection to be used
        self.collection = db.dbperformance

    # Function to create records in MongoDB

    def create_records(self, thread_id, instrument_json):

        for i in range(1, 11):
            key = int(thread_id * 100 + i)
            start_time = time.time()
            data = {
                    "key": key,
                    "data": DecimalEncoder().encode(instrument_json)
                   }

            self.collection.insert_one(data)
            end_time = time.time()
            execution_time = end_time - start_time
            self.performance_data[key] = {'Create Time': execution_time}

    # Function to read records from MongoDB

    def read_records(self, thread_id):

        for key in self.performance_data.keys():
            start_time = time.time()
            data = self.collection.find_one({'key': key})
            end_time = time.time()
            execution_time = end_time - start_time
            self. performance_data[key]['Read Time'] = execution_time


if __name__ == "__main__":

    file_name = 'instrument.json'
    MongoDB(file_name=file_name, threads=2, records=2).execute()
