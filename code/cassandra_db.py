import time
import json
from decimal import Decimal
from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
from ssl import SSLContext, PROTOCOL_TLSv1_2, CERT_REQUIRED
from cassandra.auth import PlainTextAuthProvider
from base_db import BaseDB
from base_db import DecimalEncoder

class CassandraDB(BaseDB):

    def __init__(self, file_name, threads, records):

        super().__init__(file_name=file_name, threads=threads, records=records)

        # Cassandra Keyspaces configuration
        self.contact_points = ['cassandra.us-east-1.amazonaws.com']
        self.username = 'edxProjectUser-at-597782288487'
        self.password = 'xxiuSzxzaqyjWxB9X+DyAh0vee7In8fJVLqhZYJmlGs='
        self.keyspace_name = 'db_performance'

        # Create a cluster connection

        self.ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        self.ssl_context.load_verify_locations('sf-class2-root.crt')
        self.ssl_context.verify_mode = CERT_REQUIRED

        self.auth_provider = PlainTextAuthProvider(
            username=self.username, password=self.password)
        self.cluster = Cluster(contact_points=self.contact_points,
                               ssl_context=self.ssl_context, auth_provider=self.auth_provider, port=9142)
        self.session = self.cluster.connect(self.keyspace_name)


    # Function to create records in Keyspaces :)

    def create_records(self, thread_id, instrument_json):

        value = json.dumps(instrument_json, cls=DecimalEncoder).encode()

        for i in range(1, self.num_records):
            key = int(thread_id * 100 + i)
            query = SimpleStatement(
                f"INSERT INTO db_performance.instruments (key, data) VALUES ({key}, $${value}$$);", consistency_level=ConsistencyLevel.LOCAL_QUORUM)

            start_time = time.time()
            self.session.execute(query)
            end_time = time.time()
            execution_time = end_time - start_time

            self.performance_data[key] = {'Create Time': execution_time}

    # Function to read records from Keyspaces
    def read_records(self, thread_id):

        for key in self.performance_data.keys():
            start_time = time.time()
            query = f"SELECT data FROM db_performance.instruments WHERE key = {key}"
            self.session.execute(query)
            end_time = time.time()
            execution_time = end_time - start_time
            self.performance_data[key]['Read Time'] = execution_time


if __name__ == "__main__":

    file_name = 'instrument.json'
    CassandraDB(file_name=file_name, threads=10, records=20).execute()
