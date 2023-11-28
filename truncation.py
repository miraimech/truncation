import json
import os
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_truncated(directory, base_filename, truncated_data, truncated_number):
    new_filename = f"{base_filename}_truncated_{truncated_number}.txt"
    new_file_path = os.path.join(directory, new_filename)
    with open(new_file_path, 'w') as file:
        file.write(json.dumps(truncated_data, indent=4))
    logging.info(f"Processed and created file: {new_filename}")

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def process_file(file_path, filename, directory):
    logging.info(f"Starting to process file: {filename}")
    base_filename = filename.replace('_data.txt', '')
    json_data = read_json(file_path)

    flattened_data = flatten_json(json_data)
    keys = sorted(flattened_data.keys())

    current_truncated = []
    truncated_number = 1

    for key in keys:
        current_truncated.append({key: flattened_data[key]})

        # Check if current_truncated will exceed character limit, if so, start a new truncated
        if len(json.dumps(current_truncated, indent=4)) > 511:
            write_truncated(directory, base_filename, current_truncated, truncated_number)
            current_truncated = [{key: flattened_data[key]}]
            truncated_number += 1

    if current_truncated:
        write_truncated(directory, base_filename, current_truncated, truncated_number)

def process_files(directory, file_extension='.txt'):
    logging.info(f"Processing files in directory: {directory}")
    for filename in os.listdir(directory):
        logging.info(f"Found file: {filename}")
        if '_truncated_' in filename or not filename.endswith(file_extension):
            logging.info(f"Skipping file: {filename}")
            continue
        file_path = os.path.join(directory, filename)
        process_file(file_path, filename, directory)

directory = os.path.dirname(os.path.abspath(__file__))
process_files(directory)