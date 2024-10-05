from tkinter import Toplevel, Label, Entry, Button

def open_ospf_config_window(shell, router_name, device_ip, result_text):
    ospf_window = Toplevel()
    ospf_window.title(f"OSPF Configuration for {router_name} ({device_ip})")

    Label(ospf_window, text="Enter OSPF Process ID:").pack(pady=5)
    process_id_entry = Entry(ospf_window, width=30)
    process_id_entry.pack(pady=5)

    Label(ospf_window, text="Enter Network:").pack(pady=5)
    network_entry = Entry(ospf_window, width=30)
    network_entry.pack(pady=5)

    Label(ospf_window, text="Enter Wildcard Mask:").pack(pady=5)
    wildcard_entry = Entry(ospf_window, width=30)
    wildcard_entry.pack(pady=5)

    Label(ospf_window, text="Enter Area:").pack(pady=5)
    area_entry = Entry(ospf_window, width=30)
    area_entry.pack(pady=5)

    # Function to configure OSPF
    def configure_ospf():
        process_id = process_id_entry.get()
        network = network_entry.get()
        wildcard = wildcard_entry.get()
        area = area_entry.get()

        if process_id and network and wildcard and area:
            try:
                command = f"configure terminal\nrouter ospf {process_id}\nnetwork {network} {wildcard} area {area}\nexit\n"
                shell.send(command)
                result_text.insert("end", f"Configured OSPF with Process ID {process_id}, Network {network}, Wildcard {wildcard}, Area {area}.\n")
            except Exception as e:
                result_text.insert("end", f"Error configuring OSPF: {str(e)}\n")

    Button(ospf_window, text="Configure OSPF", command=configure_ospf).pack(pady=10)

    # Back Button
    Button(ospf_window, text="Back", command=ospf_window.destroy).pack(pady=10)
