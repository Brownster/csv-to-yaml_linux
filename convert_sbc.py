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

# Write the YAML data to a file
output_path = output_dir + output_file
with open(output_path, 'w') as f:
    yaml.dump(yaml_output, f)
