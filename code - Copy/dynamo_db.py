import threading
import time
import boto3
import json
import pandas as pd
import statistics

# AWS DynamoDB configuration
dynamodb = boto3.resource('dynamodb', region_name='your_region_name')
table_name = 'your_table_name'
table = dynamodb.Table(table_name)

# Dictionary to store performance data
performance_data = {}

def get_instrument_json(file_name):
    try:
        with open(file_name, 'r') as json_file:
            # Load the JSON data into a Python dictionary
            data = json.load(json_file)
            # print(data)  # You can now work with the 'data' dictionary

            return data

    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# Function to create records in DynamoDB
def create_records(thread_id, instrument_json):
    for i in range(1, 11):
        key = str(thread_id * 10 + i)
        start_time = time.time()
        item = {
            'Key': key,
            'Data': instrument_json
        }
        table.put_item(Item=item)
        end_time = time.time()
        execution_time = end_time - start_time
        performance_data[key] = {'Create Time': execution_time}

# Function to read records from DynamoDB
def read_records(thread_id):
    for key in performance_data.keys():
        start_time = time.time()
        response = table.get_item(Key={'Key': key})
        end_time = time.time()
        execution_time = end_time - start_time
        performance_data[key]['Read Time'] = execution_time

if __name__ == "__main__":

    file_name = 'yahoo.json'
    instrument_json = get_instrument_json(file_name)
    # Number of threads
    num_threads = 5

    # Create and start the threads for record creation
    create_threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=create_records, args=(i, instrument_json))
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
