import os
import re
import json
import nltk
import logging
from collections import defaultdict

# Download necessary NLTK data
nltk.download('punkt')

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def tokenize(text):
    return re.findall(r'\b\w+\b', text)

def truncate_text(tokens, max_length=511):
    logging.info(f"Truncating text with {len(tokens)} tokens")
    if len(tokens) <= max_length:
        return tokens, []
    truncated_tokens = tokens[:max_length]
    remaining_tokens = tokens[max_length:]
    logging.info(f"Truncated to {len(truncated_tokens)} tokens, {len(remaining_tokens)} tokens remaining")
    return truncated_tokens, remaining_tokens

def is_data_file(filename):
    return filename.endswith('_data.txt')

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def group_by_security_type(data):
    grouped_data = defaultdict(list)
    for entry in data:
        security_type = entry['securityType']
        grouped_data[security_type].append(entry)
    return grouped_data

def write_to_files(grouped_data, directory, base_filename):
    for security_type, entries in grouped_data.items():
        content = json.dumps(entries, indent=4)
        tokens = tokenize(content)
        chunk_number = 1
        while tokens:
            truncated_tokens, tokens = truncate_text(tokens)
            truncated_content = ' '.join(truncated_tokens)
            new_filename = f"{base_filename}_truncated_{security_type.replace(' ', '_').replace('.', '').lower()}_chunk_{chunk_number}.txt"
            new_file_path = os.path.join(directory, new_filename)
            with open(new_file_path, 'w') as file:
                file.write(truncated_content)
            logging.info(f"Processed and created truncated file: {new_filename}")
            chunk_number += 1

def process_file(file_path, filename, directory):
    logging.info(f"Starting to process file: {filename}")
    base_filename = filename.replace('_data.txt', '')
    json_data = read_json(file_path)

    if 'ytd' in json_data['pd']['marketshare']:
        data_to_group = json_data['pd']['marketshare']['ytd']['interDealerBrokers']
    else:  # For quarterly data
        data_to_group = json_data['pd']['marketshare']['quarterly']['interDealerBrokers']

    grouped_data = group_by_security_type(data_to_group)
    write_to_files(grouped_data, directory, base_filename)

def process_files(directory, file_extension='.txt'):
    logging.info(f"Processing files in directory: {directory}")
    for filename in os.listdir(directory):
        logging.info(f"Found file: {filename}")
        if '_truncated_' in filename or not is_data_file(filename):
            logging.info(f"Skipping file: {filename}")
            continue
        file_path = os.path.join(directory, filename)
        process_file(file_path, filename, directory)

directory = os.path.dirname(os.path.abspath(__file__))
process_files(directory)