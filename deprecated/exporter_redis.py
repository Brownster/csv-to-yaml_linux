import os
import pandas as pd
import yaml

def exporter_redis(file_path, output_file, output_dir):
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_redis']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_redis key in the YAML dictionary
    yaml_output['exporter_redis'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
        application = row['Application']

        if hostname not in yaml_output.get('exporter_redis', {}):
            yaml_output['exporter_redis'][hostname] = {}

        yaml_output['exporter_redis'][hostname]['ip_address'] = ip_address
        yaml_output['exporter_redis'][hostname]['listen_port'] = int(row['App-Listen-Port'])
        yaml_output['exporter_redis'][hostname]['location'] = location
        yaml_output['exporter_redis'][hostname]['country'] = country
        yaml_output['exporter_redis'][hostname]['password'] = 'put your password here'
        yaml_output['exporter_redis'][hostname]['redis_port'] = 6379
        yaml_output['exporter_redis'][hostname]['username'] = 'put your username here'
        yaml_output['exporter_redis'][hostname]['redis_address'] = f"redis://{ip_address}:6379"
        yaml_output['exporter_redis'][hostname]['debug'] = True
        yaml_output['exporter_redis'][hostname]['application'] = application

    # Write the YAML data to a file
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w') as f:
        yaml.dump(yaml_output, f, default_flow_style=False)
