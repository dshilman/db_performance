import threading
import json
import pandas as pd
import statistics
from decimal import Decimal


class BaseDB:
    
    # Dictionary to store performance data
    performance_data = {}
        
    def __init__(self, file_name, threads, records):
        self.threads = threads
        self.records = records
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

        # Create a Pandas DataFrame from performance data
        df = pd.DataFrame.from_dict(self.performance_data, orient='index')

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

    def execute(self):

        instrument_json = self.get_instrument_json()
        # Number of threads
        num_threads = 2

        # Create and start the threads for record creation
        create_threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=self.create_records, args=(i, instrument_json))
            create_threads.append(thread)
            thread.start()

        # Wait for all create threads to finish
        for thread in create_threads:
            thread.join()

        # Create and start threads for reading records
        read_threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=self.read_records, args=(i,))
            read_threads.append(thread)
            thread.start()

        # Wait for all read threads to finish
        for thread in read_threads:
            thread.join()

        self.print_stats()


