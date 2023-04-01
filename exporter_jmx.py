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
    new_entries = []
    for index, row in df.iterrows():
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if ip_exists_in_yaml('exporter_jmx', ip_address, output_dir=output_dir, output_file=output_file):
            continue

        if hostname not in yaml_output.get('exporter_jmx', {}):
            yaml_output['exporter_jmx'][hostname] = {}

        jmx_ports = row.get('jmx_ports', None)
        if jmx_ports is None:
            ports = [8081, 8082]
        else:
            ports = [int(port) for port in jmx_ports.split(',')]

        for port in ports:
            if port not in yaml_output['exporter_jmx'][hostname]:
                yaml_output['exporter_jmx'][hostname][str(port)] = {}

            yaml_output['exporter_jmx'][hostname][str(port)]['ip_address'] = ip_address
            yaml_output['exporter_jmx'][hostname][str(port)]['location'] = location
            yaml_output['exporter_jmx'][hostname][str(port)]['country'] = country


    # Write the YAML data to a file
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'a') as f:
        yaml.dump(yaml_output, f, default_flow_style=False)
        print("Exporter JMX completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
