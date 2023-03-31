import os
import pandas as pd
import yaml

def exporter_jmx(file_path, output_file, output_dir):
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_jmx']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_jmx key in the YAML dictionary
    yaml_output['exporter_jmx'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if hostname not in yaml_output.get('exporter_jmx', {}):
            yaml_output['exporter_jmx'][hostname] = {}

        ports = [8081, 8082]
        for port in ports:
            if port not in yaml_output['exporter_jmx'][hostname]:
                yaml_output['exporter_jmx'][hostname][str(port)] = {}

            yaml_output['exporter_jmx'][hostname][str(port)]['ip_address'] = ip_address
            yaml_output['exporter_jmx'][hostname][str(port)]['location'] = location
            yaml_output['exporter_jmx'][hostname][str(port)]['country'] = country

            if port == 8081:
                yaml_output['exporter_jmx'][hostname][str(port)]['username'] = 'put your username here'
                yaml_output['exporter_jmx'][hostname][str(port)]['password'] = 'put your password here'

    # Write the YAML data to a file
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w') as f:
        yaml.dump(yaml_output, f, default_flow_style=False)
