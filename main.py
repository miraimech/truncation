import os
import sys
import re
import logging
import nltk

# Download necessary NLTK data
nltk.download('punkt')

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def tokenize(text):
    """
    Tokenizes the given text. This function considers words, numbers, and symbols as separate tokens.
    """
    return re.findall(r'\b\w+\b', text)

def truncate_text(tokens, max_length=511):
    """
    Truncate the list of tokens to the maximum length.
    """
    logging.info(f"Truncating text with {len(tokens)} tokens")

    if len(tokens) <= max_length:
        return tokens, []

    # Truncate tokens to the maximum length
    truncated_tokens = tokens[:max_length]
    remaining_tokens = tokens[max_length:]

    logging.info(f"Truncated to {len(truncated_tokens)} tokens, {len(remaining_tokens)} tokens remaining")

    return truncated_tokens, remaining_tokens


def is_data_file(filename):
    """
    Checks if the filename ends with '_data.txt'.
    """
    return filename.endswith('_data.txt')

def get_last_truncated_file(directory, base_filename):
    """
    Gets the last truncated file for the given base filename.
    """
    last_file = None
    highest_number = -1
    for fname in os.listdir(directory):
        if fname.startswith(base_filename) and fname.endswith(".txt") and "_truncated_" in fname:
            try:
                number = int(fname.split("_truncated_")[1].split(".")[0])
                if number > highest_number:
                    highest_number = number
                    last_file = fname
            except ValueError:
                continue
    return os.path.join(directory, last_file) if last_file else None

def process_file(file_path, filename, directory, file_counters):
    logging.info(f"Starting to process file: {filename}")

    base_filename = filename.replace('_data.txt', '')
    iteration = file_counters.get(base_filename, 1)

    with open(file_path, 'r') as file:
        content = file.read()

    tokens = tokenize(content)
    logging.info(f"Tokenized content into {len(tokens)} tokens")

    while tokens:
        truncated_tokens, tokens = truncate_text(tokens)
        logging.info(f"Truncated to {len(truncated_tokens)} tokens, {len(tokens)} tokens remaining")

        if not truncated_tokens:
            logging.info("No truncated tokens, breaking out of loop")
            break

        truncated_content = ' '.join(truncated_tokens)
        new_filename = f"{base_filename}_truncated_{iteration}.txt"
        new_file_path = os.path.join(directory, new_filename)

        with open(new_file_path, 'w') as file:
            file.write(truncated_content)
        logging.info(f"Processed and created truncated file: {new_filename}")

        iteration += 1

    # Update the counter for the base filename
    file_counters[base_filename] = iteration

def process_files(directory, file_extension='.txt'):
    """
    Processes all files in the given directory that end with '_data.txt'.
    """
    logging.info(f"Processing files in directory: {directory}")

    file_counters = {}
    for filename in os.listdir(directory):
        logging.info(f"Found file: {filename}")

        if '_truncated_' in filename:
            logging.info(f"Skipping already truncated file: {filename}")
            continue  # Skip already truncated files

        if is_data_file(filename):
            logging.info(f"Processing data file: {filename}")
            file_path = os.path.join(directory, filename)
            process_file(file_path, filename, directory, file_counters)
        else:
            logging.info(f"Skipping non-data file: {filename}")

# Get the directory where the script is located
directory = os.path.dirname(os.path.abspath(__file__))

# Process the files in the script's directory
process_files(directory)