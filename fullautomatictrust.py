import psutil
import requests
import webbrowser
import os
import time

# Function to get the current network usage in bytes
def monitor_network():
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent + net_io.bytes_recv

# Convert bytes to megabits per second (Mbps)
def bytes_to_mbps(byte_diff, time_interval=1):
    bits = byte_diff * 8  # Convert bytes to bits
    mbits = bits / (10**6)  # Convert bits to megabits
    return mbits / time_interval  # Convert to Mbps

def get_geolocation(ip):
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
            h2 {{
                margin: 20px 0;
                font-size: 24px;
                text-align: center;
            }}
            .info {{
                background-color: rgba(18, 18, 18, 0.8);
                padding: 10px;
                border-radius: 5px;
                text-align: center;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            }}
        </style>
    </head>
    <body>
        <h2>Server Location Map for IP: {ip}</h2>
        <div id="map"></div>
        <div class="info">
            <p>Location: {location['city']}, {location['region']}, {location['country']}</p>
            <p>ISP: {location['isp']}</p>
            <p>AS: {location['as']}</p>
            <p>Program: {program_name}</p>
        </div>
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

# Initialize a variable to store the last detected IP
last_ip = None

# Main loop to monitor and display network speed in Mbps
previous_usage = monitor_network()
threshold_mbps = 5.0  # Set your threshold in Mbps

while True:
    time.sleep(1)  # Monitor every second
    current_usage = monitor_network()
    
    # Calculate the difference in bytes over the 1-second interval
    byte_diff = current_usage - previous_usage
    
    # Convert the byte difference to Mbps (megabits per second)
    current_mbps = bytes_to_mbps(byte_diff, time_interval=1)
    
    # Display the current network speed in Mbps
    print(f"Current Network Speed: {current_mbps:.2f} Mbps")
    
    # Check if the current Mbps exceeds the threshold
    if current_mbps > threshold_mbps:
        connections = psutil.net_connections(kind='inet')
        for conn in connections:
            if conn.status == 'ESTABLISHED' and conn.raddr and conn.raddr[0] != '127.0.0.1':
                server_ip = conn.raddr[0]  # Get remote address

                pid = conn.pid
                program_name = "Unknown"
                if pid is not None:
                    try:
                        process = psutil.Process(pid)
                        program_name = process.name()
                    except psutil.NoSuchProcess:
                        program_name = "Unknown"
                
                # Only process if it's a new IP
                if server_ip != last_ip:
                    last_ip = server_ip  # Update the last IP
                    location = get_geolocation(server_ip)
                    if location:
                        print(f"Incoming data from {server_ip}: {current_mbps:.2f} Mbps")
                        create_map(location, server_ip, program_name)  # Pass the program name to the map function

                break  # Exit after processing the first valid external connection
        break

    # Update the previous usage for the next comparison
    previous_usage = current_usage
