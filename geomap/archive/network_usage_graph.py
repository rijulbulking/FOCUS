from flask import Flask, render_template, jsonify
import psutil
import threading
import time
from collections import defaultdict

app = Flask(__name__)
app_data_usage = defaultdict(int)
previous_data_usage = defaultdict(int)

def update_usage():
    while True:
        app_data_usage.clear()

        # Iterate over all active connections
        connections = psutil.net_connections(kind='inet')
        for conn in connections:
            if conn.status == 'ESTABLISHED' and conn.raddr:
                pid = conn.pid
                if pid is not None:
                    try:
                        process = psutil.Process(pid)
                        app_name = process.name()
                        exe_path = process.exe()

                        # List of directories to whitelist
                        whitelist = [
                            "C:\\Program Files\\Google",
                            "C:\\Program Files\\Cloudflare",
                            "C:\\Program Files\\Epic Games"
                        ]

                        # Skip processes in Windows and Program Files unless whitelisted
                        if any(exe_path.startswith(path) for path in [
                            "C:\\Windows\\", 
                            "C:\\Program Files\\", 
                            "C:\\Program Files (x86)\\" 
                        ]) and not any(exe_path.startswith(path) for path in whitelist):
                            continue

                        # Get network usage for the process
                        net_usage = psutil.net_io_counters(pernic=False)
                        sent = net_usage.bytes_sent
                        recv = net_usage.bytes_recv

                        # Calculate delta usage
                        previous_total = previous_data_usage[app_name]
                        current_total = sent + recv
                        delta_usage = (current_total - previous_total) / (1024 * 1024) * 8  # Convert to Mbps

                        # Store the data usage for display
                        if delta_usage > 0:
                            app_data_usage[app_name] = delta_usage

                        # Update previous data
                        previous_data_usage[app_name] = current_total

                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
        
        time.sleep(1)  # Update every second

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(app_data_usage)

if __name__ == '__main__':
    threading.Thread(target=update_usage, daemon=True).start()
    app.run(debug=True, use_reloader=False)
