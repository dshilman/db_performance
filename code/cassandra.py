import time
import json
from cassandra.cluster import Cluster
from ssl import SSLContext, PROTOCOL_TLSv1_2 , CERT_REQUIRED
from cassandra.auth import PlainTextAuthProvider
from base_db import BaseDB

class CassandraDB(BaseDB):

    def __init__(self):

        # Cassandra Keyspaces configuration
        self.contact_points = ['cassandra.us-east-1.amazonaws.com']
        self.username = 'edxProjectUser-at-597782288487'
        self.password = 'xxiuSzxzaqyjWxB9X+DyAh0vee7In8fJVLqhZYJmlGs='
        self.keyspace_name = 'db_performance'

        # Create a cluster connection
        self.auth_provider = PlainTextAuthProvider(username=self.username, password=self.password)
        self.cluster = Cluster(contact_points=self.contact_points, auth_provider=self.auth_provider)
        self.session = self.cluster.connect(self.keyspace_name)

        super().__init__()


    # Function to create records in Keyspaces
    def create_records(self, thread_id, instrument_json):

        for i in range(1, 11):
            key = str(thread_id * 10 + i)
            start_time = time.time()
            value = json.dumps(instrument_json)
            query = f"INSERT INTO instruments (key, data) VALUES ({key}, {value}')"
            self.session.execute(query)
            end_time = time.time()
            execution_time = end_time - start_time

            super().performance_data[key] = {'Create Time': execution_time}

    # Function to read records from Keyspaces
    def read_records(self, thread_id):

        for key in super().performance_data.keys():
            start_time = time.time()
            query = f"SELECT data FROM your_table_name WHERE key = {key}"
            self.session.execute(query)
            end_time = time.time()
            execution_time = end_time - start_time
            super().performance_data[key]['Read Time'] = execution_time

if __name__ == "__main__":

    file_name = 'instrument.json'
    CassandraDB().execute(file_name)