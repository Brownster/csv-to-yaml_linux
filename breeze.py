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

    yaml_output[exporter_name][hostname][ip_address]['location'] = location
    yaml_output[exporter_name][hostname][ip_address]['country'] = country
    yaml_output[exporter_name][hostname][ip_address]['listen_port'] = int(row['ListenPort'])
    yaml_output[exporter_name][hostname][ip_address]['username'] = 'root'
    yaml_output[exporter_name][hostname][ip_address]['password'] = 'ENC'

# Write the YAML data to a file
output_path = output_dir + output_file
with open(output_path, 'w') as f:
    yaml.dump(yaml_output, f)
