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

    def __init__(self, file_name='instrument.json', threads=10, records=20):

        super().__init__(file_name=file_name, threads=threads, records=records)

        self.json_data = json.dumps(
            self.json_data, cls=DecimalEncoder).encode()

        # Cassandra Keyspaces configuration
        contact_points = ['cassandra.us-east-1.amazonaws.com']
        username = 'edxProjectUser-at-597782288487'
        password = 'xxiuSzxzaqyjWxB9X+DyAh0vee7In8fJVLqhZYJmlGs='
        keyspace_name = 'db_performance'

        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.load_verify_locations('sf-class2-root.crt')
        ssl_context.verify_mode = CERT_REQUIRED

        # auth_provider = PlainTextAuthProvider(
        #      username=self.username, password=self.password)
        # cluster = Cluster(contact_points=self.contact_points,
        #                        ssl_context=self.ssl_context, auth_provider=self.auth_provider, port=9142)
        # self.session = self.cluster.connect(keyspace_name)

        # use this if you want to use Boto to set the session parameters.
        boto_session = boto3.Session(region_name="us-east-1")
        credentials = boto_session.get_credentials()
        print(credentials)
        auth_provider = SigV4AuthProvider(
            region_name="us-east-1", boto_session=boto_session)

        cluster = Cluster(contact_points, ssl_context=ssl_context, auth_provider=auth_provider,
                          port=9142)
        self.session = cluster.connect(keyspace=keyspace_name)

    def create_record(self, key):

        query = SimpleStatement(
            f"INSERT INTO db_performance.instruments (key, data) VALUES ({key}, $${self.json_data}$$);", consistency_level=ConsistencyLevel.LOCAL_QUORUM)

        self.session.execute(query)

    def read_record(self, key):

        query = f"SELECT data FROM db_performance.instruments WHERE key = {key}"
        self.session.execute(query)


if __name__ == "__main__":

    CassandraDB().execute()
