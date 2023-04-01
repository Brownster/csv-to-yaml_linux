import os
import pandas as pd
import yaml

def exporter_kafka(file_path, output_file, output_dir):
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_kafka']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_kafka key in the YAML dictionary
    yaml_output['exporter_kafka'] = {}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df.iterrows():
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if ip_exists_in_yaml('exporter_kafka', ip_address, output_dir=output_dir, output_file=output_file):
            continue

        if hostname not in yaml_output.get('exporter_kafka', {}):
            yaml_output['exporter_kafka'][hostname] = {}

        yaml_output['exporter_kafka'][hostname]['ip_address'] = ip_address
        yaml_output['exporter_kafka'][hostname]['listen_port'] = int(row['App-Listen-Port'])
        yaml_output['exporter_kafka'][hostname]['location'] = location
        yaml_output['exporter_kafka'][hostname]['country'] = country
        yaml_output['exporter_kafka'][hostname]['kafka_port'] = 9092

        new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if new_entries:
        output_path = os.path.join(output_dir, output_file)
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f, default_flow_style=False)
        print("Exporter Kafka completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter Kafka completed - nothing to do")
    with open(output_path, 'w') as f:
        yaml.dump(yaml_output, f, default_flow_style=False)
