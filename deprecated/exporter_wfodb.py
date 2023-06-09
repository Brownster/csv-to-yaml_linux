import os
import pandas as pd
import yaml

def exporter_wfodb(file_path, output_file, output_dir):
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_wfodb']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_wfodb key in the YAML dictionary
    yaml_output['exporter_wfodb'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        hostname = row['FQDN']
        ip_address = row['IP Address']
        listen_port = row['App-Listen-Port']
        location = row['Location']
        country = row['Country']

        yaml_output['exporter_wfodb'][hostname] = {
            'ip_address': ip_address,
            'listen_port': listen_port,
            'location': location,
            'country': country,
            'username': 'maas',
            'password': 'ENC',
        }

    # Write the YAML data to a file
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w') as f:
        yaml.dump(yaml_output, f, default_flow_style=False)
