import os
import pandas as pd
import yaml

def exporter_drac(file_path, output_file, output_dir):
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df_filtered = df[df['Exporter_name_app'] == 'exporter_drac']

    # Define output path
    output_path = os.path.join(output_dir, output_file)

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_drac key in the YAML dictionary
    yaml_output['exporter_drac'] = {}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df_filtered.iterrows():
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if ip_exists_in_yaml('exporter_drac', ip_address, output_path=output_path):
            continue

        if hostname not in yaml_output['exporter_drac']:
            yaml_output['exporter_drac'][hostname] = {}

        yaml_output['exporter_drac'][hostname]['ip_address'] = ip_address
        yaml_output['exporter_drac'][hostname]['listen_port'] = 623
        yaml_output['exporter_drac'][hostname]['location'] = location
        yaml_output['exporter_drac'][hostname]['country'] = country
        yaml_output['exporter_drac'][hostname]['snmp_version'] = 2
        yaml_output['exporter_drac'][hostname]['community'] = row.get('comm_string', 'ENC')

        new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if new_entries:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f, default_flow_style=False)
        print("Exporter DRAC completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter DRAC completed - nothing to do")

