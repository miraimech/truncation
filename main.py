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

def content_has_changed(file_path, last_truncated_file_path):
    """
    Checks if the content of the file has changed compared to the last truncated file.
    """
    if not os.path.exists(last_truncated_file_path):
        return True

    with open(file_path, 'r') as file:
        original_content = file.read()

    with open(last_truncated_file_path, 'r') as file:
        last_truncated_content = file.read()

    return original_content != last_truncated_content

def process_special_file(file_path, filename, directory):
    """
    Processes the special file by repeatedly truncating and saving the remaining content.
    """
    iteration = 1
    last_truncated_file_path = os.path.join(directory, f"{filename.rsplit('.', 1)[0]}_truncated_{iteration}.txt")

    if not content_has_changed(file_path, last_truncated_file_path):
        logging.info("No new data to process for " + filename)
        return

    with open(file_path, 'r') as file:
        content = file.read()

    tokens = tokenize(content)
    while tokens:
        truncated_tokens, tokens = truncate_text(tokens)

        if not truncated_tokens:
            break

        truncated_content = ' '.join(truncated_tokens)
        new_filename = f"{filename.rsplit('.', 1)[0]}_truncated_{iteration}.txt"
        new_file_path = os.path.join(directory, new_filename)

        with open(new_file_path, 'w') as file:
            file.write(truncated_content)
        logging.info(f"Processed and created truncated file: {new_filename}")

        iteration += 1

def process_files(directory, file_extension='.txt'):
    """
    Processes all files in the given directory with the specified file extension.
    Creates new files with truncated content or handles special files differently.
    """
    for filename in os.listdir(directory):
        if filename.endswith(file_extension) and not filename.endswith('_truncated.txt'):
            file_path = os.path.join(directory, filename)
            last_truncated_file_path = os.path.join(directory, filename.rsplit('.', 1)[0] + '_truncated.txt')

            if not content_has_changed(file_path, last_truncated_file_path):
                logging.info("No new data to process for " + filename)
                continue

            with open(file_path, 'r') as file:
                content = file.read()
                
                truncated_tokens, _ = truncate_text(tokenize(content))
                truncated_content = ' '.join(truncated_tokens)
                new_filename = filename.rsplit('.', 1)[0] + '_truncated.txt'
                new_file_path = os.path.join(directory, new_filename)

                with open(new_file_path, 'w') as file:
                    file.write(truncated_content)
                logging.info(f"Processed and created truncated file: {new_filename}")

# Get the directory where the script is located
directory = os.path.dirname(os.path.abspath(__file__))

# Process the files in the script's directory
process_files(directory)
