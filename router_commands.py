from netmiko import ConnectHandler
import paramiko

def run_with_netmiko(ip, command, connection_type="ssh"):
    if connection_type == "telnet":
        router = {
            'device_type': 'cisco_ios_telnet',  # Use telnet instead of SSH
            'host': ip,
            'username': 'admin',  # Use the appropriate username
            'password': 'cisco',  # Use the appropriate password
        }
    else:
        router = {
            'device_type': 'cisco_ios',  # Use SSH by default
            'host': ip,
            'username': 'admin',  # Use the appropriate username
            'password': 'cisco',  # Use the appropriate password
        }
    
    try:
        connection = ConnectHandler(**router)
        output = connection.send_command(command)
        connection.disconnect()
        return output
    except Exception as e:
        return f"Netmiko {connection_type.capitalize()} Error: {str(e)}"

# Function to run a command using Paramiko
def run_with_paramiko(ip, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username='admin', password='cisco')  # Use appropriate credentials
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        ssh.close()
        return output
    except Exception as e:
        return f"Paramiko Error: {str(e)}"

# Function to enable Telnet and SSH on the router
def configure_telnet_ssh(ip, username="admin", password="cisco", enable_secret="cisco"):
    # Define the device configuration details for Netmiko
    device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    
    try:
        # Establish an SSH connection to the device
        connection = ConnectHandler(**device)
        connection.enable()  # Enter enable mode
        
        # Send Telnet configuration commands
        telnet_commands = [
            'conf t',
            'line vty 0 4',
            'login',
            'password cisco',  # Set the password for Telnet access
            'transport input telnet',
            'end',
            'write memory'
        ]
        connection.send_config_set(telnet_commands)
        print("Telnet enabled successfully.")
        
        # Send SSH configuration commands
        ssh_commands = [
            'conf t',
            'ip domain-name example.com',
            'crypto key generate rsa modulus 1024',  # Generate RSA keys for SSH
            'username admin privilege 15 secret cisco',  # Create a user for SSH login
            'line vty 0 4',
            'login local',
            'transport input ssh',
            'end',
            'write memory'
        ]
        connection.send_config_set(ssh_commands)
        print("SSH enabled successfully.")
        
        connection.disconnect()
    except Exception as e:
        print(f"Error while configuring Telnet/SSH: {str(e)}")

# Function to get the current IP address of a router
def get_router_ip(ip, use_telnet=False):
    router = {
        'device_type': 'cisco_ios_telnet' if use_telnet else 'cisco_ios',
        'host': ip,
        'username': 'admin',  # Replace with correct username
        'password': 'cisco',  # Replace with correct password
        'port': 23 if use_telnet else 22,  # Telnet uses port 23, SSH uses port 22
    }
    try:
        connection = ConnectHandler(**router)
        output = connection.send_command('show ip interface brief')
        connection.disconnect()
        return output
    except Exception as e:
        return f"Netmiko Error: {str(e)}"


