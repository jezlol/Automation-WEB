from tkinter import Toplevel, Label, Entry, Button

def open_eigrp_config_window(shell, router_name, device_ip, result_text):
    eigrp_window = Toplevel()
    eigrp_window.title(f"EIGRP Configuration for {router_name} ({device_ip})")

    Label(eigrp_window, text="Enter EIGRP Autonomous System:").pack(pady=5)
    as_entry = Entry(eigrp_window, width=30)
    as_entry.pack(pady=5)

    Label(eigrp_window, text="Enter Network:").pack(pady=5)
    network_entry = Entry(eigrp_window, width=30)
    network_entry.pack(pady=5)

    # Function to configure EIGRP
    def configure_eigrp():
        as_number = as_entry.get()
        network = network_entry.get()

        if as_number and network:
            try:
                command = f"configure terminal\nrouter eigrp {as_number}\nnetwork {network}\nexit\n"
                shell.send(command)
                result_text.insert("end", f"Configured EIGRP with AS {as_number}, Network {network}.\n")
            except Exception as e:
                result_text.insert("end", f"Error configuring EIGRP: {str(e)}\n")

    Button(eigrp_window, text="Configure EIGRP", command=configure_eigrp).pack(pady=10)

    # Back Button
    Button(eigrp_window, text="Back", command=eigrp_window.destroy).pack(pady=10)
