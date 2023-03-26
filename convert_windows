import sys
import pandas as pd
import yaml

# Get the file path from command line arguments
file_path = sys.argv[1]

# Get the output file name from command line arguments
output_file = sys.argv[2]

# Get the output directory from command line arguments
output_dir = sys.argv[3]

# Read CSV file into pandas DataFrame
df = pd.read_csv(file_path)

# Filter the data based on the condition
df_filtered = df[df['Exporter_name_os'] == 'exporter_windows']

# Create an empty dictionary to hold the final YAML data
data = {}

# Loop through the filtered data and add to the dictionary
for _, row in df_filtered.iterrows():
    exporter_name = 'exporter_windows'
    fqdn = row['FQDN']
    ip_address = row['IP Address']
    location = row['Location']
    country = row['Country']
    listen_port = 9182
    if exporter_name not in data:
        data[exporter_name] = {}
    if fqdn not in data[exporter_name]:
        data[exporter_name][fqdn] = {}
    data[exporter_name][fqdn] = {
        'ip_address': ip_address,
        'listen_port': listen_port,
        'location': location,
        'country': country,
    }

# Write the YAML data to a file
output_path = output_dir + output_file
with open(output_path, 'w') as f:
    yaml.dump(data, f)
