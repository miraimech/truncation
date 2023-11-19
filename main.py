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

def is_special_file(filename):
    """
    Checks if the filename is one of the special files.
    """
    return filename in ['marketshare_quarterly.txt', 'marketshare_yearly.txt']

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
                # This handles cases where the filename format is unexpected
                continue
    return os.path.join(directory, last_file) if last_file else None

def read_identifier(file_path):
    """
    Reads the identifier from the first line of the file.
    Adjust this function according to where the identifier is located in your file.
    """
    with open(file_path, 'r') as file:
        identifier = file.readline().strip()
    return identifier

def check_and_update_log(log_file, identifier):
    """
    Checks if the identifier is in the log file and updates the log if not.
    Returns True if the identifier is new, False otherwise.
    """
    if not os.path.exists(log_file):
        with open(log_file, 'w') as file:
            pass  # Create an empty log file

    with open(log_file, 'r+') as file:
        processed_ids = [line.strip() for line in file]
        if identifier in processed_ids:
            return False
        else:
            file.write(identifier + '\n')
            return True

def process_special_file(file_path, filename, directory, log_file):
    """
    Processes the special file by repeatedly truncating and saving the remaining content.
    Only processes new data based on the identifier.
    """
    identifier = read_identifier(file_path)
    if not check_and_update_log(log_file, identifier):
        logging.info(f"Data already processed for {filename}")
        return

    with open(file_path, 'r') as file:
        content = file.read()

    base_filename = filename.split('.')[0]
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

def process_files(directory, file_extension='.txt', log_file='processed_log.txt'):
    """
    Processes all files in the given directory with the specified file extension.
    """
    for filename in os.listdir(directory):
        if filename.endswith(file_extension) and not filename.endswith('_truncated.txt') and not is_special_file(filename):
            file_path = os.path.join(directory, filename)
            process_special_file(file_path, filename, directory, log_file)
        elif is_special_file(filename):
            file_path = os.path.join(directory, filename)
            process_special_file(file_path, filename, directory, log_file)

# Get the directory where the script is located
directory = os.path.dirname(os.path.abspath(__file__))

# Process the files in the script's directory
process_files(directory)
