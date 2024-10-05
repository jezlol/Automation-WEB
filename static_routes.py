from tkinter import Toplevel, Label, Entry, Button

def open_route_config_window(shell, router_name, device_ip, result_text):
    route_window = Toplevel()
    route_window.title(f"Configure Static Route - {router_name} ({device_ip})")

    # Label and Entry fields for Static Route inputs
    Label(route_window, text="Enter Destination Network:").pack(pady=5)
    dest_network_entry = Entry(route_window, width=30)
    dest_network_entry.pack(pady=5)

    Label(route_window, text="Enter Subnet Mask:").pack(pady=5)
    subnet_mask_entry = Entry(route_window, width=30)
    subnet_mask_entry.pack(pady=5)

    Label(route_window, text="Enter Next-Hop IP Address:").pack(pady=5)
    next_hop_entry = Entry(route_window, width=30)
    next_hop_entry.pack(pady=5)

    # Function to configure the static route
    def configure_route():
        dest_network = dest_network_entry.get()
        subnet_mask = subnet_mask_entry.get()
        next_hop = next_hop_entry.get()
        if dest_network and subnet_mask and next_hop:
            try:
                command = f"configure terminal\nip route {dest_network} {subnet_mask} {next_hop}\nexit\nexit\n"
                shell.send(f"{command}\n")
                time.sleep(2)
                output = shell.recv(10000).decode('utf-8')
                result_text.insert("end", f"Configured static route:\n{output}\n")
            except Exception as e:
                result_text.insert("end", f"Error configuring static route: {str(e)}\n")

    # Function to remove the static route
    def remove_route():
        dest_network = dest_network_entry.get()
        subnet_mask = subnet_mask_entry.get()
        next_hop = next_hop_entry.get()
        if dest_network and subnet_mask and next_hop:
            try:
                command = f"configure terminal\nno ip route {dest_network} {subnet_mask} {next_hop}\nexit\nexit\n"
                shell.send(f"{command}\n")
                time.sleep(2)
                output = shell.recv(10000).decode('utf-8')
                result_text.insert("end", f"Removed static route:\n{output}\n")
            except Exception as e:
                result_text.insert("end", f"Error removing static route: {str(e)}\n")

    # Configure Route Button
    configure_button = Button(route_window, text="Configure Route", command=configure_route)
    configure_button.pack(pady=5)

    # Remove Route Button
    remove_button = Button(route_window, text="Remove Route", command=remove_route)
    remove_button.pack(pady=5)

    # Back Button to return to the previous window
    def go_back():
        route_window.destroy()

    back_button = Button(route_window, text="Back", command=go_back)
    back_button.pack(pady=10)
