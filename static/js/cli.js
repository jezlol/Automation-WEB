function sendCommand() {
    const command = document.getElementById("command").value;

    fetch('/run_command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            command: command,
            router_name: '{{ router_name }}',
            device_ip: '{{ device_ip }}'
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').value += data.output + '\n';
    })
    .catch(error => {
        alert('Failed to send the command.');
        console.error('Error:', error);
    });
}
