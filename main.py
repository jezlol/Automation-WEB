import tkinter as tk
from tkinter import ttk
from gui_components import open_ip_edit_window, save_callback  # Import other necessary functions from gui_components
from gui_helpers import load_devices_into_treeview  # Import load_devices_into_treeview from gui_helpers
from router_commands import run_with_netmiko, run_with_paramiko  # Router command functions
from ssh_cli import login_via_ssh  # Import the new SSH functionality
from ssh_cli import login_via_ssh
from tkinter import Tk, Toplevel, Text, Entry, Button, Label, ttk


# Create the main GUI window
root = tk.Tk()
root.title("Device Management Tool")
root.geometry("900x600")

# Create a Treeview to show devices
device_tree = ttk.Treeview(root, columns=("ID", "Name", "IP", "Type"), show='headings')
device_tree.heading("ID", text="ID")
device_tree.heading("Name", text="Name")
device_tree.heading("IP", text="IP")
device_tree.heading("Type", text="Type")
device_tree.pack(fill=tk.BOTH, expand=True)

# Load devices into the Treeview
load_devices_into_treeview(device_tree)

# Bind double-click to open the IP edit popup
device_tree.bind("<Double-1>", lambda event: on_router_click(event, device_tree))

# Function to handle router click and open the IP edit popup
def on_router_click(event, device_tree):
    selection = device_tree.selection()
    if selection:
        selected_router = device_tree.item(selection[0])["values"]
        router_name = selected_router[1]  # Assuming the device name is in the second column
        current_ip = selected_router[2]   # Prefill with current IP (initially 'N/A')
        open_ip_edit_window(router_name, current_ip, save_callback, device_tree, selection[0])

# Text area for output
result_text = tk.Text(root, height=10, width=70)
result_text.pack(pady=10)

# Run button for SSH login (calls the new SSH functionality)
def run_ssh_login():
    selected_device = device_tree.selection()
    if not selected_device:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Please select a device to login.\n")
        return

    device_info = device_tree.item(selected_device)["values"]
    device_name = device_info[1]
    device_ip = device_info[2]
    
    if device_ip == 'N/A':
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "No IP assigned to this device.\n")
        return

    login_via_ssh(device_name, device_ip, result_text)

# Run button for SSH login
login_button = tk.Button(root, text="Login via SSH", command=run_ssh_login)
login_button.pack(pady=5)


# Refresh button to reload devices
refresh_button = tk.Button(root, text="Refresh", command=lambda: load_devices_into_treeview(device_tree))
refresh_button.pack(side=tk.LEFT, padx=10)


# Start the GUI loop

# Function to log messages in the Log Window
def log_message(message):
    log_window.insert("end", f"{message}\n")
    log_window.see("end")  # Auto-scroll to the end of the log
root.mainloop()
