def run_quick_command(command, router_name, device_ip):
    # Simulate running a command and returning a result
    if command == 'assign_ip':
        result = f"Assigned IP to {device_ip}"
    elif command == 'show_ip_interface_brief':
        result = f"{router_name} - IP Interface Brief:\nFastEthernet0/0: UP\nFastEthernet0/1: DOWN"
    elif command == 'traceroute':
        result = f"{router_name} - Traceroute to 8.8.8.8:\n1. 192.168.1.1\n2. 8.8.8.8"
    else:
        result = "Invalid Command"
    
    return result
