import os

def process_inter_dealer_brokers_section(broker, index, base_file_path):
    file_name = f"{os.path.splitext(base_file_path)[0]}_interDealerBrokers_{index}.txt"
    print(f"Attempting to save file: {file_name}")  # Debugging print
    try:
        with open(file_name, 'w') as file:
            file.write(str(broker))
        print(f"File saved: {file_name}")  # Confirmation print
    except Exception as e:
        print(f"Error saving file {file_name}: {e}")  # Error print
def process_file(file_path):
    data = {
        "releaseDate": "",
        "title": "",
        "numDealers": {},
        "interDealerBrokers": [],
        "others": [],
        "totals": []
    }

    def process_line(line):
        if line.startswith('releaseDate'):
            data['releaseDate'] = line.split(':', 1)[1].strip()
        elif line.startswith('title'):
            data['title'] = line.split(':', 1)[1].strip()
        elif line.startswith('numDealers'):
            data['numDealers'] = eval(line.split(':', 1)[1].strip())
        elif line.startswith('interDealerBrokers'):
            brokers_data = line.split(':', 1)[1].strip()
            inter_dealer_brokers = eval(brokers_data)
            for index, broker in enumerate(inter_dealer_brokers):
                data['interDealerBrokers'].append(broker)
                process_inter_dealer_brokers_section(broker, index, file_path)
        elif line.startswith('others'):
            data['others'] = eval(line.split(':', 1)[1].strip())
        elif line.startswith('totals'):
            data['totals'] = eval(line.split(':', 1)[1].strip())

    try:
        with open(file_path, 'r') as file:
            for line in file:
                process_line(line.strip())

        return data
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

# Process the quarterly data file
file_path_quarterly = 'market_share_quarterly_fixed.txt'
print(f"Processing file: {file_path_quarterly}")  # Debugging print
processed_data_quarterly = process_file(file_path_quarterly)

# Process the yearly data file
file_path_yearly = 'market_share_yearly_fixed.txt'
print(f"Processing file: {file_path_yearly}")  # Debugging print
processed_data_yearly = process_file(file_path_yearly)