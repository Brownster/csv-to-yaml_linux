# csv-to-yaml - Prometheus config

# Exporters GUI

This is a Python script that creates a GUI application using tkinter to generate YAML files based on the data from a CSV or Excel file. The GUI allows users to select specific exporters, input file path, output file name, and output directory. Then, it processes the selected exporters and generates YAML files accordingly.

Here's a high-level overview of the script:

    The script contains multiple functions that represent different exporters, such as exporter_breeze, exporter_linux, exporter_blackbox, etc. Each function processes the input file and filters the data based on the exporter name. It then writes the filtered data to the output YAML file.

    The ip_exists_in_yaml function checks if a given IP address already exists in the YAML file for a given exporter.

    The create_exporter_checkbuttons function creates checkboxes for each exporter in the GUI.

    The run_exporters function is called when the "Go" button is clicked, and it runs the selected exporters using the provided input file, output file, and output directory.

    The browse_file_path and browse_output_dir functions are used to open file dialogs for selecting the input file and output directory, respectively.

    The StdoutRedirector class is used to redirect the standard output and standard error streams to the GUI's text widget, allowing the user to see any printed output or errors.

    The GUI is created using tkinter, and various elements such as labels, entry fields, buttons, and checkboxes are added to the interface. The script also creates tooltips for each element to provide more information to the user.

    The script enters the main event loop to display the GUI and wait for user input.

To run this script, you need to have Python and the required libraries (tkinter, pandas, and PyYAML) installed on your system. Save the script as a .py file, and then execute it using the Python interpreter:

bash

python script_name.py

Replace script_name.py with the name you saved the script as. This will open the GUI, and you can use it to generate the YAML files based on your input data.

windows exe built with (when in folder of csv file):

C:\Python39\python.exe C:\Python39\Lib\site-packages\PyInstaller\__main__.py --onefile workbook_converter_gui.py



Break Down of Functions:

exporter_generic:

    Define exporter_generic function with the following parameters:
        exporter_name: The name of the exporter to process.
        file_path: The path to the input file.
        output_file: The name of the output file.
        output_dir: The directory to save the output file in.

    Set default_listen_port and output_path as global variables.

    Read the input file using read_input_file function, handling exceptions with a try-except block.

    Filter the DataFrame using filter_rows_by_exporter function based on the exporter_name.

    Construct the output_path by joining output_dir and output_file.

    Initialize an empty dictionary yaml_output with a key for the exporter_name.

    Loop through the filtered DataFrame rows, and process each row using the process_row_generic function. This function updates the yaml_output dictionary with the row data.

    Convert the filtered DataFrame to a list of dictionaries using to_dict('records') and store it in new_entries.

    Load the existing YAML data from the output file using the load_existing_yaml function.

    Write the YAML data to the output file, either updating the existing file or creating a new one, using the process_exporter function with the following parameters:
        exporter_name
        existing_yaml_output
        new_entries
        yaml_output
        output_path

By using this generic function, you can process different exporters by just providing the appropriate exporter_name instead of writing separate functions for each exporter.


process_row_generic:

This function, process_row_generic, is designed to process a single row from a DataFrame and update the yaml_output dictionary accordingly for a generic exporter. It takes the following parameters:

    exporter_name: The name of the exporter to process.
    row: A single row from the DataFrame.
    yaml_output: A dictionary that stores the YAML output.
    default_listen_port: A default listen port value.

Here's a step-by-step explanation of the function:

    Extract relevant information from the row such as hostname, ip_address, location, and country.

    Check if the IP address already exists in the YAML output using the ip_exists_in_yaml function. If it exists, return early and don't process the row.

    If the hostname is not already in the yaml_output dictionary under the exporter_name key, create a new dictionary for it.

    Check if the 'App-Listen-Port' value is available in the row. If not, use the default_listen_port value. If listen_port is the same as the default_listen_port, increment the default_listen_port by 1.

    Update the yaml_output dictionary with the extracted information, such as ip_address, listen_port, location, and country.

    Check if the optional headers ssh_username and ssh_password are present in the row.

    If the ssh_username is present and not empty, use its value. Otherwise, use the default value 'root' for the username.

    If the ssh_password is present and not empty, use its value. Otherwise, use the default value 'ENC' for the password.

This function is called within the exporter_generic function to process each row of the filtered DataFrame and update the yaml_output dictionary. It provides a generic way to process rows for different exporters without writing separate functions for each exporter.




filter_rows_by_exporter:

The filter_rows_by_exporter function is designed to filter the rows of a DataFrame based on the exporter_name provided. Here's a step-by-step explanation of the function:

    Define a list os_exporters containing the names of the exporters that belong to the "os" category (operating system-based exporters).

    Check if the given exporter_name is in the os_exporters list.
        If it is, set the column_name variable to 'Exporter_name_os', which corresponds to the column in the DataFrame where operating system-based exporters are specified.
        If it isn't, set the column_name variable to 'Exporter_name_app', which corresponds to the column in the DataFrame where application-based exporters are specified.

    Return a new DataFrame containing only the rows where the value in the column_name column matches the given exporter_name.

This function is used to filter the rows of the input DataFrame so that only the rows relevant to the specified exporter are processed. It helps separate the rows based on whether the exporter is an operating system-based exporter or an application-based exporter, making it easier to handle different types of exporters.




read_input_file:

The read_input_file function is responsible for reading an input file, either a CSV or an Excel file, and returning a pandas DataFrame object. Here's a step-by-step explanation of the function:

    Determine the file extension of the input file using the os.path.splitext method. It returns the file extension as the second element of the resulting tuple (e.g., .csv, .xlsx, .xls).

    Check the file extension:
        If the file extension is .csv, use pandas' pd.read_csv method to read the file into a DataFrame object. The skiprows parameter is set to 7, meaning the first 7 rows of the file will be skipped when reading the data.
        If the file extension is either .xlsx or .xls, use pandas' pd.read_excel method to read the file into a DataFrame object. The sheet_name parameter is set to 'Sheet2', meaning the data will be read from the 'Sheet2' sheet of the Excel workbook. The skiprows parameter is set to range(0, 6), meaning the first 6 rows of the sheet will be skipped when reading the data.
        If the file extension is neither of the above, raise a ValueError indicating that the file type is not supported.

    Return the DataFrame object containing the data read from the input file.

This function is used to read the input data file and create a DataFrame object that can be used for further processing and filtering. It supports both CSV and Excel file formats, making it flexible for different types of input data files.




process_exporter:

The process_exporter function handles writing the YAML data to a file, either updating an existing file or creating a new one. Here's an explanation of the function:

    The function takes five arguments:
        exporter_name: The name of the exporter being processed.
        existing_yaml_output: The YAML data loaded from the existing output file.
        new_entries: A list of new entries that need to be added to the YAML data.
        yaml_output: The YAML data that has been generated by processing the input file.
        output_path: The path to the output file where the YAML data should be written.

    Check if there are any new entries to be added to the YAML data:
        If there are new entries, call the write_yaml function to merge the existing YAML data and the newly generated YAML data, and write the result to the output file. Then, print a completion message for the exporter with the total number of hosts processed.
        If there are no new entries, print a completion message for the exporter, indicating that there is nothing to do.

The purpose of this function is to handle the final step in the exporter processing pipeline, where the YAML data is written to a file. It checks if there are new entries to be added and writes the data accordingly, providing feedback about the progress and completion of the exporter processing.




load_existing_yaml:

The load_existing_yaml function is responsible for loading the YAML data from an existing output file, if it exists. Here's an explanation of the function:

    The function takes one argument, output_path, which is the path to the output file containing the existing YAML data.

    Check if the output file exists at the specified path using os.path.exists(output_path).

    If the output file exists:
        Open the file in read mode using a with statement and open(output_path, 'r') as f. This ensures that the file is closed properly after reading the contents.
        Use the yaml.safe_load(f) function to safely load the YAML data from the file. Assign the loaded data to the variable existing_yaml_output.
        Return the loaded YAML data if it is not None. If it is None, return an empty dictionary (indicating that there is no existing YAML data).

    If the output file does not exist, return an empty dictionary (indicating that there is no existing YAML data).

In summary, this function checks if the specified output file exists, and if so, loads the existing YAML data from it. If the file does not exist or the loaded data is None, an empty dictionary is returned. This ensures that the existing data can be merged with the newly generated data before writing the result to the output file.





ip_exists_in_yaml:

The ip_exists_in_yaml function checks if a given IP address already exists in the YAML file for a specific exporter. Here's an explanation of the function:

    The function takes three arguments: exporter_name, ip_address, and output_path. The exporter_name is the name of the exporter (e.g., 'exporter_linux', 'exporter_windows'), ip_address is the IP address you want to check for, and output_path is the path to the output YAML file.

    Check if the output YAML file exists at the specified path using os.path.exists(output_path). If it doesn't exist, return False to indicate that the IP address doesn't exist in the YAML file.

    If the YAML file exists:
        Open the file in read mode using a with statement and open(output_path, 'r') as f. This ensures that the file is closed properly after reading the contents.
        Use the yaml.safe_load(f) function to safely load the YAML data from the file. Assign the loaded data to the variable yaml_output.
        If the loaded YAML data (yaml_output) is not None and the exporter name is present in the YAML data (exporter_name in yaml_output), proceed to step 4. Otherwise, return False.

    Iterate through the IP data in the YAML data using a for loop: for hostname, ip_data in yaml_output[exporter_name].items(). For each hostname and its corresponding IP data:
        Check if the IP address is present in the IP data using 'ip_address' in ip_data. If the IP address is present and matches the given IP address (ip_data['ip_address'] == ip_address), return True to indicate that the IP address exists in the YAML file.

    If the IP address is not found in the YAML data, return False.

In summary, this function checks if a given IP address is already present in the YAML data for a specific exporter. If the IP address exists, it returns True. Otherwise, it returns False.




write_yaml:

The write_yaml function updates the existing YAML data with new entries and writes the updated data back to the file. Here's an explanation of the function:

    The function takes three arguments: existing_yaml_output, yaml_output, and output_path. The existing_yaml_output is a dictionary representing the existing YAML data, yaml_output is a dictionary containing the new data to be added, and output_path is the path to the output YAML file.

    Update the existing YAML data with the new entries:
        Iterate through the key-value pairs in the new YAML data (yaml_output) using a for loop: for key, value in yaml_output.items().
        Check if the key is not in the existing YAML data (key not in existing_yaml_output). If the key is not present, create a new empty dictionary for that key in the existing YAML data: existing_yaml_output[key] = {}.
        Update the existing YAML data for the current key with the new value using existing_yaml_output[key].update(value).

    Write the updated YAML data back to the file:
        Open the output file in write mode using a with statement and open(output_path, 'w') as f. This ensures that the file is closed properly after writing the contents.
        Use the yaml.dump(existing_yaml_output, f) function to write the updated YAML data (existing_yaml_output) to the file.

In summary, this function merges the new YAML data with the existing YAML data and writes the updated data back to the output file.



MAIN SECTION

    run_exporters(): This function runs the selected exporters based on the user's input. It first validates the input fields and checks if at least one exporter is selected. If "all" is selected, it runs all the exporters using the run_scripts function. Otherwise, it runs each selected exporter individually.

    browse_file_path(): This function opens a file dialog to browse for the CSV input file and updates the file path entry in the GUI.

    browse_output_dir(): This function opens a directory dialog to browse for the output directory and updates the output directory entry in the GUI.

    redirect_stdout(): This function redirects the standard output and standard error to a Tkinter text widget, allowing the output to be displayed in the GUI.

    StdoutRedirector: This class is used to redirect the standard output and standard error to a Tkinter text widget.

    The Tkinter GUI window is created using tk.Tk(), and various Tkinter widgets are created and placed on the window using the grid() method. This includes labels, entries, buttons, checkbuttons, a canvas, and a scrollbar.

    create_exporter_checkbuttons(): This function creates a checkbutton for each exporter and a "Select All" checkbutton that toggles the selection of all exporters.

    Tooltips are created for various widgets in the GUI, providing helpful information to the user.

    Finally, the mainloop() method is called 
    
![Screenshot from 2023-04-06 18-45-14](https://user-images.githubusercontent.com/6543166/230456734-28f14714-64cf-4910-ac2c-473134bd3fdb.png)
![Screenshot from 2023-04-06 18-47-03](https://user-images.githubusercontent.com/6543166/230456323-046f9a8e-8ca5-49af-86b7-96d7ce426324.png)
![Screenshot from 2023-04-06 18-47-55](https://user-images.githubusercontent.com/6543166/230456534-9058dad6-9d88-4958-bc8e-12638f1f70cc.png)
