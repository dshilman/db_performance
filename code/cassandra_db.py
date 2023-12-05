import json
import boto3
from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
from ssl import SSLContext, PROTOCOL_TLSv1_2, CERT_REQUIRED
from cassandra_sigv4.auth import SigV4AuthProvider
from cassandra.auth import PlainTextAuthProvider
from base_db import BaseDB
from base_db import DecimalEncoder


class CassandraDB(BaseDB):

    # Cassandra Keyspaces configuration
    contact_points = ['cassandra.us-east-1.amazonaws.com']
    keyspace_name = 'db_performance'

    ssl_context = SSLContext(PROTOCOL_TLSv1_2)
    ssl_context.load_verify_locations('sf-class2-root.crt')
    ssl_context.verify_mode = CERT_REQUIRED

    boto_session = boto3.Session(region_name="us-east-1")
    auth_provider = SigV4AuthProvider(session=boto_session)
    
    def __init__(self, file_name='instrument.json', threads=10, records=20):

        super().__init__(file_name=file_name, threads=threads, records=records)

        self.json_data = json.dumps(
            self.json_data, cls=DecimalEncoder).encode()

        cluster = Cluster(CassandraDB.contact_points, ssl_context=CassandraDB.ssl_context, auth_provider=CassandraDB.auth_provider,
                          port=9142)
        self.session = cluster.connect(keyspace=CassandraDB.keyspace_name)

    def create_record(self, key):

        query = SimpleStatement(
            f"INSERT INTO db_performance.instruments (key, data) VALUES ({key}, $${self.json_data}$$);", consistency_level=ConsistencyLevel.LOCAL_QUORUM)

        self.session.execute(query)

    def read_record(self, key):

        query = f"SELECT data FROM db_performance.instruments WHERE key = {key}"
        self.session.execute(query)


if __name__ == "__main__":

    CassandraDB().execute()
