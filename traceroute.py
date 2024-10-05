from tkinter import Toplevel, Label, Entry, Button
import time

def traceroute_script(shell, router_name, device_ip, result_text):
    # Create a new window for Traceroute
    traceroute_window = Toplevel()
    traceroute_window.title(f"Traceroute - {router_name} ({device_ip})")

    # Label for Destination IP
    Label(traceroute_window, text="Enter Destination IP Address:").pack(pady=5)

    # Entry for Destination IP
    dest_ip_entry = Entry(traceroute_window, width=30)
    dest_ip_entry.pack(pady=5)

    # Label for Timeout (optional, if you want to provide a timeout)
    Label(traceroute_window, text="Enter Timeout (in seconds, optional):").pack(pady=5)
    timeout_entry = Entry(traceroute_window, width=10)
    timeout_entry.pack(pady=5)

    # Function to run the traceroute command
    def run_traceroute():
        dest_ip = dest_ip_entry.get()
        timeout = timeout_entry.get()

        if dest_ip:
            try:
                # Use the timeout value if provided, otherwise use a default of 2 seconds
                timeout_value = int(timeout) if timeout else 2

                # Construct the traceroute command
                command = f"traceroute {dest_ip}\n"
                shell.send(command)
                time.sleep(timeout_value)

                output = shell.recv(10000).decode('utf-8')
                result_text.insert("end", f"{router_name} - Traceroute to {dest_ip}:\n{output}\n")
            except Exception as e:
                result_text.insert("end", f"Error running traceroute: {str(e)}\n")
        else:
            result_text.insert("end", "Please provide a valid destination IP address.\n")

    # Button to execute the traceroute command
    run_button = Button(traceroute_window, text="Run Traceroute", command=run_traceroute)
    run_button.pack(pady=5)

    # Back Button to close the window and return to the previous screen
    def go_back():
        traceroute_window.destroy()  # Close the traceroute window

    back_button = Button(traceroute_window, text="Back", command=go_back)
    back_button.pack(pady=10)
