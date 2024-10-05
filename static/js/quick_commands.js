// Initialize the WebSocket connection
var socket = io.connect('http://127.0.0.1:5000');

// Function to send command through WebSocket
function sendCommand(command) {
    const routerName = document.getElementById('router_name').innerText;
    const deviceIp = document.getElementById('device_ip').innerText;

    // Notify the user that the script is running
    document.getElementById('command_output').innerHTML = '<pre>Script is running...</pre>';

    // Correct the command to 'show running-config'
    if (command === 'show_running_config') {
        command = 'show running-config';  // Ensure correct IOS command is sent
    }

    socket.emit('run_command', {
        command: command,
        router_name: routerName,
        device_ip: deviceIp
    });
}


// Listen for the result of the command from the server
socket.on('command_result', function(data) {
    const outputDiv = document.getElementById('command_output');
    if (data.success) {
        outputDiv.innerHTML = `<pre>${data.output}</pre>`;
    } else {
        outputDiv.innerHTML = `<pre>Error: ${data.output}</pre>`;
    }
});

// Function to show the traceroute popup
function showTraceroutePopup() {
    const popup = document.createElement('div');
    popup.id = 'traceroute-popup';
    popup.innerHTML = `
        <div class="popup-content">
            <h3>Traceroute Configuration</h3>
            <label for="destination_ip">Destination IP:</label>
            <input type="text" id="destination_ip" placeholder="Enter IP address" required><br><br>
            <label for="time_delay">Time Delay (ms):</label>
            <input type="number" id="time_delay" placeholder="Enter time delay" required><br><br>
            <button onclick="runTraceroute()">Run Traceroute</button>
            <button onclick="closePopup()">Cancel</button>
        </div>
    `;

    // Add popup styles
    popup.style.position = 'fixed';
    popup.style.left = '50%';
    popup.style.top = '50%';
    popup.style.transform = 'translate(-50%, -50%)';
    popup.style.backgroundColor = 'white';
    popup.style.padding = '20px';
    popup.style.boxShadow = '0px 0px 10px rgba(0, 0, 0, 0.1)';
    popup.style.zIndex = '1000';

    document.body.appendChild(popup);
}

// Function to run traceroute
function runTraceroute() {
    const destinationIp = document.getElementById('destination_ip').value;
    const timeDelay = document.getElementById('time_delay').value;

    if (!destinationIp || !timeDelay) {
        alert('Please enter both Destination IP and Time Delay');
        return;
    }

    const routerName = document.getElementById('router_name').textContent;
    const deviceIp = document.getElementById('device_ip').textContent;

    // Emit WebSocket event for traceroute
    socket.emit('run_command', {
        command: 'traceroute',
        router_name: routerName,
        device_ip: deviceIp,
        destination_ip: destinationIp,
        time_delay: timeDelay
    });

    closePopup();
}

// Function to close the popup
function closePopup() {
    const popup = document.getElementById('traceroute-popup');
    if (popup) {
        document.body.removeChild(popup);
    }
}

// Function to clear the command output
function clearOutput() {
    const outputDiv = document.getElementById('command_output');
    outputDiv.innerHTML = '';  // Clear the output area
}

// Attach the showTraceroutePopup function to the Traceroute button
document.getElementById('traceroute_button').addEventListener('click', showTraceroutePopup);
