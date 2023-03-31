import os
import pandas as pd
import yaml

def exporter_genesyscloud(file_path, output_file, output_dir):
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_genesyscloud']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_genesyscloud key in the YAML dictionary
    yaml_output['exporter_genesyscloud'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        hostname = row['FQDN']
        listen_port = row['App-Listen-Port']

        yaml_output['exporter_genesyscloud'][hostname] = {
            'listen_port': listen_port,
            'extra_args': (" --client.managed  --billing.enabled --billing.frequency 30m --usage.enabled "
                          "--usage.frequency 12h --client.first-day-of-month 22 --mos.enabled "
                          "--mos.bandceilingcritical 2.59999 --mos.bandceilingbad 3.59999 "
                          "--mos.bandceilingwarning 3.09999 --mos.bandceilinggood 3.99999"),
            'client_id': 'ENC[PKCS7...]',
            'client_secret': 'ENC[PKCS7...]',
            'client_basepath': 'https://api.mypurecloud.ie'
        }

    # Write the YAML data to a file
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w') as f:
        yaml.dump(yaml_output, f, default_flow_style=False)
