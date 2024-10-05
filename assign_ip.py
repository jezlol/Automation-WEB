from tkinter import Toplevel, Label, Entry, Button
from tkinter import ttk  # Import for Combobox (dropdown)
import time

def open_assign_ip_window(shell, router_name, device_ip, result_text):
    assign_window = Toplevel()
    assign_window.title(f"Assign IP to Interface - {router_name} ({device_ip})")

    # Label for the interface selection
    Label(assign_window, text=f"Choose Interface for {router_name}").pack(pady=5)

    # Dropdown to select an interface
    interfaces = ['fa0/0', 'fa0/1', 'fa1/0']  # Example interfaces
    interface_var = ttk.Combobox(assign_window, values=interfaces, width=30)
    interface_var.pack(pady=5)
    interface_var.set('fa0/0')  # Default value

    # Entry field for IP address
    Label(assign_window, text="Enter IP Address:").pack(pady=5)
    ip_entry = Entry(assign_window, width=30)
    ip_entry.pack(pady=5)

    # Entry field for Subnet Mask
    Label(assign_window, text="Enter Subnet Mask:").pack(pady=5)
    subnet_entry = Entry(assign_window, width=30)
    subnet_entry.pack(pady=5)

    # Function to run the command for assigning the IP to the selected interface
    def run_ip_assignment():
        selected_interface = interface_var.get()
        ip_address = ip_entry.get()
        subnet_mask = subnet_entry.get()

        if selected_interface and ip_address and subnet_mask:
            try:
                # Construct the full set of commands to assign the IP
                command = f"configure terminal\ninterface {selected_interface}\nip address {ip_address} {subnet_mask}\nexit\nexit\n"
                shell.send(f"{command}\n")
                time.sleep(2)
                output = shell.recv(10000).decode('utf-8')

                if "% Invalid input detected" in output:  # Error detection
                    raise Exception("Invalid input detected")

                result_text.insert("end", f"Assigned IP to {selected_interface}:\n{output}\n")
            except Exception as e:
                result_text.insert("end", f"Error assigning IP: {str(e)}\n")
        else:
            result_text.insert("end", "Please provide valid values for interface, IP address, and subnet mask.\n")

    # Function to remove the IP from the selected interface
    def remove_ip_assignment():
        selected_interface = interface_var.get()

        if selected_interface:
            try:
                # Command to remove the IP from the selected interface
                command = f"configure terminal\ninterface {selected_interface}\nno ip address\nexit\nexit\n"
                shell.send(f"{command}\n")
                time.sleep(2)
                output = shell.recv(10000).decode('utf-8')

                if "% Invalid input detected" in output:  # Error detection
                    raise Exception("Invalid input detected")

                result_text.insert("end", f"Removed IP from {selected_interface}:\n{output}\n")
            except Exception as e:
                result_text.insert("end", f"Error removing IP: {str(e)}\n")
        else:
            result_text.insert("end", "Please select a valid interface.\n")

    # Button to assign IP
    assign_button = Button(assign_window, text="Assign IP", command=run_ip_assignment)
    assign_button.pack(pady=5)

    # Button to remove IP
    remove_button = Button(assign_window, text="Remove IP", command=remove_ip_assignment)
    remove_button.pack(pady=5)

    # Back Button to return to the previous window
    def go_back():
        assign_window.destroy()

    back_button = Button(assign_window, text="Back", command=go_back)
    back_button.pack(pady=10)
