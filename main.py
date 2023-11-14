import os
import sys

def tokenize(text):
    """
    Tokenizes the given text. This function considers words, numbers, and symbols as separate tokens.
    """
    return text.split()

def truncate_text(tokens, max_length=511):
    """
    Truncate the list of tokens to the maximum length.
    """
    return tokens[:max_length]

def process_files(directory, file_extension='.txt'):
    """
    Processes all files in the given directory with the specified file extension.
    Creates new files with truncated content.
    """
    for filename in os.listdir(directory):
        if filename.endswith(file_extension):
            file_path = os.path.join(directory, filename)

            with open(file_path, 'r') as file:
                content = file.read()
            
            tokens = tokenize(content)
            truncated_tokens = truncate_text(tokens)
            truncated_content = ' '.join(truncated_tokens)

            # Creating a new filename for the truncated file
            new_filename = filename.rsplit('.', 1)[0] + '_truncated.txt'
            new_file_path = os.path.join(directory, new_filename)

            with open(new_file_path, 'w') as file:
                file.write(truncated_content)
            print(f"Processed and created truncated file: {new_filename}")

# Get the directory where the script is located
directory = os.path.dirname(os.path.abspath(__file__))

# Process the files in the script's directory
process_files(directory)