import os
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
                continue
    return os.path.join(directory, last_file) if last_file else None

def process_special_file(file_path, filename, directory):
    """
    Processes the special file by repeatedly truncating and saving the remaining content.
    Only processes new data based on content comparison.
    """
    base_filename = filename.split('.')[0]

    # Check if there is an existing truncated file. If so, compare its content.
    last_truncated_file = get_last_truncated_file(directory, base_filename)
    if last_truncated_file:
        with open(os.path.join(directory, last_truncated_file), 'r') as file:
            last_content = file.read()
            if content == last_content:
                logging.info(f"No new data to process for {filename}")
                return

    with open(file_path, 'r') as file:
        content = file.read()

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
    Processes all files in the given directory with the specified file extension.
    Avoids files that have already been truncated.
    """
    for filename in os.listdir(directory):
        if filename.endswith('_truncated.txt'):
            continue

        if filename.endswith(file_extension) and is_special_file(filename):
            file_path = os.path.join(directory, filename)
            process_special_file(file_path, filename, directory)

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    process_files(directory)
