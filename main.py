import os
import sys
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def tokenize(text):
    """
    Tokenizes the given text. This function considers words, numbers, and symbols as separate tokens.
    """
    return text.split()

def truncate_text(tokens, max_length=511):
    """
    Truncate the list of tokens to the maximum length.
    """
    return tokens[:max_length], tokens[max_length:]

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

def process_file(file_path, filename, directory):
    """
    Processes the file by repeatedly truncating and saving the remaining content.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    base_filename = filename.replace('_data.txt', '')

    last_truncated_file = get_last_truncated_file(directory, base_filename)
    if last_truncated_file:
        with open(os.path.join(directory, last_truncated_file), 'r') as file:
            last_content = file.read()
            if content == last_content:
                logging.info(f"No new data to process for {filename}")
                return

    tokens = tokenize(content)
    iteration = 1
    while tokens:
        truncated_tokens, tokens = truncate_text(tokens)
        if not truncated_tokens:
            break

        truncated_content = ' '.join(truncated_tokens)
        new_filename = f"{base_filename}_truncated_{iteration}.txt"
        new_file_path = os.path.join(directory, new_filename)

        with open(new_file_path, 'w') as file:
            file.write(truncated_content)
        logging.info(f"Processed and created truncated file: {new_filename}")

        iteration += 1

def process_files(directory, file_extension='.txt'):
    """
    Processes all files in the given directory that end with '_data.txt'.
    """
    for filename in os.listdir(directory):
        if '_truncated_' in filename:
            continue  # Skip already truncated files

        if is_data_file(filename):
            file_path = os.path.join(directory, filename)
            process_file(file_path, filename, directory)

# Get the directory where the script is located
directory = os.path.dirname(os.path.abspath(__file__))

# Process the files in the script's directory
process_files(directory)
