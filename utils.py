import json


# helper method for reading cached data into memory
def read_config_from_file(server_data):
    try:
        with open('server.json', 'r') as file:
            server_data = json.load(file)
    except:
        print('error reading from file')
        server_data = {}

    return server_data


# helper method for writing cached data onto disk
def write_config_to_file(server_data):
    try:
        with open('server.json', 'w') as file:
            json.dump(server_data, file)
    except:
        print('error writing to file')