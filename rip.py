from tkinter import Toplevel, Label, Entry, Button

def open_rip_config_window(shell, router_name, device_ip, result_text):
    rip_window = Toplevel()
    rip_window.title(f"RIPv2 Configuration for {router_name} ({device_ip})")

    Label(rip_window, text="Enter Network:").pack(pady=5)
    network_entry = Entry(rip_window, width=30)
    network_entry.pack(pady=5)

    # Function to configure RIPv2
    def configure_rip():
        network = network_entry.get()

        if network:
            try:
                command = f"configure terminal\nrouter rip\nversion 2\nnetwork {network}\nexit\n"
                shell.send(command)
                result_text.insert("end", f"Configured RIPv2 with Network {network}.\n")
            except Exception as e:
                result_text.insert("end", f"Error configuring RIPv2: {str(e)}\n")

    Button(rip_window, text="Configure RIPv2", command=configure_rip).pack(pady=10)

    # Back Button
    Button(rip_window, text="Back", command=rip_window.destroy).pack(pady=10)
