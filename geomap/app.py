from flask import Flask, render_template, jsonify
import psutil
from collections import defaultdict
import threading
import time
import webbrowser

app = Flask(__name__)
app_data_usage = defaultdict(float)

def update_usage():
    last_data = defaultdict(lambda: (0, 0))

    while True:
        current_data = defaultdict(lambda: (0, 0))
        connections = psutil.net_connections(kind='inet')
        
        for conn in connections:
            if conn.status == 'ESTABLISHED' and conn.raddr:
                pid = conn.pid
                if pid is not None:
                    try:
                        process = psutil.Process(pid)
                        app_name = process.name()
                        bytes_sent, bytes_recv = process.io_counters()[:2]

                        current_data[app_name] = (bytes_sent, bytes_recv)

                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
        
        # Calculate current speed
        for app_name, (current_sent, current_recv) in current_data.items():
            last_sent, last_recv = last_data[app_name]
            sent_diff = current_sent - last_sent
            recv_diff = current_recv - last_recv

            app_data_usage[app_name] = ((sent_diff + recv_diff) * 8) / (1024 * 1024)  # Convert to Mbps

            last_data[app_name] = (current_sent, current_recv)

        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(app_data_usage)

if __name__ == '__main__':
    threading.Thread(target=update_usage, daemon=True).start()
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(debug=True, use_reloader=False)
