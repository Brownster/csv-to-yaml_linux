import sys
import pandas as pd
import yaml

def exporter_windows(file_path, output_file, output_dir):
    global output_path
    
    try:
        print("Exporter Windows called")

        # Check if file is CSV or Excel
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.csv':
            # Read CSV file into pandas
            df = pd.read_csv(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            # Read Excel file into pandas
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Invalid file type. Only CSV and Excel files are supported.")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Filter rows based on condition
    df_filtered = df[df['Exporter_name_os'] == 'exporter_windows']

    output_path = os.path.join(output_dir, output_file)

    # Initialize exporter_windows key in the YAML dictionary
    yaml_output = {'exporter_windows': {}}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df_filtered.iterrows():
        exporter_name = 'exporter_windows'
        fqdn = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if ip_exists_in_yaml(exporter_name, ip_address, output_path=output_path):
            continue

        if fqdn not in yaml_output[exporter_name]:
            yaml_output[exporter_name][fqdn] = {}

        yaml_output[exporter_name][fqdn]['ip_address'] = ip_address
        yaml_output[exporter_name][fqdn]['listen_port'] = 9182  # Set to default listen port for Windows
        yaml_output[exporter_name][fqdn]['location'] = location
        yaml_output[exporter_name][fqdn]['country'] = country

        new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if new_entries:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
        print("Exporter Windows completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter Windows completed - nothing to do")
