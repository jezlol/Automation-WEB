from tkinter import Toplevel, Button, Label
from static_routes import open_route_config_window
from ospf import open_ospf_config_window
from rip import open_rip_config_window
from eigrp import open_eigrp_config_window

def open_routing_window(shell, router_name, device_ip, result_text):
    routing_window = Toplevel()
    routing_window.title(f"Routing Configuration for {router_name} ({device_ip})")

    Label(routing_window, text=f"Routing Configuration for {router_name}").pack(pady=10)

    # Static Route Button
    Button(routing_window, text="Static Route", command=lambda: open_route_config_window(shell, router_name, device_ip, result_text)).pack(pady=5)

    # OSPF Button
    Button(routing_window, text="OSPF", command=lambda: open_ospf_config_window(shell, router_name, device_ip, result_text)).pack(pady=5)

    # RIPv2 Button
    Button(routing_window, text="RIPv2", command=lambda: open_rip_config_window(shell, router_name, device_ip, result_text)).pack(pady=5)

    # EIGRP Button
    Button(routing_window, text="EIGRP", command=lambda: open_eigrp_config_window(shell, router_name, device_ip, result_text)).pack(pady=5)

    # Back Button to return to the previous window
    def go_back():
        routing_window.destroy()

    Button(routing_window, text="Back", command=go_back).pack(pady=10)
