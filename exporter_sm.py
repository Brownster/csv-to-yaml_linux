def exporter_sm(file_path, output_file, output_dir):
    global listen_port_var
    global output_path
    try:
        print("Exporter SM called")

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
    df_filtered = df[df['Exporter_name_app'] == 'exporter_sm']

    output_path = os.path.join(output_dir, output_file)

    # Initialize exporter_sm key in the YAML dictionary
    yaml_output = {'exporter_sm': {}}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df_filtered.iterrows():
        exporter_name = 'exporter_sm'
        hostname = row['Hostnames']
        ip_address = row['IP Address']
        listen_port = row['App-Listen-Port'] if not pd.isna(row['App-Listen-Port']) else listen_port_var.get()

        # Check for duplicate entries
        if ip_exists_in_yaml(exporter_name, ip_address, os.path.join(output_dir, output_file)):
            continue

        if hostname not in yaml_output[exporter_name]:
            yaml_output[exporter_name][hostname] = {}
        if ip_address not in yaml_output[exporter_name][hostname]:
            yaml_output[exporter_name][hostname][ip_address] = {}
        
        yaml_output[exporter_name][hostname][ip_address]['listen_port'] = int(listen_port)
        
        new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if new_entries:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
        print("Exporter SM completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter SM completed - nothing to do")
