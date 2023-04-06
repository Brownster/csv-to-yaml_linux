def exporter_breeze(file_path, output_file, output_dir):
    global default_listen_port
    global output_path

    try:
        print("Exporter Breeze called")

        df = read_input_file(file_path)

    except Exception as e:
        print(f"Error: {e}")
        return

    df_filtered = filter_rows_by_exporter(df, 'exporter_breeze')
    output_path = os.path.join(output_dir, output_file)

    yaml_output = {'exporter_breeze': {}}

    for index, row in df_filtered.iterrows():
        process_row_breeze(row, yaml_output)

    new_entries = df_filtered.to_dict('records')
    existing_yaml_output = load_existing_yaml(output_path)

    # Write the YAML data to a file, either updating the existing file or creating a new file
    process_exporter('exporter_breeze', existing_yaml_output, new_entries, yaml_output, output_path)
