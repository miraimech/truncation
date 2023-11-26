import json
import os
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_chunk(directory, base_filename, key_value, chunk_data, chunk_number):
    new_filename = f"{base_filename}_{key_value.replace(' ', '_').lower()}_chunk_{chunk_number}.txt"
    new_file_path = os.path.join(directory, new_filename)
    with open(new_file_path, 'w') as file:
        file.write(json.dumps(chunk_data, indent=4))
    logging.info(f"Processed and created file: {new_filename}")

def process_file(file_path, filename, directory):
    logging.info(f"Starting to process file: {filename}")
    base_filename = filename.replace('_data.txt', '')
    json_data = read_json(file_path)

    marketshare_data = json_data['pd']['marketshare']
    data_to_group = marketshare_data.get('ytd', marketshare_data.get('quarterly', {})).get('interDealerBrokers', [])

    current_key_value = None
    current_chunk = []
    chunk_number = 1

    for entry in data_to_group:
        if entry:  # Ensure entry is not empty
            first_key = next(iter(entry))
            key_value = entry[first_key]

            if key_value != current_key_value:
                if current_chunk:
                    write_chunk(directory, base_filename, current_key_value, current_chunk, chunk_number)
                current_key_value = key_value
                current_chunk = [entry]
                chunk_number = 1
            else:
                # Check if current_chunk will exceed character limit, if so, start a new chunk
                if len(json.dumps(current_chunk + [entry], indent=4)) > 511:
                    write_chunk(directory, base_filename, key_value, current_chunk, chunk_number)
                    current_chunk = [entry]
                    chunk_number += 1
                else:
                    current_chunk.append(entry)

    if current_chunk:
        write_chunk(directory, base_filename, current_key_value, current_chunk, chunk_number)

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