import paramiko
import time

# Function to log into a router via SSH
def login_via_ssh(router_name, device_ip, result_text):
    username = "jez"  # Update this with your actual SSH username
    password = "123"  # Update this with your actual SSH password
    enable_password = "123"  # Update this if needed

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=device_ip, username=username, password=password)

        shell = client.invoke_shell()

        # Wait for the prompt and clear the buffer
        time.sleep(1)
        shell.recv(1000)

        # Send 'enable' command
        shell.send('enable\n')
        time.sleep(1)
        shell.recv(1000)  # Clear the buffer

        # Send the enable password
        shell.send(f'{enable_password}\n')
        time.sleep(1)
        shell.recv(1000)  # Clear the buffer again

        result_text = f"Logged into {router_name} ({device_ip}) successfully!"
        return True
    except Exception as e:
        result_text = f"SSH login failed for {router_name} ({device_ip}): {str(e)}"
        return False
