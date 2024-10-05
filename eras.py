import time
from tkinter import messagebox

# Function to erase the router configuration
def erase_router_config(shell, router_name, result_text):
    try:
        # Send the command to erase the startup configuration
        shell.send('write erase\n')
        time.sleep(2)
        output = shell.recv(10000).decode('utf-8')
        
        # Log the output after sending 'write erase'
        result_text.insert("end", f"{router_name} - Erase command output:\n{output}\n")
        
        # Check if confirmation is required for erasing the configuration
        if 'Erasing the nvram filesystem' in output or 'Continue? [confirm]' in output:
            shell.send('y\n')  # Send 'y' to confirm
            time.sleep(2)
            output = shell.recv(10000).decode('utf-8')
            result_text.insert("end", f"{router_name} - Erase confirmation output:\n{output}\n")
        
        # Send the reload command after erasing the config
        shell.send('reload\n')
        time.sleep(2)
        output = shell.recv(10000).decode('utf-8')
        
        # Log the output after sending 'reload'
        result_text.insert("end", f"{router_name} - Reload command output:\n{output}\n")
        
        # Check if it asks whether to save the configuration before reloading
        if 'System configuration has been modified. Save? [yes/no]:' in output:
            shell.send('no\n')  # Send 'no' to avoid saving the configuration
            time.sleep(2)
            output = shell.recv(10000).decode('utf-8')
            result_text.insert("end", f"{router_name} - Save response output:\n{output}\n")
        
        # Check if confirmation is required for reload
        if 'Proceed with reload' in output:
            shell.send('y\n')  # Confirm reload
            time.sleep(2)
            result_text.insert("end", f"{router_name}: Configuration erased and router reloading...\n")
            messagebox.showinfo("Success", "Configuration erased and router is reloading.")
        else:
            raise Exception("Failed to erase config")
    except Exception as e:
        result_text.insert("end", f"Error while erasing config on {router_name}: {str(e)}\n")
        messagebox.showerror("Error", f"Failed to erase config on {router_name}: {str(e)}")

