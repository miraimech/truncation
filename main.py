import os

def process_inter_dealer_brokers_section(broker, index, base_file_path):
    # Write each broker's information to a separate file
    file_name = f"{os.path.splitext(base_file_path)[0]}_interDealerBrokers_{index}.txt"
    with open(file_name, 'w') as file:
        file.write(str(broker))

def process_file(file_path):
    data = {
        "releaseDate": "",
        "title": "",
        "numDealers": {},
        "interDealerBrokers": [],
        "others": [],
        "totals": []
    }

    def process_section(section):
        if section.startswith('releaseDate'):
            data['releaseDate'] = section.split(':', 1)[1].strip()
        elif section.startswith('title'):
            data['title'] = section.split(':', 1)[1].strip()
        elif section.startswith('numDealers'):
            data['numDealers'] = eval(section.split(':', 1)[1].strip())
        elif section.startswith('interDealerBrokers'):
            inter_dealer_brokers = eval(section.split(':', 1)[1].strip())
            for index, broker in enumerate(inter_dealer_brokers):
                data['interDealerBrokers'].append(broker)
                process_inter_dealer_brokers_section(broker, index, file_path)
        elif section.startswith('others'):
            data['others'] = eval(section.split(':', 1)[1].strip())
        elif section.startswith('totals'):
            data['totals'] = eval(section.split(':', 1)[1].strip())

    try:
        with open(file_path, 'r') as file:
            content = file.read()

        sections = content.split('\n\n')
        for section in sections:
            process_section(section)

        return data
    except Exception as e:
        print(f"An error occurred: {e}")

# Process the quarterly data file
file_path_quarterly = 'market_share_quarterly_fixed.txt'
processed_data_quarterly = process_file(file_path_quarterly)

# Process the yearly data file
file_path_yearly = 'market_share_yearly_fixed.txt'
processed_data_yearly = process_file(file_path_yearly)