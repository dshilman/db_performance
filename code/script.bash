sudo yum install git
git clone https://github.com/dshilman/db_performance.git
sudo git pull

sudo yum install python3

sudo python3 -m dynamo_db
sudo python3 -m cassandra_db
sudo python3 -m redis_db
sudo python3 -m mongo_db