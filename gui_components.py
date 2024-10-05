import json
from tkinter import Toplevel, Label, Entry, Button

# File where IPs will be saved
IP_FILE = "ip_data.json"

# Load saved IPs from a JSON file
def load_saved_ips():
    try:
        with open(IP_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save IPs to the JSON file
def save_ips(ip_data):
    with open(IP_FILE, "w") as f:
        json.dump(ip_data, f)

# Function to open a popup to manually enter or edit the IP address
def open_ip_edit_window(router_name, current_ip, save_callback, device_tree, selected_index):
    window = Toplevel()
    window.title(f"Edit IP Address for {router_name}")
    
    # Set the size of the popup window
    window.geometry("300x200")

    # Display current IP address (if any) or placeholder for input
    Label(window, text=f"Current IP: {current_ip}").pack(pady=10, padx=10)

    # Input field for the new IP address
    new_ip_var = Entry(window)
    new_ip_var.insert(0, current_ip)  # Prefill with the current IP or N/A
    new_ip_var.pack(pady=10, padx=10)

    # Function to save the new IP
    def save_new_ip():
        new_ip = new_ip_var.get()
        save_callback(router_name, new_ip, device_tree, selected_index)  # Pass the new IP to save
        window.destroy()  # Close the popup

    # Add Save and Cancel buttons with some padding for layout
    Button(window, text="Save", command=save_new_ip).pack(pady=10, padx=10)
    Button(window, text="Cancel", command=window.destroy).pack(pady=5, padx=10)

# Callback function to handle IP saving and update the GUI
def save_callback(router_name, new_ip, device_tree, selected_index):
    # Get the current values of the selected item
    current_values = device_tree.item(selected_index, 'values')
    
    # Convert current values to a list and update the IP (assuming the third column is for the IP address)
    updated_values = list(current_values)
    updated_values[2] = new_ip  # Update the IP in the third column

    # Update the item in the Treeview with new values
    device_tree.item(selected_index, values=updated_values)

    # Load the saved IPs from the JSON file
    saved_ips = load_saved_ips()
    
    # Update the IP for this router
    saved_ips[router_name] = new_ip

    # Save the updated IPs to the file
    save_ips(saved_ips)

    # Log the change
    print(f"Router: {router_name}, updated IP: {new_ip}")
