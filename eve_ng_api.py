import requests

LAB_ID = "Jezlol.unl"  # Define your LAB ID here

def login_to_eve_ng():
    url = "http://192.168.1.148/api/auth/login"
    data = {
        'username': 'admin',
        'password': 'eve',
        'html5': '-1'
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.cookies
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Login error: {str(e)}")
        return None

# Function to get devices from Eve-NG Lab
def get_lab_devices():
    cookies = login_to_eve_ng()
    if not cookies:
        return []

    url = f"http://192.168.1.148/api/labs/{LAB_ID}/nodes"
    
    try:
        response = requests.get(url, cookies=cookies)
        if response.status_code == 200:
            devices = response.json().get('data', {})
            if isinstance(devices, dict):
                return [
                    {'id': node_id, 'name': node_info['name'], 'ip': node_info.get('ip', 'N/A'), 'type': node_info['type']} 
                    for node_id, node_info in devices.items()
                ]
            else:
                print(f"Unexpected data format: {devices}")
                return []
        else:
            print(f"Failed to get devices: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching devices: {str(e)}")
        return []
