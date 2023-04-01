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

