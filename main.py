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

def process_special_file(file_path, filename, directory):
    """
    Processes the special file by repeatedly truncating and saving the remaining content.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    tokens = tokenize(content)
    iteration = 1

    while tokens:
        truncated_tokens, tokens = truncate_text(tokens)
        if not truncated_tokens:
            logging.info("No new data to process for " + filename)
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

            if is_special_file(filename):
                process_special_file(file_path, filename, directory)
            else:
                with open(file_path, 'r') as file:
                    content = file.read()
                
                truncated_tokens, _ = truncate_text(tokenize(content))

                if not truncated_tokens:
                    logging.info("No new data to process for " + filename)
                    continue

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
