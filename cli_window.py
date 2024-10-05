import time
from tkinter import Toplevel, Text, Entry, Button

# Function to create the CLI window after logging in via SSH
def open_cli_window(shell, router_name, device_ip, result_text):
    cli_window = Toplevel()
    cli_window.title(f"CLI for {router_name} ({device_ip})")
    
    # Create a Text area for the output
    cli_output = Text(cli_window, height=20, width=80)
    cli_output.pack(padx=10, pady=10)
    
    # Entry for input commands
    cli_entry = Entry(cli_window, width=80)
    cli_entry.pack(padx=10, pady=10)
    
    # Function to send the command and display output in both CLI window and main result area
    def send_command(event=None):
        command = cli_entry.get()
        if command:
            shell.send(f"{command}\n")
            time.sleep(2)
            output = shell.recv(10000).decode('utf-8')
            cli_output.insert("end", f"{router_name}# {command}\n{output}\n")
            result_text.insert("end", f"{router_name}# {command}\n{output}\n")
            cli_entry.delete(0, "end")
    
    # Button to send commands
    send_button = Button(cli_window, text="Send", command=send_command)
    send_button.pack(pady=5)

    # Back Button to return to the main option window
    def go_back():
        cli_window.destroy()

    back_button = Button(cli_window, text="Back", command=go_back)
    back_button.pack(pady=5)

    # Bind the Enter key to the send_command function
    cli_entry.bind("<Return>", send_command)
