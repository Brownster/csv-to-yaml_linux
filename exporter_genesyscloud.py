import os
import pandas as pd
import yaml

def exporter_genesyscloud(file_path, output_file, output_dir):
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_genesyscloud']

    # Define output path
    output_path = os.path.join(output_dir, output_file)

    # Check existing IPs in YAML output
    existing_ips = set()
    if os.path.exists(output_path):
        with open(output_path, 'r') as f:
            yaml_output = yaml.safe_load(f)
            for ip_addresses in yaml_output.get('exporter_genesyscloud', {}).values():
                for ip_address in ip_addresses.keys():
                    existing_ips.add(ip_address)

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_genesyscloud key in the YAML dictionary
    yaml_output['exporter_genesyscloud'] = {}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df.iterrows():
        hostname = row['FQDN']
        listen_port = row['App-Listen-Port']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
        comm_string = row.get('comm_string', 'public')

        if ip_address in existing_ips:
            continue

        yaml_output['exporter_genesyscloud'][hostname] = {
            'listen_port': listen_port,
            'extra_args': (" --client.managed  --billing.enabled --billing.frequency 30m --usage.enabled "
                          "--usage.frequency 12h --client.first-day-of-month 22 --mos.enabled "
                          "--mos.bandceilingcritical 2.59999 --mos.bandceilingbad 3.59999 "
                          "--mos.bandceilingwarning 3.09999 --mos.bandceilinggood 3.99999"),
            'client_id': 'ENC[PKCS7...]',
            'client_secret': 'ENC[PKCS7...]',
            'client_basepath': 'https://api.mypurecloud.ie',
            'ip_address': ip_address,
            'location': location,
            'country': country,
            'community': comm_string
        }

        existing_ips.add(ip_address)
        new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if new_entries:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f, default_flow_style=False)
        print("Exporter Genesys Cloud completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter Genesys Cloud completed - nothing to do")
