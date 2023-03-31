import os
import pandas as pd
import yaml

def exporter_callback(file_path, output_file, output_dir):
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_callback']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_callback key in the YAML dictionary
    yaml_output['exporter_callback'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if hostname not in yaml_output.get('exporter_callback', {}):
            yaml_output['exporter_callback'][hostname] = {}

        yaml_output['exporter_callback'][hostname]['ip_address'] = ip_address
        yaml_output['exporter_callback'][hostname]['listen_port'] = int(row['App-Listen-Port'])
        yaml_output['exporter_callback'][hostname]['location'] = location
        yaml_output['exporter_callback'][hostname]['country'] = country
        yaml_output['exporter_callback'][hostname]['username'] = 'maas'
        yaml_output['exporter_callback'][hostname]['password'] = 'ENC'

    # Write the YAML data to a file
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w') as f:
        yaml.dump(yaml_output, f, default_flow_style=False)
