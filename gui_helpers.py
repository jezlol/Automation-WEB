from eve_ng_api import get_lab_devices
from gui_components import load_saved_ips

def load_devices_into_treeview(treeview):
    devices = get_lab_devices()
    saved_ips = load_saved_ips()  # Load saved IPs from the file

    # Clear the current Treeview content
    for item in treeview.get_children():
        treeview.delete(item)

    # Populate Treeview with devices
    for device in devices:
        device_id = device['id']
        device_name = device['name']
        device_type = device['type']
        
        # Use saved IP if available, otherwise default to N/A
        device_ip = saved_ips.get(device_name, 'N/A')
        
        # Insert the device information into the Treeview
        treeview.insert('', 'end', values=(device_id, device_name, device_ip, device_type))