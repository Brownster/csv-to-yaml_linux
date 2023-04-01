import os
import pandas as pd
import yaml

def exporter_acm(file_path, output_file, output_dir, default_listen_port=8081):
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_acm']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_acm key in the YAML dictionary
    yaml_output['exporter_acm'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
        listen_port = row['App-Listen-Port']
        ssh_username = row.get('ssh_username', 'put your username here')
        ssh_password = row.get('ssh_password', 'put your password here')

        if hostname not in yaml_output.get('exporter_acm', {}):
            yaml_output['exporter_acm'][hostname] = {}

        yaml_output['exporter_acm'][hostname]['ip_address'] = ip_address
        yaml_output['exporter_acm'][hostname]['listen_port'] = int(listen_port) if not pd.isna(listen_port) else int(default_listen_port)
        yaml_output['exporter_acm'][hostname]['type'] = 'lsp' if 'lsp' in hostname.lower() else 'ess'
        yaml_output['exporter_acm'][hostname]['location'] = location
        yaml_output['exporter_acm'][hostname]['country'] = country
        yaml_output['exporter_acm'][hostname]['username'] = ssh_username
        yaml_output['exporter_acm'][hostname]['password'] = ssh_password

    # Write the YAML data to a file
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w') as f:
        yaml.dump(yaml_output, f, default_flow_style=False)
        print(f"Exporter ACM completed")
        print(f"Total number of hosts processed: {len(yaml_output['exporter_acm'])}")
