import time

# Show ARP Table
def show_arp_table(shell, router_name, result_text):
    try:
        shell.send('show arp\n')
        time.sleep(2)
        output = shell.recv(10000).decode('utf-8')
        result_text.insert("end", f"{router_name} - Show ARP Table:\n{output}\n")
    except Exception as e:
        result_text.insert("end", f"Error running 'show arp': {str(e)}\n")

# Clear ARP Table
def clear_arp_table(shell, router_name, result_text):
    try:
        shell.send('clear arp-cache\n')
        time.sleep(2)
        output = shell.recv(10000).decode('utf-8')
        result_text.insert("end", f"{router_name} - Clear ARP Table:\n{output}\n")
    except Exception as e:
        result_text.insert("end", f"Error running 'clear arp-cache': {str(e)}\n")
