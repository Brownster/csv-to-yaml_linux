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



###############LINUX#########################

def exporter_linux(file_path, output_file, output_dir):
    global default_listen_port  # Access the global variable

    print("Exporter converter_linux called")
    # Read CSV file into pandas DataFrame
    df = pd.read_csv(file_path)

    # Filter the data based on the condition
    df_filtered = df[df['Exporter_name_os'] == 'exporter_linux']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_blackbox key in the YAML dictionary
    yaml_output['exporter_linux'] = {}

    # Loop through the filtered data and add to the dictionary
    for _, row in df_filtered.iterrows():
        exporter_name = 'exporter_linux'
        fqdn = row['FQDN']
        ip_address = row['IP Address']

        if pd.isnull(row.get('OS-Listen-Port')):
            listen_port = default_listen_port
            default_listen_port += 1
        else:
            listen_port = int(row['OS-Listen-Port'])

        location = row['Location']
        country = row['Country']
        username = 'your_username_here'
        password = 'your_password_here'

        if exporter_name not in yaml_output:
            yaml_output[exporter_name] = {}
        if fqdn not in yaml_output[exporter_name]:
            yaml_output[exporter_name][fqdn] = {}
        yaml_output[exporter_name][fqdn] = {
            'ip_address': ip_address,
            'listen_port': listen_port,
            'location': location,
            'country': country,
            'username': username,
            'password': password
        }

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)
    print("Exporter converter_linux completed")



#################BlackBox##################


def exporter_blackbox(file_path, output_file, output_dir):
    print("Exporter converter_blackbox called")
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[(df['icmp'] == True) & (df['ssh-banner'] == True)]

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_blackbox key in the YAML dictionary
    yaml_output['exporter_blackbox'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        exporter_name = 'exporter_blackbox'
        hostname = row['Hostnames']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
    
        if hostname not in yaml_output.get(exporter_name, {}):
             yaml_output[exporter_name][hostname] = {}
    
        if ip_address not in yaml_output[exporter_name][hostname]:
             yaml_output[exporter_name][hostname][ip_address] = {}
        
        yaml_output[exporter_name][hostname][ip_address]['location'] = location
        yaml_output[exporter_name][hostname][ip_address]['country'] = country
    
        if row['icmp']:
            yaml_output[exporter_name][hostname][ip_address]['module'] = 'icmp'
        
        if row['ssh-banner']:
            yaml_output[exporter_name][hostname][f'{ip_address}:22'] = {
                'module': 'ssh_banner',
                'location': location,
                'country': country
            }
    # Write the YAML data to a file, either appending to an existing file or creating a new file
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)
    print("Exporter converter_blackbox completed")



###################SSL####################


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

    # Loop through the filtered data and add to the dictionary
    for _, row in df_filtered.iterrows():
        exporter_name = 'exporter_ssl'
        fqdn = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
        listen_port = 443
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
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)
    print("Exporter converter_SSL completed")

################CMS#######################


def exporter_cms(file_path, output_file, output_dir):
    print("Exporter converter_CMS called")
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter the data based on the condition
    df_filtered = df[df['Exporter_name_app'] == 'exporter_cms']

    # Add new columns for username and password
    df['Username'] = 'root'
    df['Password'] = 'ENC'

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_cms key in the YAML dictionary
    yaml_output['exporter_cms'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        exporter_name = 'exporter_cms'
        hostname = row['Hostnames']
        ip_address = row['IP Address']
        listen_port = int(row['App-Listen-Port'])
        location = row['Location']
        country = row['Country']
        username = row['Username']
        password = row['Password']

        if hostname not in yaml_output.get(exporter_name, {}):
            yaml_output[exporter_name][hostname] = {}

        yaml_output[exporter_name][hostname]['ip_address'] = ip_address
        yaml_output[exporter_name][hostname]['listen_port'] = listen_port
        yaml_output[exporter_name][hostname]['location'] = location
        yaml_output[exporter_name][hostname]['country'] = country
        yaml_output[exporter_name][hostname]['username'] = username
        yaml_output[exporter_name][hostname]['password'] = password

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)
    print("Exporter converter_CMS completed")

##################WINDOWS###################

def exporter_windows(file_path, output_file, output_dir):
    print("Exporter converter_Windows called")
    # Read CSV file into pandas
    df = pd.read_csv(file_path)
    
    # Filter the data based on the condition
    df_filtered = df[df['Exporter_name_os'] == 'exporter_windows']


    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_cms key in the YAML dictionary
    yaml_output['exporter_windows'] = {}

    # Loop through the filtered data and add to the dictionary
    for _, row in df_filtered.iterrows():
        exporter_name = 'exporter_windows'
        fqdn = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
        listen_port = 9182
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
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)

    print("Exporter converter_Windows completed")           
 ##############VERINT###########################

def exporter_verint(file_path, output_file, output_dir):
    print("Exporter converter_Verint called")
    # Read CSV file into pandas
    df = pd.read_csv(file_path)
    
    # Filter the data based on the condition
    df_filtered = df[df['Exporter_name_os'] == 'exporter_verint']


    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_cms key in the YAML dictionary
    yaml_output['exporter_verint'] = {}

    # Loop through the filtered data and add to the dictionary
    for _, row in df_filtered.iterrows():
        exporter_name = 'exporter_verint'
        fqdn = row['FQDN']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
        listen_port = 9182
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
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)
            
    print("Exporter converter_Verint completed")            
            
            
##################AVAYA SBC###########################

def exporter_avayasbc(file_path, output_file, output_dir):

    print("Exporter converter_Avaya SBC called")
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_sbc']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_avayasbc key in the YAML dictionary
    yaml_output['exporter_avayasbc'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        exporter_name = 'exporter_avayasbc'
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']
        username = 'ipcs'  # Generate username as it does not exist in the CSV file
        hostname = row['FQDN']
    
        if hostname not in yaml_output.get(exporter_name, {}):
            yaml_output[exporter_name][hostname] = {}
    
        yaml_output[exporter_name][hostname][ip_address] = {
            'ip_address': ip_address,
            'listen_port': 3601,  # Hard-coded as it is not present in the CSV file
            'location': location,
            'country': country,
            'username': username
        }

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)
    print("Exporter converter_Avaya SBC called")


 
######################GATEWAY###############

def exporter_gateway(file_path, output_file, output_dir):
    print("Exporter gateway called")
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on exporter_name condition
    df = df[df['Exporter_name_app'] == 'exporter_gateway']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_gateway key in the YAML dictionary
    yaml_output['exporter_gateway'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        exporter_name = 'exporter_gateway'
        hostname = row['Hostnames']
        ip_address = row['IP Address']
        listen_port = int(row['App-Listen-Port'])
        location = row['Location']
        country = row['Country']
    
        if hostname not in yaml_output.get(exporter_name, {}):
            yaml_output[exporter_name][hostname] = {}
    
        yaml_output[exporter_name][hostname]['ip_address'] = ip_address
        yaml_output[exporter_name][hostname]['listen_port'] = listen_port
        yaml_output[exporter_name][hostname]['location'] = location
        yaml_output[exporter_name][hostname]['country'] = country
        yaml_output[exporter_name][hostname]['snmp_version'] = 2
        yaml_output[exporter_name][hostname]['community'] = 'ENC'

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)            
 
    print("Exporter gateway completed")

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
            df = pd.read_csv(file_path)
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
        yaml_output[exporter_name][hostname][ip_address]['username'] = 'root'
        yaml_output[exporter_name][hostname][ip_address]['password'] = 'ENC'

        new_entries.append(row)

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    if new_entries:
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
        print("Exporter breeze completed")
        print(f"Total number of hosts processed: {len(new_entries)}")
    else:
        print("Exporter Breeze completed - nothing to do")


####### check if exists in yaml section ########

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

##################MAIN LOOP###################
def create_exporter_checkbuttons(frame):
    for index, name in enumerate(exporter_names):
        var = tk.IntVar()
        column = 0 if index < len(exporter_names) // 2 else 1
        row = index if index < len(exporter_names) // 2 else index - len(exporter_names) // 2
        exporter = tk.Checkbutton(frame, text=name, variable=var)
        exporter.grid(row=row, column=column, padx=10, pady=5, sticky='w')
        exporters.append(exporter)
        exporter_vars.append(var)

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

    # Run selected exporters
    if 'all' in selected_exporter_names:
        run_scripts(['exporter_linux', 'exporter_blackbox', 'exporter_breeze', 'exporter_avayasbc', 'exporter_gateway', 'exporter_verint', 'exporter_windows', 'exporter_ssl', 'exporter_cms'], file_path, output_file, output_dir)
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


####terminal window#########
def redirect_stdout():
    sys.stdout = StdoutRedirector(output_text)
    sys.stderr = StdoutRedirector(output_text)

class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, str):
        self.text_widget.insert(END, str)
        self.text_widget.see(END)

# Create GUI window
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

# Define go_button before calling grid()
go_button = tk.Button(root, text='Go', command=run_exporters)
go_button.grid(row=5, column=2, pady=10, sticky='w')

# Create GUI elements
exporter_names = ['exporter_linux', 'exporter_blackbox', 'exporter_breeze', 'exporter_avayasbc', 'exporter_gateway', 'exporter_verint', 'exporter_windows', 'exporter_ssl', 'exporter_cms']

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
