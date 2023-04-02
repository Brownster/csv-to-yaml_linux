import tkinter as tk
from tkinter import filedialog, messagebox, END, ttk
from tkinter.scrolledtext import ScrolledText as Text
import sys
import pandas as pd
import yaml
import os

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
            
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, str):
        self.text_widget.insert(END, str)
        self.text_widget.see(END)

    def flush(self):
        pass

global listen_port_var
output_path = None
selected_exporter_names = []

################  EXPORTER_SM  ###########################

def exporter_sm(file_path, output_file, output_dir):
    global listen_port_var
    global output_path
    try:
        print("Exporter SM called")

        # Check if file is CSV or Excel
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.csv':
            # Read CSV file into pandas
            df = pd.read_csv(file_path, skiprows=7)
        elif file_extension in ['.xlsx', '.xls']:
            # Read Excel file into pandas
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Invalid file type. Only CSV and Excel files are supported.")
    except Exception as e:
        print(f"Error: {e}")
        print("Exporter SM failed")
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


###############LINUX#########################

def exporter_linux(file_path, output_file, output_dir):
    global default_listen_port
    global output_path
    try:
        print("Exporter converter_linux called")

        # Check if file is CSV or Excel
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.csv':
            # Read CSV file into pandas DataFrame, skip first 7 rows
            df = pd.read_csv(file_path, skiprows=7)
        elif file_extension in ['.xlsx', '.xls']:
            # Read Excel file into pandas DataFrame, start on row 8
            df = pd.read_excel(file_path, sheet_name='Sheet1', header=8)
        else:
            raise ValueError("Invalid file type. Only CSV and Excel files are supported.")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Filter the data based on the condition
    df_filtered = df[df['Exporter_name_os'] == 'exporter_linux']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Check if output file already exists
    output_path = os.path.join(output_dir, output_file)
    if os.path.exists(output_path):
        with open(output_path, 'r') as f:
            existing_yaml = yaml.load(f, Loader=yaml.FullLoader)
    else:
        existing_yaml = {}

    # Initialize exporter_linux key in the YAML dictionary
    if 'exporter_linux' not in existing_yaml:
        existing_yaml['exporter_linux'] = {}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df_filtered.iterrows():
        exporter_name = 'exporter_linux'
        fqdn = row['FQDN']
        ip_address = row['IP Address']

        # Check if IP address already exists in the output dictionary
        if ip_exists_in_yaml(exporter_name, ip_address, output_path=output_path):
            continue

        if pd.isnull(row.get('OS-Listen-Port')):
            listen_port = default_listen_port
            default_listen_port += 1
        else:
            listen_port = int(row['OS-Listen-Port'])

        location = row['Location']
        country = row['Country']
        username = 'your_username_here'
        password = 'your_password_here'

        if fqdn not in existing_yaml[exporter_name]:
            existing_yaml[exporter_name][fqdn] = {}
        existing_yaml[exporter_name][fqdn] = {
            'ip_address': ip_address,
            'listen_port': listen_port,
            'location': location,
            'username': username,
            'password': password,
            'country': country
        }

        new_entries.append(row)

    # Write the YAML data to a file
    with open(output_path, 'w') as f:
        yaml.dump(existing_yaml, f, sort_keys=False)

    # Iterate over rows in filtered dataframe to remove duplicates from the original CSV file
    for index, row in df_filtered.iterrows():
        exporter_name = 'exporter_linux'
        ip_address = row['IP Address']

        if ip_exists_in_yaml(exporter_name, ip_address, output_path=output_path):
            # Remove the row from the filtered DataFrame
            df_filtered = df_filtered.drop(index)

# Write the filtered data to a new CSV file
    filtered_csv_path = os.path.join(output_dir, 'filtered_exporter_linux.csv')
    df_filtered.to_csv(filtered_csv_path, index=False)

    # Print summary information
    if new_entries:
        print(f"Total number of hosts processed: {len(new_entries)}")
        print("Exporter converter_linux completed")
    else:
        print("Exporter converter_linux completed - nothing to do")

#################  BlackBox  ##################

def exporter_blackbox(file_path, output_file, output_dir):
    print("Exporter converter_blackbox called")
    
    # Define the output_path at the beginning of the function
    output_path = os.path.join(output_dir, output_file)

    # Check if file is CSV or Excel
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == '.csv':
        # Read CSV file into pandas
        df = pd.read_csv(file_path, skiprows=7)
    elif file_extension in ['.xlsx', '.xls']:
        # Read Excel file into pandas
        df = pd.read_excel(file_path, sheet_name='Sheet1')
    else:
        raise ValueError("Invalid file type. Only CSV and Excel files are supported.")

    # Filter rows based on condition
    df = df[(df['icmp'] == True) & (df['ssh-banner'] == True)]

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_blackbox key in the YAML dictionary
    yaml_output['exporter_blackbox'] = {}

    # Check if optional headers are present
    ssh_username_present = 'ssh_username' in df.columns
    ssh_password_present = 'ssh_password' in df.columns

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df.iterrows():
        exporter_name = 'exporter_blackbox'
        hostname = row['Hostnames']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if ip_exists_in_yaml(exporter_name, ip_address, output_path=output_path):
            continue

        if hostname not in yaml_output.get(exporter_name, {}):
             yaml_output[exporter_name][hostname] = {}
    
        if ip_address not in yaml_output[exporter_name][hostname]:
             yaml_output[exporter_name][hostname][ip_address] = {}
        
        yaml_output[exporter_name][hostname][ip_address]['location'] = location
        yaml_output[exporter_name][hostname][ip_address]['country'] = country
    
        if row['icmp']:
            yaml_output[exporter_name][hostname][ip_address]['module'] = 'icmp'
        
        if row['ssh-banner']:
            ssh_ip_address = f"{ip_address}:22"
            if ip_exists_in_yaml(exporter_name, ssh_ip_address, output_path=output_path):
                continue
            yaml_output[exporter_name][hostname][ssh_ip_address] = {
                'module': 'ssh_banner',
                'location': location,
                'country': country
            }
            if ssh_username_present and not pd.isna(row['ssh_username']):
                yaml_output[exporter_name][hostname][ssh_ip_address]['username'] = row['ssh_username']
            else:
                yaml_output[exporter_name][hostname][ssh_ip_address]['username'] = 'root'

            if ssh_password_present and not pd.isna(row['ssh_password']):
                yaml_output[exporter_name][hostname][ssh_ip_address]['password'] = row['ssh_password']
            else:
                yaml_output[exporter_name][hostname][ssh_ip_address]['password'] = 'ENC'

        new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    output_path = os.path.join(output_dir, output_file)
    if new_entries:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
        print("Exporter converter_blackbox completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter converter_blackbox completed - nothing to do")


###################SSL####################

def exporter_ssl(file_path, output_file, output_dir):
    try:
        print("Exporter SSL called")

        # Check if file is CSV or Excel
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.csv':
            # Read CSV file into pandas
            df = pd.read_csv(file_path, skiprows=7)
        elif file_extension in ['.xlsx', '.xls']:
            # Read Excel file into pandas
            df = pd.read_excel(file_path, sheet_name='Sheet2', skiprows=7)
        else:
            raise ValueError("Invalid file type. Only CSV and Excel files are supported.")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Filter the data based on the condition
    df_filtered = df[df['Exporter_SSL'] == True]

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_cms key in the YAML dictionary
    yaml_output['exporter_ssl'] = {}

    output_path = os.path.join(output_dir, output_file)

    # Counter to keep track of the number of lines processed
    processed_lines = 0

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

        # Increment the processed lines counter
        processed_lines += 1

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if yaml_output['exporter_ssl']:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
        print("Exporter SSL completed")
        print(f"Total number of hosts processed: {processed_lines}")
    else:
        print("Exporter SSL completed - nothing to do")


################CMS#######################


def exporter_cms(file_path, output_file, output_dir):
    global default_listen_port
    global output_path
    try:
        print("Exporter CMS called")

        # Check if file is CSV or Excel
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.csv':
            # Read CSV file into pandas
            df = pd.read_csv(file_path, skiprows=7)
        elif file_extension in ['.xlsx', '.xls']:
            # Read Excel file into pandas
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Invalid file type. Only CSV and Excel files are supported.")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Filter rows based on condition
    df_filtered = df[df['Exporter_name_app'] == 'exporter_cms']

    # Check if optional headers are present
    ssh_username_present = 'ssh_username' in df.columns
    ssh_password_present = 'ssh_password' in df.columns

    output_path = os.path.join(output_dir, output_file)

    # Initialize exporter_cms key in the YAML dictionary
    yaml_output = {'exporter_cms': {}}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df_filtered.iterrows():
        exporter_name = 'exporter_cms'
        hostname = row['Hostnames']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if ip_exists_in_yaml(exporter_name, ip_address, output_path=output_path):
            continue

        if hostname not in yaml_output[exporter_name]:
            yaml_output[exporter_name][hostname] = {}

        # Use default_listen_port if 'App-Listen-Port' is not available
        listen_port = row.get('App-Listen-Port', default_listen_port)
        if listen_port == default_listen_port:
            default_listen_port += 1

        yaml_output[exporter_name][hostname]['ip_address'] = ip_address
        yaml_output[exporter_name][hostname]['listen_port'] = listen_port
        yaml_output[exporter_name][hostname]['location'] = location
        yaml_output[exporter_name][hostname]['country'] = country

        # Use the values from the optional headers if present, otherwise use the placeholders
        if ssh_username_present and not pd.isna(row['ssh_username']):
            yaml_output[exporter_name][hostname]['username'] = row['ssh_username']
        else:
            yaml_output[exporter_name][hostname]['username'] = 'root'

        if ssh_password_present and not pd.isna(row['ssh_password']):
            yaml_output[exporter_name][hostname]['password'] = row['ssh_password']
        else:
            yaml_output[exporter_name][hostname]['password'] = 'ENC'

        new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if new_entries:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
        print("Exporter CMS completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter CMS completed - nothing to do")

##################WINDOWS###################

def exporter_windows(file_path, output_file, output_dir):
    global output_path
    
    try:
        print("Exporter Windows called")

        # Check if file is CSV or Excel
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.csv':
            # Read CSV file into pandas
            df = pd.read_csv(file_path, skiprows=7)
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

         
 ##############VERINT###########################

def exporter_verint(file_path, output_file, output_dir):
    global default_listen_port
    global output_path
    try:
        print("Exporter Verint called")

        # Check if file is CSV or Excel
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.csv':
            # Read CSV file into pandas
            df = pd.read_csv(file_path, skiprows=7)
        elif file_extension in ['.xlsx', '.xls']:
            # Read Excel file into pandas
            df = pd.read_excel(file_path, sheet_name='Sheet2')
        else:
            raise ValueError("Invalid file type. Only CSV and Excel files are supported.")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Filter rows based on condition
    df_filtered = df[df['Exporter_name_app'] == 'exporter_verint']

    output_path = os.path.join(output_dir, output_file)

    # Initialize exporter_verint key in the YAML dictionary
    yaml_output = {'exporter_verint': {}}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df_filtered.iterrows():
        exporter_name = 'exporter_verint'
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if ip_exists_in_yaml(exporter_name, ip_address, output_path=output_path):
            continue

        if hostname not in yaml_output[exporter_name]:
            yaml_output[exporter_name][hostname] = {}

        if ip_address not in yaml_output[exporter_name][hostname]:
            yaml_output[exporter_name][hostname][ip_address] = {}

        # Use default_listen_port if 'App-Listen-Port' is not available
        listen_port = row.get('App-Listen-Port', default_listen_port)
        if listen_port == default_listen_port:
            default_listen_port += 1

        yaml_output[exporter_name][hostname][ip_address]['listen_port'] = listen_port
        yaml_output[exporter_name][hostname][ip_address]['location'] = location
        yaml_output[exporter_name][hostname][ip_address]['country'] = country
        yaml_output[exporter_name][hostname][ip_address]['username'] = 'ipcs'

        new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if new_entries:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
        print("Exporter Verint completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter Verint completed - nothing to do")
          
            
            
##################AVAYA SBC###########################

def exporter_avayasbc(file_path, output_file, output_dir):
    global default_listen_port
    global output_path
    try:
        print("Exporter Avaya SBC called")

        # Check if file is CSV or Excel
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.csv':
            # Read CSV file into pandas
            df = pd.read_csv(file_path, skiprows=7)
        elif file_extension in ['.xlsx', '.xls']:
            # Read Excel file into pandas, starting from row 3
            df = pd.read_excel(file_path, sheet_name='Sheet2', header=2, skiprows=[0, 1])
        else:
            raise ValueError("Invalid file type. Only CSV and Excel files are supported.")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Filter rows based on condition
    df_filtered = df[df['Exporter_name_app'] == 'exporter_sbc']

    output_path = os.path.join(output_dir, output_file)

    # Initialize exporter_avayasbc key in the YAML dictionary
    yaml_output = {'exporter_avayasbc': {}}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df_filtered.iterrows():
        exporter_name = 'exporter_avayasbc'
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if ip_exists_in_yaml(exporter_name, ip_address, output_path=output_path):
            continue

        if hostname not in yaml_output[exporter_name]:
            yaml_output[exporter_name][hostname] = {}

        if ip_address not in yaml_output[exporter_name][hostname]:
            yaml_output[exporter_name][hostname][ip_address] = {}

            yaml_output[exporter_name][hostname][ip_address]['listen_port'] = 3601
            yaml_output[exporter_name][hostname][ip_address]['location'] = location
            yaml_output[exporter_name][hostname][ip_address]['country'] = country
            yaml_output[exporter_name][hostname][ip_address]['username'] = 'ipcs'

            new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if new_entries:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
        print("Exporter Avaya SBC completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter Avaya SBC completed - nothing to do")


 
######################GATEWAY###############

def exporter_gateway(file_path, output_file, output_dir):
    global default_listen_port
    global output_path
    try:
        print("Exporter Gateway called")

        # Check if file is CSV or Excel
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.csv':
            # Read CSV file into pandas
            df = pd.read_csv(file_path, skiprows=7)
        elif file_extension in ['.xlsx', '.xls']:
            # Read Excel file into pandas
            df = pd.read_excel(file_path, sheet_name='Sheet2')
        else:
            raise ValueError("Invalid file type. Only CSV and Excel files are supported.")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Filter rows based on condition
    df_filtered = df[df['Exporter_name_app'] == 'exporter_gateway']

    output_path = os.path.join(output_dir, output_file)

    # Initialize exporter_gateway key in the YAML dictionary
    yaml_output = {'exporter_gateway': {}}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df_filtered.iterrows():
        exporter_name = 'exporter_gateway'
        hostname = row['Hostnames']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if ip_exists_in_yaml(exporter_name, ip_address, output_path=output_path):
            continue

        if hostname not in yaml_output[exporter_name]:
            yaml_output[exporter_name][hostname] = {}

        if ip_address not in yaml_output[exporter_name][hostname]:
            yaml_output[exporter_name][hostname][ip_address] = {}

        if pd.isna(row['App-Listen-Port']):
            yaml_output[exporter_name][hostname][ip_address]['listen_port'] = int(default_listen_port.get())
        else:
            yaml_output[exporter_name][hostname][ip_address]['listen_port'] = int(row['App-Listen-Port'])

        yaml_output[exporter_name][hostname][ip_address]['location'] = location
        yaml_output[exporter_name][hostname][ip_address]['country'] = country
        yaml_output[exporter_name][hostname][ip_address]['snmp_version'] = 2

        if 'comm_string' in df.columns and not pd.isna(row['comm_string']):
            yaml_output[exporter_name][hostname][ip_address]['community'] = row['comm_string']
        else:
            yaml_output[exporter_name][hostname][ip_address]['community'] = 'ENC'

        new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if new_entries:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
        print("Exporter Gateway completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter Gateway completed - nothing to do")


#################BREEZE##############

def exporter_breeze(file_path, output_file, output_dir):
    global default_listen_port
    global output_path
    try:
        print("Exporter Breeze called")

        # Check if file is CSV or Excel
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.csv':
        # Read CSV file into pandas           
            df = pd.read_csv(file_path, skiprows=7)
        elif file_extension in ['.xlsx', '.xls']:
            # Read Excel file into pandas
            df = pd.read_excel(file_path, sheet_name='Sheet2')
        else:
            raise ValueError("Invalid file type. Only CSV and Excel files are supported.")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Filter rows based on condition
    df_filtered = df[df['Exporter_name_app'] == 'exporter_breeze']

    output_path = os.path.join(output_dir, output_file)


    # Define ip_address variable outside the if block
    ip_address = None

    # Check if optional headers are present
    ssh_username_present = 'ssh_username' in df.columns
    ssh_password_present = 'ssh_password' in df.columns

    # Initialize exporter_breeze key in the YAML dictionary
    yaml_output = {'exporter_breeze': {}}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df_filtered.iterrows():
        exporter_name = 'exporter_breeze'
        hostname = row['Hostnames']
        # Assign ip_address to the current row
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if ip_exists_in_yaml(exporter_name, ip_address, output_path=output_path):
            continue

        if hostname not in yaml_output[exporter_name]:
            yaml_output[exporter_name][hostname] = {}

        if ip_address not in yaml_output[exporter_name][hostname]:
            yaml_output[exporter_name][hostname][ip_address] = {}

        if pd.isna(row['App-Listen-Port']):
            yaml_output[exporter_name][hostname][ip_address]['listen_port'] = int(default_listen_port.get())
        else:
            yaml_output[exporter_name][hostname][ip_address]['listen_port'] = int(row['App-Listen-Port'])
        # Use the values from the optional headers if present, otherwise use the placeholders
        if ssh_username_present and not pd.isna(row['ssh_username']):
            yaml_output[exporter_name][hostname][ip_address]['username'] = row['ssh_username']
        else:
            yaml_output[exporter_name][hostname][ip_address]['username'] = 'root'

        if ssh_password_present and not pd.isna(row['ssh_password']):
            yaml_output[exporter_name][hostname][ip_address]['password'] = row['ssh_password']
        else:
            yaml_output[exporter_name][hostname][ip_address]['password'] = 'ENC'
        
        yaml_output[exporter_name][hostname][ip_address]['location'] = location
        yaml_output[exporter_name][hostname][ip_address]['country'] = country
        
        new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if new_entries:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
        print("Exporter breeze completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter Breeze completed - nothing to do")

######## EXPORTER_JMX ############
def exporter_jmx(file_path, output_file, output_dir):
    global default_listen_port
    global output_path
    try:
        print("Exporter Breeze called")

        # Check if file is CSV or Excel
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.csv':
        # Read CSV file into pandas           
            df = pd.read_csv(file_path, skiprows=7)
        elif file_extension in ['.xlsx', '.xls']:
            # Read Excel file into pandas
            df = pd.read_excel(file_path, sheet_name='Sheet2')
        else:
            raise ValueError("Invalid file type. Only CSV and Excel files are supported.")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_jmx']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_jmx key in the YAML dictionary
    yaml_output['exporter_jmx'] = {}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df.iterrows():
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        output_path = os.path.join(output_dir, output_file)
        if ip_exists_in_yaml('exporter_jmx', ip_address, output_path=output_path):
            continue

        if hostname not in yaml_output.get('exporter_jmx', {}):
            yaml_output['exporter_jmx'][hostname] = {}

        jmx_ports = row.get('jmx_ports', None)
        if jmx_ports is None:
            ports = [8081, 8082]
        else:
            ports = [int(port) for port in jmx_ports.split(',')]

        for port in ports:
            if port not in yaml_output['exporter_jmx'][hostname]:
                yaml_output['exporter_jmx'][hostname][str(port)] = {}

            yaml_output['exporter_jmx'][hostname][str(port)]['ip_address'] = ip_address
            yaml_output['exporter_jmx'][hostname][str(port)]['location'] = location
            yaml_output['exporter_jmx'][hostname][str(port)]['country'] = country

        new_entries.append(row)

    # Write the YAML data to a file
    new_entries_count = len(new_entries)
    if new_entries_count:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f, default_flow_style=False)
        print("Exporter JMX completed")
    else:
        print("Exporter JMX completed - nothing to do")
    print(f"Total number of hosts processed: {new_entries_count}")

############ EXPORTER_VMWARE #######################

def exporter_vmware(file_path, output_file, output_dir):
    # Read CSV file into pandas           
    df = pd.read_csv(file_path, skiprows=7)


    # Filter rows based on condition
    df_filtered = df[df['Exporter_name_app'] == 'exporter_vmware']

    # Define output path
    output_path = os.path.join(output_dir, output_file)

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_vmware key in the YAML dictionary
    yaml_output['exporter_vmware'] = {}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df_filtered.iterrows():
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if ip_exists_in_yaml('exporter_vmware', ip_address, output_path=output_path):
            continue

        if hostname not in yaml_output['exporter_vmware']:
            yaml_output['exporter_vmware'][hostname] = {}

        if pd.isna(row['App-Listen-Port']):
            yaml_output['exporter_vmware'][hostname]['listen_port'] = 9272
        else:
            yaml_output['exporter_vmware'][hostname]['listen_port'] = int(row['App-Listen-Port'])

        yaml_output['exporter_vmware'][hostname]['ip_address'] = ip_address
        yaml_output['exporter_vmware'][hostname]['location'] = location
        yaml_output['exporter_vmware'][hostname]['country'] = country
        yaml_output['exporter_vmware'][hostname]['username'] = 'put your username here'
        yaml_output['exporter_vmware'][hostname]['password'] = 'put your password here'

        new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if new_entries:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f, default_flow_style=False)
        print("Exporter VMware completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter VMware completed - nothing to do")

#################### EXPORTER_KAFKA ################


import os
import pandas as pd

def exporter_kafka(file_path, output_file, output_dir):
    global output_path

    try:
        print("Exporter Kafka called")

        # Check if file is CSV or Excel
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.csv':
            # Read CSV file into pandas
            df = pd.read_csv(file_path, skiprows=7)
        elif file_extension in ['.xlsx', '.xls']:
            # Read Excel file into pandas
            df = pd.read_excel(file_path, sheet_name='Sheet2', skiprows=7)
        else:
            raise ValueError("Invalid file type. Only CSV and Excel files are supported.")
    except Exception as e:
        print(f"Error: {e}")
        return

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

        output_path = os.path.join(output_dir, output_file)
        if ip_exists_in_yaml('exporter_kafka', ip_address, output_path=output_path):
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
    new_entries_count = len(new_entries)
    if new_entries_count:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f, default_flow_style=False)
        print("Exporter Kafka completed")
    else:
        print("Exporter Kafka completed - nothing to do")
    print(f"Total number of hosts processed: {new_entries_count}")


########## EXPORTER_CALLBACK ################################

def exporter_callback(file_path, output_file, output_dir):
    # Read CSV file into pandas           
    df = pd.read_csv(file_path, skiprows=7)


    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_callback']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_callback key in the YAML dictionary
    yaml_output['exporter_callback'] = {}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df.iterrows():
        exporter_name = 'exporter_callback'
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if ip_exists_in_yaml(exporter_name, ip_address, output_dir, output_file):
            continue

        if hostname not in yaml_output.get('exporter_callback', {}):
            yaml_output['exporter_callback'][hostname] = {}

        if pd.isna(row['App-Listen-Port']):
            listen_port = default_listen_port.get()
        else:
            listen_port = int(row['App-Listen-Port'])

        yaml_output['exporter_callback'][hostname]['ip_address'] = ip_address
        yaml_output['exporter_callback'][hostname]['listen_port'] = listen_port
        yaml_output['exporter_callback'][hostname]['location'] = location
        yaml_output['exporter_callback'][hostname]['country'] = country

        # Check if optional headers are present
        ssh_username_present = 'ssh_username' in df.columns
        ssh_password_present = 'ssh_password' in df.columns

        # Use the values from the optional headers if present, otherwise use the placeholders
        if ssh_username_present and not pd.isna(row['ssh_username']):
            yaml_output['exporter_callback'][hostname]['username'] = row['ssh_username']
        else:
            yaml_output['exporter_callback'][hostname]['username'] = 'maas'

        if ssh_password_present and not pd.isna(row['ssh_password']):
            yaml_output['exporter_callback'][hostname]['password'] = row['ssh_password']
        else:
            yaml_output['exporter_callback'][hostname]['password'] = 'ENC'

        new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if new_entries:
        output_path = os.path.join(output_dir, output_file)
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f, default_flow_style=False)
        print("Exporter Callback completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter Callback completed - nothing to do")


########## EXPORTER_DRAC ############

def exporter_drac(file_path, output_file, output_dir):
    # Read CSV file into pandas           
    df = pd.read_csv(file_path, skiprows=7)


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


############ exporter_genesyscloud ########################

import os
import pandas as pd
import yaml

def exporter_genesyscloud(file_path, output_file, output_dir):
    # Read CSV file into pandas           
    df = pd.read_csv(file_path, skiprows=7)


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


############# EXPORTER_ACM ###############

def exporter_acm(file_path, output_file, output_dir, default_listen_port=8081):
    print("Exporter ACM called")

    # Read CSV file into pandas           
    df = pd.read_csv(file_path, skiprows=7)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_acm']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_acm key in the YAML dictionary
    yaml_output['exporter_acm'] = {}

    # Iterate over rows in filtered dataframe
    new_entries = []
    
    # Create output_path
    output_path = os.path.join(output_dir, output_file)
    
    for index, row in df.iterrows():
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
        listen_port = row['App-Listen-Port']
        ssh_username = row.get('ssh_username', 'put your username here')
        ssh_password = row.get('ssh_password', 'put your password here')

        if ip_exists_in_yaml('exporter_acm', ip_address, output_path=output_path):
            print(f"IP {ip_address} already exists in the YAML file.")
            continue

        if hostname not in yaml_output.get('exporter_acm', {}):
            yaml_output['exporter_acm'][hostname] = {}

        yaml_output['exporter_acm'][hostname]['ip_address'] = ip_address
        yaml_output['exporter_acm'][hostname]['listen_port'] = int(listen_port) if not pd.isna(listen_port) else int(default_listen_port)
        if 'lsp' in hostname.lower():
            yaml_output['exporter_acm'][hostname]['type'] = 'lsp'
        elif 'ess' in hostname.lower():
            yaml_output['exporter_acm'][hostname]['type'] = 'ess'
        else:
            yaml_output['exporter_acm'][hostname]['type'] = 'acm'
        yaml_output['exporter_acm'][hostname]['location'] = location
        yaml_output['exporter_acm'][hostname]['country'] = country
        yaml_output['exporter_acm'][hostname]['username'] = ssh_username
        yaml_output['exporter_acm'][hostname]['password'] = ssh_password

        new_entries.append(row)

    # Write the YAML data to a file
    if new_entries:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f, default_flow_style=False)
            print(f"Exporter ACM completed")
            print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter ACM completed - nothing to do")



############# WEBLM_EXPORTER ##########

def exporter_weblm(file_path, output_file, output_dir, default_listen_port=8081):
    # Read CSV file into pandas           
    df = pd.read_csv(file_path, skiprows=7)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_weblm']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_weblm key in the YAML dictionary
    yaml_output['exporter_weblm'] = {}

    # Iterate over rows in filtered dataframe
    new_entries = []
    for index, row in df.iterrows():
        hostname = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
        listen_port = row['App-Listen-Port']
        ssh_username = row.get('ssh_username', 'put your username here')
        ssh_password = row.get('ssh_password', 'put your password here')

        if ip_exists_in_yaml('exporter_weblm', ip_address, output_dir=output_dir, output_file=output_file):
            continue

        if hostname not in yaml_output.get('exporter_weblm', {}):
            yaml_output['exporter_weblm'][hostname] = {}

        yaml_output['exporter_weblm'][hostname]['ip_address'] = ip_address
        yaml_output['exporter_weblm'][hostname]['listen_port'] = int(listen_port) if not pd.isna(listen_port) else int(default_listen_port)
        yaml_output['exporter_weblm'][hostname]['location'] = location
        yaml_output['exporter_weblm'][hostname]['country'] = country
        yaml_output['exporter_weblm'][hostname]['data_path'] = '/opt/Avaya/tomcat/webapps/WebLM/data/'
        yaml_output['exporter_weblm'][hostname]['username'] = ssh_username
        yaml_output['exporter_weblm'][hostname]['password'] = ssh_password

        new_entries.append(row)


####### check if exists in yaml section ########
    # Write the YAML data to a file
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w') as f:
        yaml.dump(yaml_output, f, default_flow_style=False)
        print(f"Exporter WebLM completed")
        print(f"Total number of hosts processed: {len(new_entries)}")


def ip_exists_in_yaml(exporter_name, ip_address, output_path):
    """
    Check if the given IP address already exists in the YAML file for the given exporter
    """
    if not os.path.exists(output_path):
        return False

    with open(output_path, 'r') as f:
        yaml_output = yaml.safe_load(f)
        if yaml_output is not None and exporter_name in yaml_output:
            for hostname, ip_data in yaml_output[exporter_name].items():
                if ip_address in ip_data:
                    return True
    return False


################## MAIN SECTION ###################
def run_exporters():
    global default_listen_port

    # Get the file path
    file_path = file_path_entry.get()

    # Get the output file name
    output_file = output_file_entry.get()

    # Get the output directory
    output_dir = output_dir_entry.get()

    # Get the starting value for the listen port
    try:
        default_listen_port = int(listen_port_var.get())
    except ValueError:
        messagebox.showerror('Error', 'Please enter a valid starting value for the listen port')
        return

    # Get the selected exporter names
    selected_exporter_names = [name for name, var in zip(exporter_names, exporter_vars) if var.get()]

    # Validate inputs
    if not file_path or not output_file or not output_dir:
        messagebox.showerror('Error', 'Please enter all fields')
        return

    # Check if any exporters were selected
    if not selected_exporter_names:
        messagebox.showerror('Error', 'Please select at least one exporter')
        return

    # Run selected exporters
    if 'all' in selected_exporter_names:
        run_scripts(['exporter_linux', 'exporter_blackbox', 'exporter_breeze', 'exporter_sm', 'exporter_avayasbc', 'exporter_gateway', 'exporter_verint', 'exporter_windows', 'exporter_ssl', 'exporter_cms', 'exporter_acm', 'exporter_jmx', 'exporter_weblm', 'exporter_vmware', 'exporter_kafka', 'exporter_callback', 'exporter_drac', 'exporter_genesyscloud'], file_path, output_file, output_dir)
    else:
        for exporter_name in selected_exporter_names:
            if exporter_name == 'exporter_linux':
                exporter_linux(file_path, output_file, output_dir)
            elif exporter_name == 'exporter_blackbox':
                exporter_blackbox(file_path, output_file, output_dir)
            elif exporter_name == 'exporter_ssl':
                exporter_ssl(file_path, output_file, output_dir)
            elif exporter_name == 'exporter_cms':
                exporter_cms(file_path, output_file, output_dir)
            elif exporter_name == 'exporter_windows':
                exporter_windows(file_path, output_file, output_dir)
            elif exporter_name == 'exporter_avayasbc':
                exporter_avayasbc(file_path, output_file, output_dir)
            elif exporter_name == 'exporter_verint':
                exporter_verint(file_path, output_file, output_dir)
            elif exporter_name == 'exporter_gateway':
                exporter_gateway(file_path, output_file, output_dir) 
            elif exporter_name == 'exporter_breeze':
                exporter_breeze(file_path, output_file, output_dir) 
            elif exporter_name == 'exporter_sm':
                exporter_sm(file_path, output_file, output_dir) 
            elif exporter_name == 'exporter_acm':
                exporter_acm(file_path, output_file, output_dir)
            elif exporter_name == 'exporter_jmx':
                exporter_jmx(file_path, output_file, output_dir)
            elif exporter_name == 'exporter_weblm':
                exporter_weblm(file_path, output_file, output_dir)
            elif exporter_name == 'exporter_vmware':
                exporter_vmware(file_path, output_file, output_dir)
            elif exporter_name == 'exporter_kafka':
                exporter_kafka(file_path, output_file, output_dir)
            elif exporter_name == 'exporter_callback':
                exporter_callback(file_path, output_file, output_dir)
            elif exporter_name == 'exporter_drac':
                exporter_drac(file_path, output_file, output_dir)
            elif exporter_name == 'exporter_genesyscloud':
                exporter_genesyscloud(file_path, output_file, output_dir)

    # Show success message
    messagebox.showinfo('Success', 'Exporters completed')

def browse_file_path():
    file_path = filedialog.askopenfilename()
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

def browse_output_dir():
    output_dir = filedialog.askdirectory()
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(0, output_dir)


####  terminal window #########
def redirect_stdout():
    sys.stdout = StdoutRedirector(output_text)
    sys.stderr = StdoutRedirector(output_text)

class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, str):
        self.text_widget.insert(END, str)
        self.text_widget.see(END)

####### Create GUI window ######################
root = tk.Tk()
root.title('Exporters GUI')
root.geometry("800x500")
listen_port_var = tk.StringVar()
# create text widget to display output
output_text = Text(root)
output_text.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Define file_path_label, file_path_entry, and file_path_button before calling grid()
file_path_label = tk.Label(root, text='CSV File path:')
file_path_entry = tk.Entry(root)
file_path_button = tk.Button(root, text='Browse', command=browse_file_path)

file_path_label.grid(row=1, column=0, sticky='w', padx=10, pady=5)
file_path_entry.grid(row=1, column=1, sticky='we', padx=10, pady=5)
file_path_button.grid(row=1, column=2, sticky='e', padx=10, pady=5)

# Define output_file_label and output_file_entry before calling grid()
output_file_label = tk.Label(root, text='Yaml Output file name:')
output_file_entry = tk.Entry(root)

output_file_label.grid(row=2, column=0, sticky='w', padx=10, pady=5)
output_file_entry.grid(row=2, column=1, sticky='we', padx=10, pady=5)

# Define output_dir_label and output_dir_entry before calling grid()
output_dir_label = tk.Label(root, text='Yaml Output directory:')
output_dir_entry = tk.Entry(root)

output_dir_label.grid(row=3, column=0, sticky='w', padx=10, pady=5)
output_dir_entry.grid(row=3, column=1, sticky='we', padx=10, pady=5)

# Define listen_port_label, listen_port_entry, and listen_port_var before calling grid()
listen_port_label = tk.Label(root, text='Starting value for listen port:')
listen_port_entry = tk.Entry(root, textvariable=listen_port_var)

listen_port_label.grid(row=4, column=0, sticky='w', padx=10, pady=5)
listen_port_entry.grid(row=4, column=1, sticky='we', padx=10, pady=5)

def create_exporter_checkbuttons(frame):
    global exporter_names, exporter_vars

    num_rows = len(exporter_names) // 2 + len(exporter_names) % 2
    for index, name in enumerate(exporter_names):
        var = tk.BooleanVar()
        exporter_vars.append(var)
        checkbutton = tk.Checkbutton(frame, text=name, variable=var)
        checkbutton.grid(row=index % num_rows, column=index // num_rows, sticky='w')

    # Add a "Select All" checkbutton
    select_all_var = tk.BooleanVar()

    def toggle_select_all():
        for var in exporter_vars:
            var.set(select_all_var.get())

    select_all_checkbutton = tk.Checkbutton(frame, text="Select All", variable=select_all_var, command=toggle_select_all)
    select_all_checkbutton.grid(row=num_rows, column=0, columnspan=2, sticky='w')

# Define go_button before calling grid()
go_button = tk.Button(root, text='Go', command=run_exporters)
go_button.grid(row=5, column=2, pady=10, sticky='w')

exporter_names = ['exporter_linux', 'exporter_blackbox', 'exporter_breeze', 'exporter_avayasbc', 'exporter_gateway', 'exporter_verint', 'exporter_windows', 'exporter_sm', 'exporter_ssl', 'exporter_cms', 'exporter_acm', 'exporter_jmx', 'exporter_weblm', 'exporter_vmware', 'exporter_kafka', 'exporter_callback', 'exporter_drac', 'exporter_genesyscloud']

exporters = []
exporter_vars = []

# Create a frame for the exporter checkbuttons
exporter_frame = ttk.Frame(root)
exporter_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Create a canvas for the exporter checkbuttons
canvas = tk.Canvas(exporter_frame)
canvas.grid(row=0, column=0, sticky="nsew")

# Create a scrollbar for the canvas
scrollbar = ttk.Scrollbar(exporter_frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
canvas.config(yscrollcommand=scrollbar.set)

# Create an inner frame to hold the exporter checkbuttons
inner_exporter_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=inner_exporter_frame, anchor='nw')
inner_exporter_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a tooltip for the file_path_entry
file_path_tooltip = ToolTip(file_path_entry, "Enter the path to your CSV file")

# Create a tooltip for the file_path_button
file_path_button_tooltip = ToolTip(file_path_button, "Browse for the CSV file")

# Create a tooltip for the output_file_entry
output_file_tooltip = ToolTip(output_file_entry, "Enter the name of the output YAML file")

# Create a tooltip for the output_dir_entry
output_dir_tooltip = ToolTip(output_dir_entry, "Enter the directory where the output YAML file will be saved")

# Create a tooltip for the go_button
go_button_tooltip = ToolTip(go_button, "Run the selected exporters")

# Create tooltips for the exporter checkbuttons
for exporter, name in zip(exporters, exporter_names):
    tooltip_text = f"Select this option to run the {name} exporter"
    tooltip = ToolTip(exporter, tooltip_text)

# Call the function to create exporter checkbuttons
create_exporter_checkbuttons(inner_exporter_frame)

# Create a main loop to display the GUI window
redirect_stdout()
root.mainloop()
