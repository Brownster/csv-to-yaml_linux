import sys
import pandas as pd
import yaml
import os


###############LINUX#########################


def exporter_linux(file_path, output_file, output_dir):
    # Read CSV file into pandas DataFrame
    df = pd.read_csv(file_path)

    # Filter the data based on the condition
    df_filtered = df[df['Exporter_name_os'] == 'exporter_linux']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_blackbox key in the YAML dictionary
    yaml_output['exporter_linux'] = {}

    # Loop through the filtered data and add to the dictionary
    for _, row in df_filtered.iterrows():
        exporter_name = 'exporter_linux'
        fqdn = row['FQDN']
        ip_address = row['IP Address']
        listen_port = int(row['OS-Listen-Port'])
        location = row['Location']
        country = row['Country']
        username = 'your_username_here'
        password = 'your_password_here'
        if exporter_name not in yaml_output:
            yaml_output[exporter_name] = {}
        if fqdn not in data[exporter_name]:
            yaml_output[exporter_name][fqdn] = {}
        yaml_output[exporter_name][fqdn] = {
            'ip_address': ip_address,
            'listen_port': listen_port,
            'location': location,
            'country': country,
            'username': username,
            'password': password
        }

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)

#################BlackBox##################


def exporter_blackbox(file_path, output_file, output_dir):

    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[(df['icmp'] == True) & (df['ssh-banner'] == True)]

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_blackbox key in the YAML dictionary
    yaml_output['exporter_blackbox'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        exporter_name = 'exporter_blackbox'
        hostname = row['Hostnames']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
    
        if hostname not in yaml_output.get(exporter_name, {}):
             yaml_output[exporter_name][hostname] = {}
    
        if ip_address not in yaml_output[exporter_name][hostname]:
             yaml_output[exporter_name][hostname][ip_address] = {}
        
        yaml_output[exporter_name][hostname][ip_address]['location'] = location
        yaml_output[exporter_name][hostname][ip_address]['country'] = country
    
        if row['icmp']:
            yaml_output[exporter_name][hostname][ip_address]['module'] = 'icmp'
        
        if row['ssh-banner']:
            yaml_output[exporter_name][hostname][f'{ip_address}:22'] = {
                'module': 'ssh_banner',
                'location': location,
                'country': country
            }
    # Write the YAML data to a file, either appending to an existing file or creating a new file
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)

###################SSL####################


def exporter_ssl(file_path, output_file, output_dir):
    # Read CSV file into pandas DataFrame
    df = pd.read_csv(file_path)

    # Filter the data based on the condition
    df_filtered = df[df['Exporter_SSL'] == True]

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_cms key in the YAML dictionary
    yaml_output['exporter_ssl'] = {}

    # Loop through the filtered data and add to the dictionary
    for _, row in df_filtered.iterrows():
        exporter_name = 'exporter_ssl'
        fqdn = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
        listen_port = 443
        if exporter_name not in yaml_output:
            yaml_output[exporter_name] = {}
        if fqdn not in yaml_output[exporter_name]:
            yaml_output[exporter_name][fqdn] = {}
        yaml_output[exporter_name][fqdn] = {
            'ip_address': ip_address,
            'listen_port': listen_port,
            'location': location,
            'country': country,
        }

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)

################CMS#######################


def exporter_cms(file_path, output_file, output_dir):
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter the data based on the condition
    df_filtered = df[df['Exporter_name_app'] == 'exporter_cms']

    # Add new columns for username and password
    df['Username'] = 'root'
    df['Password'] = 'ENC'

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_cms key in the YAML dictionary
    yaml_output['exporter_cms'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        exporter_name = 'exporter_cms'
        hostname = row['Hostnames']
        ip_address = row['IP Address']
        listen_port = int(row['App-Listen-Port'])
        location = row['Location']
        country = row['Country']
        username = row['Username']
        password = row['Password']

        if hostname not in yaml_output.get(exporter_name, {}):
            yaml_output[exporter_name][hostname] = {}

        yaml_output[exporter_name][hostname]['ip_address'] = ip_address
        yaml_output[exporter_name][hostname]['listen_port'] = listen_port
        yaml_output[exporter_name][hostname]['location'] = location
        yaml_output[exporter_name][hostname]['country'] = country
        yaml_output[exporter_name][hostname]['username'] = username
        yaml_output[exporter_name][hostname]['password'] = password

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)



def run_scripts(scripts, file_path, output_file, output_dir):
    for script in scripts:
        if script == 'exporter_linux':
            exporter_linux(file_path, output_file, output_dir)
        elif script == 'exporter_blackbox':
            exporter_blackbox(file_path, output_file, output_dir)
        elif script == 'exporter_ssl':
            exporter_ssl(file_path, output_file, output_dir)

if __name__ == '__main__':
    # Get the script names from command line arguments
    script_names = sys.argv[1:]

    # Get the file path from command line arguments
    file_path = sys.argv[2]

    # Get the output file name from command line arguments
    output_file = sys.argv[3]

    # Get the output directory from command line arguments
    output_dir = sys.argv[4]

    # If "all" is specified, run all scripts
    if 'all' in script_names:
        run_scripts(['exporter_linux', 'exporter_blackbox', 'exporter_ssl', 'exporter_cms'], file_path, output_file, output_dir)
    else:
        exporter_names = script_names

    # Initialize exporter_names to empty list if not specified
    if not exporter_names:
        exporter_names = []

    # Loop through the exporter names and call the corresponding function
    for exporter_name in exporter_names:
        if exporter_name == 'exporter_linux':
            exporter_linux(file_path, output_file, output_dir)
        elif exporter_name == 'exporter_blackbox':
            exporter_blackbox(file_path, output_file, output_dir)
        elif exporter_name == 'exporter_ssl':
            exporter_ssl(file_path, output_file, output_dir)
        elif exporter_name == 'exporter_cms':
            exporter_cms(file_path, output_file, output_dir)
