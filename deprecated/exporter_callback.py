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
    new_entries = []
    for index, row in df.iterrows():
        exporter_name = 'exporter_callback'
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if ip_exists_in_yaml(exporter_name, ip_address, output_dir, output_file):
            continue

        if hostname not in yaml_output.get('exporter_callback', {}):
            yaml_output['exporter_callback'][hostname] = {}

        if pd.isna(row['App-Listen-Port']):
            listen_port = default_listen_port.get()
        else:
            listen_port = int(row['App-Listen-Port'])

        yaml_output['exporter_callback'][hostname]['ip_address'] = ip_address
        yaml_output['exporter_callback'][hostname]['listen_port'] = listen_port
        yaml_output['exporter_callback'][hostname]['location'] = location
        yaml_output['exporter_callback'][hostname]['country'] = country

        # Check if optional headers are present
        ssh_username_present = 'ssh_username' in df.columns
        ssh_password_present = 'ssh_password' in df.columns

        # Use the values from the optional headers if present, otherwise use the placeholders
        if ssh_username_present and not pd.isna(row['ssh_username']):
            yaml_output['exporter_callback'][hostname]['username'] = row['ssh_username']
        else:
            yaml_output['exporter_callback'][hostname]['username'] = 'maas'

        if ssh_password_present and not pd.isna(row['ssh_password']):
            yaml_output['exporter_callback'][hostname]['password'] = row['ssh_password']
        else:
            yaml_output['exporter_callback'][hostname]['password'] = 'ENC'

        new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if new_entries:
        output_path = os.path.join(output_dir, output_file)
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f, default_flow_style=False)
        print("Exporter Callback completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter Callback completed - nothing to do")


####### check if exists in yaml section ########

def ip_exists_in_yaml(exporter_name, ip_address, output_dir, output_file):
    """
    Check if the given IP address already exists in the YAML file for the given exporter
    """
    output_path = os.path.join(output_dir, output_file)
    if not os.path.exists(output_path):
        return False

    with open(output_path, 'r') as f:
        yaml_output = yaml.safe_load(f)
        if yaml_output is not None and exporter_name in yaml_output:
            for hostname, ip_data in yaml_output[exporter_name].items():
                if ip_address in ip_data['ip_address']:
                    return True
    return False
