sudo yum install git
sudo yum install python3

git clone https://github.com/dshilman/db_performance.git
sudo git pull

cd db_performance
python3 -m venv venv
source ./venv/bin/activate

sudo python3 -m pip install -r requirements.txt

cd code
sudo python3 -m dynamo_db
sudo python3 -m cassandra_db
sudo python3 -m redis_db
sudo python3 -m mongo_db