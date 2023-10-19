import threading
import json
import pandas as pd
import statistics
import time
from decimal import Decimal
from bson.decimal128 import Decimal128


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(str(obj))

        return json.JSONEncoder.default(self, obj)


class BaseDB:

    def __init__(self, file_name, threads, records):

        self.num_threads = threads
        self.num_records = records
        self.performance_data = {}
        self.file_name = file_name

    def get_instrument_json(self):
        try:
            with open(self.file_name, 'r') as json_file:
                # Load the JSON data into a Python dictionary
                data = json.load(json_file, parse_float=Decimal)
                # print(data)  # You can now work with the 'data' dictionary

                return data

        except FileNotFoundError:
            print(f"File not found: {self.file_name}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    # Function to create records in DynamoDB
    def create_records(self, thread_id, instrument_json):
        pass

    # Function to read records from DynamoDB
    def read_records(self, thread_id):
        pass

    def print_stats(self):

        if len(self.performance_data) > 0:
            # Create a Pandas DataFrame from performance data
            df = pd.DataFrame.from_dict(self.performance_data, orient='index')

            if not df.empty:
                df.sort_index(inplace=True)
                # Calculate mean and standard deviation for each column
                create_mean = statistics.mean(df['Create Time'])
                read_mean = statistics.mean(df['Read Time'])
                create_std = statistics.stdev(df['Create Time'])
                read_std = statistics.stdev(df['Read Time'])

                print("Performance Data:")
                print(df)
                print(f"Create Time mean: {create_mean}, std: {create_std}")
                print(f"Read Time mean: {read_mean}, std: {read_std}")

    def execute(self):

        start_time = time.time()

        instrument_json = self.get_instrument_json()

        # Create and start the threads for record creation
        create_threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(
                target=self.create_records, args=(i, instrument_json))
            create_threads.append(thread)
            thread.start()

        # Wait for all create threads to finish
        for thread in create_threads:
            thread.join()

        # Create and start threads for reading records
        read_threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.read_records, args=(i,))
            read_threads.append(thread)
            thread.start()

        # Wait for all read threads to finish
        for thread in read_threads:
            thread.join()
                
        self.print_stats()

        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"Execution time: {execution_time}")
