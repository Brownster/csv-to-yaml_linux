import os
import pandas as pd
import yaml

def exporter_weblm(file_path, output_file, output_dir):
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_weblm']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_weblm key in the YAML dictionary
    yaml_output['exporter_weblm'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
        listen_port = row['App-Listen-Port']

        if hostname not in yaml_output.get('exporter_weblm', {}):
            yaml_output['exporter_weblm'][hostname] = {}

        yaml_output['exporter_weblm'][hostname]['ip_address'] = ip_address
        yaml_output['exporter_weblm'][hostname]['listen_port'] = int(listen_port) if listen_port else None
        yaml_output['exporter_weblm'][hostname]['location'] = location
        yaml_output['exporter_weblm'][hostname]['country'] = country
        yaml_output['exporter_weblm'][hostname]['data_path'] = '/opt/Avaya/tomcat/webapps/WebLM/data/'
        yaml_output['exporter_weblm'][hostname]['username'] = 'put your username here'
        yaml_output['exporter_weblm'][hostname]['password'] = 'put your password here'

    # Write the YAML data to a file
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w') as f:
        yaml.dump(yaml_output, f, default_flow_style=False)
