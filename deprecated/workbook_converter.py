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

##################WINDOWS###################

def exporter_windows(file_path, output_file, output_dir):
    
    # Read CSV file into pandas
    df = pd.read_csv(file_path)
    
    # Filter the data based on the condition
    df_filtered = df[df['Exporter_name_os'] == 'exporter_windows']


    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_cms key in the YAML dictionary
    yaml_output['exporter_windows'] = {}

    # Loop through the filtered data and add to the dictionary
    for _, row in df_filtered.iterrows():
        exporter_name = 'exporter_windows'
        fqdn = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
        listen_port = 9182
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

            
 ##############VERINT###########################

def exporter_verint(file_path, output_file, output_dir):
    
    # Read CSV file into pandas
    df = pd.read_csv(file_path)
    
    # Filter the data based on the condition
    df_filtered = df[df['Exporter_name_os'] == 'exporter_verint']


    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_cms key in the YAML dictionary
    yaml_output['exporter_verint'] = {}

    # Loop through the filtered data and add to the dictionary
    for _, row in df_filtered.iterrows():
        exporter_name = 'exporter_verint'
        fqdn = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
        listen_port = 9182
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
            
            
            
            
##################AVAYA SBC###########################

def exporter_avayasbc(file_path, output_file, output_dir):


    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_sbc']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_avayasbc key in the YAML dictionary
    yaml_output['exporter_avayasbc'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        exporter_name = 'exporter_avayasbc'
        ip_address = row['IP_address']
        location = row['Location']
        country = row['Country']
        username = 'ipcs'  # Generate username as it does not exist in the CSV file
        hostname = row['Exporter_hostname']
    
        if hostname not in yaml_output.get(exporter_name, {}):
            yaml_output[exporter_name][hostname] = {}
    
        yaml_output[exporter_name][hostname][ip_address] = {
            'ip_address': ip_address,
            'listen_port': 3601,  # Hard-coded as it is not present in the CSV file
            'location': location,
            'country': country,
            'username': username
        }

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)
 
######################GATEWAY###############

def exporter_gateway(file_path, output_file, output_dir):
    
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on exporter_name condition
    df = df[df['Exporter_name_app'] == 'exporter_gateway']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_gateway key in the YAML dictionary
    yaml_output['exporter_gateway'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        exporter_name = 'exporter_gateway'
        hostname = row['Hostnames']
        ip_address = row['IP Address']
        listen_port = int(row['App-Listen-Port'])
        location = row['Location']
        country = row['Country']
    
        if hostname not in yaml_output.get(exporter_name, {}):
            yaml_output[exporter_name][hostname] = {}
    
        yaml_output[exporter_name][hostname]['ip_address'] = ip_address
        yaml_output[exporter_name][hostname]['listen_port'] = listen_port
        yaml_output[exporter_name][hostname]['location'] = location
        yaml_output[exporter_name][hostname]['country'] = country
        yaml_output[exporter_name][hostname]['snmp_version'] = 2
        yaml_output[exporter_name][hostname]['community'] = 'ENC'

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)            
 

#################BREEZE##############

def exporter_breeze(file_path, output_file, output_dir):
    
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_breeze']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_breeze key in the YAML dictionary
    yaml_output['exporter_breeze'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        exporter_name = 'exporter_breeze'
        hostname = row['Hostnames']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if hostname not in yaml_output.get(exporter_name, {}):
            yaml_output[exporter_name][hostname] = {}

        if ip_address not in yaml_output[exporter_name][hostname]:
            yaml_output[exporter_name][hostname][ip_address] = {}

        yaml_output[exporter_name][hostname][ip_address]['listen_port'] = int(row['App-Listen-Port'])
        yaml_output[exporter_name][hostname][ip_address]['location'] = location
        yaml_output[exporter_name][hostname][ip_address]['country'] = country
        yaml_output[exporter_name][hostname][ip_address]['username'] = 'root'
        yaml_output[exporter_name][hostname][ip_address]['password'] = 'ENC'

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)   



##################MAIN LOOP###################

def run_scripts(scripts, file_path, output_file, output_dir):
    for script in scripts:
        if script == 'exporter_linux':
            exporter_linux(file_path, output_file, output_dir)
        elif script == 'exporter_blackbox':
            exporter_blackbox(file_path, output_file, output_dir)
        elif script == 'exporter_ssl':
            exporter_ssl(file_path, output_file, output_dir)
        elif script == 'exporter_cms':
            exporter_cms(file_path, output_file, output_dir)
        elif script == 'exporter_windows':
            exporter_windows(file_path, output_file, output_dir)            
        elif script == 'exporter_avayasbc':
            exporter_avayasbc(file_path, output_file, output_dir)  
        elif script == 'exporter_verint':
            exporter_verint(file_path, output_file, output_dir)  
        elif script == 'exporter_gateway':
            exporter_gateway(file_path, output_file, output_dir)             
         elif script == 'exporter_breeze':
            exporter_breeze(file_path, output_file, output_dir)  
            
            
            
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
        run_scripts(['exporter_linux', 'exporter_blackbox', 'exporter_breeze', 'exporter_avayasbc', 'exporter_gateway', 'exporter_verint', 'exporter_windows', 'exporter_ssl', 'exporter_cms'], file_path, output_file, output_dir)
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
        elif exporter_name == 'exporter_windows':
            exporter_windows(file_path, output_file, output_dir)
        elif exporter_name == 'exporter_avayasbc':
            exporter_avayasbc(file_path, output_file, output_dir)
        elif exporter_name == 'exporter_verint':
            exporter_verint(file_path, output_file, output_dir)
        elif exporter_name == 'exporter_gateway':
            exporter_gateway(file_path, output_file, output_dir) 
        elif exporter_name == 'exporter_breeze':
            exporter_breeze(file_path, output_file, output_dir)               
