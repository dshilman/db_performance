import threading
import time
import redis from Redis
import pandas as pd
import statistics

# Redis configuration
redis_host = 'your_redis_endpoint'
redis_port = 6379  # Default Redis port
redis_db = 0  # Redis database number
redis_password = 'your_redis_password'

# Dictionary to store performance data
performance_data = {}

# Function to create records in Redis
def create_records(thread_id):
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
    for i in range(1, 11):
        key = str(thread_id * 10 + i)
        start_time = time.time()
        r.set(key, f'Some data for key {key}')
        end_time = time.time()
        execution_time = end_time - start_time
        performance_data[key] = {'Create Time': execution_time}

# Function to read records from Redis
def read_records(thread_id):
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
    for key in performance_data.keys():
        start_time = time.time()
        value = r.get(key)
        end_time = time.time()
        execution_time = end_time - start_time
        performance_data[key]['Read Time'] = execution_time

if __name__ == "__main__":
    # Number of threads
    num_threads = 5

    # Create and start the threads for record creation
    create_threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=create_records, args=(i,))
        create_threads.append(thread)
        thread.start()

    # Wait for all create threads to finish
    for thread in create_threads:
        thread.join()

    # Create and start threads for reading records
    read_threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=read_records, args=(i,))
        read_threads.append(thread)
        thread.start()

    # Wait for all read threads to finish
    for thread in read_threads:
        thread.join()

    # Create a Pandas DataFrame from performance data
    df = pd.DataFrame.from_dict(performance_data, orient='index')

    # Calculate mean and standard deviation for each column
    create_mean = statistics.mean(df['Create Time'])
    read_mean = statistics.mean(df['Read Time'])
    create_std = statistics.stdev(df['Create Time'])
    read_std = statistics.stdev(df['Read Time'])

    print("Performance Data:")
    print(df)
    print(f"Create Mean Time: {create_mean}")
    print(f"Read Mean Time: {read_mean}")
    print(f"Create Standard Deviation: {create_std}")
    print(f"Read Standard Deviation: {read_std}")
