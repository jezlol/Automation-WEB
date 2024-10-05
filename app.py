from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
from eve_ng_api import get_lab_devices
from netmiko import ConnectHandler


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # จำเป็นต้องมี secret_key สำหรับการใช้ session
socketio = SocketIO(app)

# Default route to show device list and login form
@app.route('/')
def index():
    devices = get_lab_devices()
    return render_template('index.html', devices=devices)

# Route for SSH login
@app.route('/login_ssh', methods=['POST'])
def login_ssh():
    router_name = request.form['router_name']
    device_ip = request.form['device_ip']

    # เก็บค่า router_name และ device_ip ลงใน session
    session['router_name'] = router_name
    session['device_ip'] = device_ip

    return redirect(url_for('router_options'))

# Router Options - Main menu
@app.route('/router_options')
def router_options():
    router_name = session.get('router_name')
    device_ip = session.get('device_ip')
    
    if not router_name or not device_ip:
        return redirect(url_for('index'))

    return render_template('option_window.html', router_name=router_name, device_ip=device_ip)

# CLI page
@app.route('/cli')
def cli():
    router_name = session.get('router_name')
    device_ip = session.get('device_ip')

    if not router_name or not device_ip:
        return redirect(url_for('index'))

    return render_template('cli.html', router_name=router_name, device_ip=device_ip)

# Quick Command Scripts page
@app.route('/quick_command_scripts')
def quick_command_scripts():
    router_name = session.get('router_name')
    device_ip = session.get('device_ip')

    if not router_name or not device_ip:
        return redirect(url_for('index'))

    return render_template('quick_command.html', router_name=router_name, device_ip=device_ip)


def run_show_ip_int_brief(router_name, device_ip):
    try:
        # ข้อมูลการเชื่อมต่อของ Router (สามารถแก้ไข username และ password ได้)
        router = {
            'device_type': 'cisco_ios',  # ประเภทของ Router (เปลี่ยนได้ตามรุ่นของ Router)
            'host': device_ip,
            'username': 'jez',  # ใช้ username ของคุณ
            'password': '123',  # ใช้ password ของคุณ
            'secret': '123'  # ใช้ enable password ของคุณ    
        }

        # เริ่มการเชื่อมต่อ
        connection = ConnectHandler(**router)

        # เข้าสู่โหมด enable
        connection.enable()

        # รันคำสั่ง 'show ip interface brief'
        output = connection.send_command("show ip interface brief")

        # ปิดการเชื่อมต่อ
        connection.disconnect()

        return output

    except Exception as e:
        return str(e)
    
# WebSocket event for running commands
@socketio.on('run_command')
def handle_run_command(data):
    try:
        command = data.get('command')
        router_name = data.get('router_name')
        device_ip = data.get('device_ip')

        if not command:
            emit('command_result', {'success': False, 'output': 'No command provided.'})
            return

        # ข้อมูลสำหรับการเชื่อมต่อ Router
        router = {
            'device_type': 'cisco_ios',  # ประเภทอุปกรณ์
            'ip': device_ip,
            'username': 'jez',  # ใส่ username ที่ใช้ login ไปยัง router
            'password': '123',  # ใส่ password ที่ใช้ login ไปยัง router
            'secret': '123',  # enable password
        }

        # เชื่อมต่อกับ Router โดยใช้ Netmiko
        net_connect = ConnectHandler(**router)
        net_connect.enable()  # เข้าสู่ enable mode

        if command == 'show_ip_interface_brief':
            output = net_connect.send_command('show ip interface brief')

        elif command == 'traceroute':
            destination_ip = data.get('destination_ip')
            time_delay = data.get('time_delay')
            if not destination_ip:
                emit('command_result', {'success': False, 'output': 'No destination IP provided.'})
                return

            traceroute_command = f'traceroute {destination_ip} timeout {time_delay}'
            output = net_connect.send_command(traceroute_command)
        elif command == 'show running-config':
            output = net_connect.send_command('show running-config')    

        else:
            output = f"Unknown command: {command}"

        emit('command_result', {'success': True, 'output': output})

    except Exception as e:
        emit('command_result', {'success': False, 'output': f"Error: {str(e)}"})

if __name__ == '__main__':
    socketio.run(app, debug=True)
