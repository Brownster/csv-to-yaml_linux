import sys
import pandas as pd
import yaml

def exporter_ssl(file_path, output_file, output_dir):
    print("Exporter converter_SSL called")
    # Read CSV file into pandas DataFrame
    df = pd.read_csv(file_path)

    # Filter the data based on the condition
    df_filtered = df[df['Exporter_SSL'] == True]

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_cms key in the YAML dictionary
    yaml_output['exporter_ssl'] = {}

    output_path = os.path.join(output_dir, output_file)

    # Loop through the filtered data and add to the dictionary
    for _, row in df_filtered.iterrows():
        exporter_name = 'exporter_ssl'
        fqdn = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
        exporter_app = row['Exporter_name_app']
        
        # Set default listen_port to 443 and change it to 8443 if exporter_avayasbc is specified
        listen_port = 8443 if exporter_app == 'exporter_avayasbc' else 443

        # Check for duplicate entries
        if ip_exists_in_yaml(exporter_name, ip_address, output_path):
            continue

        if exporter_name not in yaml_output:
            yaml_output[exporter_name] = {}
        if fqdn not in yaml_output[exporter_name]:
            yaml_output[exporter_name][fqdn] = {}
        yaml_output[exporter_name][fqdn] = {
            'ip_address': ip_address,
            'listen_port': listen_port,
            'location': location,
            'country': country,
        }

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if yaml_output['exporter_ssl']:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    print("Exporter converter_SSL completed")
