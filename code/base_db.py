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
        self.json_data = self.get_instrument_json()

    def execute(self):

        start_time = time.time()

        create_threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(
                target=self.create_records, args=(i,))
            create_threads.append(thread)
            thread.start()

        for thread in create_threads:
            thread.join()

        read_threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.read_records, args=(i,))
            read_threads.append(thread)
            thread.start()

        for thread in read_threads:
            thread.join()

        self.print_stats()

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Execution time: {execution_time}")

    def get_instrument_json(self):

        try:
            with open(self.file_name, "r") as f:
                data = f.read()

            return json.loads(str(data), parse_float=Decimal)


        except FileNotFoundError:
            print(f"File not found: {self.file_name}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")


    def create_records(self, thread_id):

        for i in range(1, self.num_records + 1):
            key = int(thread_id * 100 + i)
            start_time = time.time()
            self.create_record(key)
            end_time = time.time()
            execution_time = end_time - start_time
            self.performance_data[key] = {'Create Time': execution_time}

    def create_record(self, key, data):
        pass


    def read_records(self, thread_id):

        for key in self.performance_data.keys():
            start_time = time.time()
            self.read_record(key)
            end_time = time.time()
            execution_time = end_time - start_time
            self.performance_data[key]['Read Time'] = execution_time


    def read_record(self, key):
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
