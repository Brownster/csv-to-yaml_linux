import tkinter as tk
from tkinter import filedialog, messagebox, END
import sys
import pandas as pd
import yaml
import os
from tkinter import Text

###############LINUX#########################


def exporter_linux(file_path, output_file, output_dir):
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
    print("Exporter Breeze called")
    # Read CSV file into pandas
    df = pd.read_csv(file_path)

    # Filter rows based on condition
    df = df[df['Exporter_name_app'] == 'exporter_breeze']

    # Create an empty dictionary to store the YAML output
    yaml_output = {}

    # Initialize exporter_breeze key in the YAML dictionary
    yaml_output['exporter_breeze'] = {}

    # Iterate over rows in filtered dataframe
    for index, row in df.iterrows():
        exporter_name = 'exporter_breeze'
        hostname = row['Hostnames']
        ip_address = row['IP Address']
        location = row['Location']
        country = row['Country']

        if hostname not in yaml_output.get(exporter_name, {}):
            yaml_output[exporter_name][hostname] = {}

        if ip_address not in yaml_output[exporter_name][hostname]:
            yaml_output[exporter_name][hostname][ip_address] = {}

        yaml_output[exporter_name][hostname][ip_address]['listen_port'] = int(row['App-Listen-Port'])
        yaml_output[exporter_name][hostname][ip_address]['location'] = location
        yaml_output[exporter_name][hostname][ip_address]['country'] = country
        yaml_output[exporter_name][hostname][ip_address]['username'] = 'root'
        yaml_output[exporter_name][hostname][ip_address]['password'] = 'ENC'

    # Write the YAML data to a file, either appending to an existing file or creating a new file
    output_path = output_dir + output_file
    if os.path.exists(output_path):
        with open(output_path, 'a') as f:
            yaml.dump(yaml_output, f)
    else:
        with open(output_path, 'w') as f:
            yaml.dump(yaml_output, f)   

    print("Exporter Breeze completed")

##################MAIN LOOP###################

def run_exporters():
    global exporter_vars  # Add this line to specify that we're using the global variable
    # Get the file path
    file_path = file_path_entry.get()

    # Get the output file name
    output_file = output_file_entry.get()

    # Get the output directory
    output_dir = output_dir_entry.get()

    # Get the selected exporter names
    selected_exporter_names = [name for name, var in zip(exporter_names, exporter_vars) if var.get()]

    # Create a dictionary of exporter names and associated variables
   # exporter_vars = {name: var for name, var in zip(exporter_names, exporters)}

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
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, str):
        self.text_widget.insert(END, str)
        self.text_widget.see(END)


# Create GUI window
root = tk.Tk()
root.title('Exporters GUI')

# create text widget to display output
output_text = Text(root)
output_text.pack()

# redirect stdout to the text widget
sys.stdout = StdoutRedirector(output_text)


# Create GUI elements
exporter_names = ['exporter_linux', 'exporter_blackbox', 'exporter_breeze', 'exporter_avayasbc', 'exporter_gateway', 'exporter_verint', 'exporter_windows', 'exporter_ssl', 'exporter_cms']
exporters = []
exporter_vars = []  # Add this line to create an empty list for the IntVar instances

for name in exporter_names:
    var = tk.IntVar()  # Create an IntVar instance for each checkbutton
    exporter = tk.Checkbutton(root, text=name, variable=var)
    exporter.pack()
    exporters.append(exporter)
    exporter_vars.append(var)  # Add the IntVar instance to the list

file_path_label = tk.Label(root, text='CSV File path:')
file_path_label.pack()
file_path_entry = tk.Entry(root)
file_path_entry.pack()
file_path_button = tk.Button(root, text='Browse', command=browse_file_path)
file_path_button.pack()

output_file_label = tk.Label(root, text='Yaml Output file name:')
output_file_label.pack()
output_file_entry = tk.Entry(root)
output_file_entry.pack()

output_dir_label = tk.Label(root, text='Yaml Output directory:')
output_dir_label.pack()
output_dir_entry = tk.Entry(root)
output_dir_entry.pack()

go_button = tk.Button(root, text='Go', command=run_exporters)
go_button.pack()

# Create a main loop to display the GUI window
root.mainloop()