import sys
import pandas as pd
import yaml

# Get the file path from command line arguments
file_path = sys.argv[1]

# Get the output file name from command line arguments
output_file = sys.argv[2]

# Get the output directory from command line arguments
output_dir = sys.argv[3]

# Read CSV file into pandas
df = pd.read_csv(file_path)

# Filter rows based on condition
df = df[df['Exporter_name_app'] == 'exporter_cms']

# Create an empty dictionary to store the YAML output
yaml_output = {}

# Iterate over rows in filtered dataframe
for index, row in df.iterrows():
    exporter_name = 'exporter_cms'
    hostname = row['Hostnames']
    ip_address = row['IP Address']
    listen_port = row['Listen Port']
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

# Write the YAML data to a file
output_path = output_dir + output_file
with open(output_path, 'w') as f:
    yaml.dump(yaml_output, f)
