import psutil
import requests
import webbrowser
import os
import time
import threading
from flask import Flask, render_template, jsonify
from collections import defaultdict

app = Flask(__name__)
app_data_usage = defaultdict(int)
last_ip = None  # Store last detected IP to avoid repeated processing
threshold_mbps = 5.0  # Threshold for high-speed connections in Mbps

def monitor_network():
    """Get the current network usage in bytes."""
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent + net_io.bytes_recv

def bytes_to_mbps(byte_diff, time_interval=1):
    """Convert byte difference to Mbps."""
    bits = byte_diff * 8  # Convert bytes to bits
    mbits = bits / (10**6)  # Convert bits to megabits
    return mbits / time_interval  # Convert to Mbps

def get_geolocation(ip):
    """Fetch geolocation data for a given IP address."""
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'city': data.get('city', 'Unknown City'),
            'country': data.get('country', 'Unknown Country'),
            'region': data.get('regionName', 'Unknown Region'),
            'isp': data.get('isp', 'Unknown ISP'),
            'as': data.get('as', 'Unknown AS'),
            'latitude': data.get('lat'),
            'longitude': data.get('lon')
        }
    return None

def create_map(location, ip, program_name):
    """Generate and display an HTML map with server geolocation."""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Server Location Map</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #121212;
                color: #ffffff;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }}
            #map {{
                height: 70vh;
                width: 80%;
                border: 2px solid #ffffff;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
            }}
        </style>
    </head>
    <body>
        <h2>Server Location Map for IP: {ip}</h2>
        <div id="map"></div>
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
        <script>
            var map = L.map('map').setView([{location['latitude']}, {location['longitude']}], 10);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 19,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }}).addTo(map);
            L.marker([{location['latitude']}, {location['longitude']}]).addTo(map)
                .bindPopup("{ip}<br>({location['city']}, {location['region']}, {location['country']})<br>Program: {program_name}").openPopup();
        </script>
    </body>
    </html>
    """
    with open('server_location_map.html', 'w') as file:
        file.write(html_content)
    webbrowser.open('file://' + os.path.realpath('server_location_map.html'))

def update_usage():
    """Update the network usage statistics and track high-speed connections."""
    global last_ip
    previous_usage = monitor_network()
    
    while True:
        app_data_usage.clear()
        connections = psutil.net_connections(kind='inet')
        for conn in connections:
            if conn.status == 'ESTABLISHED' and conn.raddr:
                pid = conn.pid
                if pid is not None:
                    try:
                        process = psutil.Process(pid)
                        app_name = process.name()
                        exe_path = process.exe()

                        whitelist = [
                            "C:\\Program Files\\Google",
                            "C:\\Program Files\\Cloudflare",
                            "C:\\Program Files\\Epic Games"
                        ]

                        if any(exe_path.startswith(path) for path in [
                            "C:\\Windows\\", 
                            "C:\\Program Files\\", 
                            "C:\\Program Files (x86)\\"
                        ]) and not any(exe_path.startswith(path) for path in whitelist):
                            continue
                        
                        bytes_sent, bytes_recv = process.io_counters()[:2]
                        app_data_usage[app_name] += (bytes_sent + bytes_recv) / (1024 * 1024)  # MB

                        current_usage = monitor_network()
                        byte_diff = current_usage - previous_usage
                        current_mbps = bytes_to_mbps(byte_diff, time_interval=1)

                        if current_mbps > threshold_mbps and conn.raddr[0] != '127.0.0.1':
                            server_ip = conn.raddr[0]
                            if server_ip != last_ip:
                                last_ip = server_ip
                                location = get_geolocation(server_ip)
                                if location:
                                    create_map(location, server_ip, app_name)

                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(app_data_usage)

if __name__ == '__main__':
    # Start the usage update thread
    threading.Thread(target=update_usage, daemon=True).start()
    app.run(debug=True, use_reloader=False)
