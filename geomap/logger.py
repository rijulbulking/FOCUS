import psutil
import csv
import time

# CSV file name
csv_file = 'network_data_log.csv'

# Write CSV headers
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time Elapsed (s)', 'Inbound Data (KB/s)', 'Outbound Data (KB/s)'])

# Function to get the current network I/O
def get_network_data():
    net_io = psutil.net_io_counters()
    return net_io.bytes_recv, net_io.bytes_sent

# Convert bytes to kilobytes and round to 2 decimal places
def bytes_to_kb(bytes_value):
    return round(bytes_value / 1024, 2)

# Initial time and network usage to calculate elapsed time and data speed
start_time = time.time()
prev_inbound, prev_outbound = get_network_data()

# Infinite loop to log data every second
try:
    while True:
        # Sleep for 1 second
        time.sleep(1)
        
        # Get current time and network data
        current_time = time.time()
        elapsed_time = int(current_time - start_time)
        
        current_inbound, current_outbound = get_network_data()
        
        # Calculate inbound and outbound speeds (KB/s)
        inbound_speed = bytes_to_kb(current_inbound - prev_inbound)
        outbound_speed = bytes_to_kb(current_outbound - prev_outbound)
        
        # Update previous values for the next iteration
        prev_inbound, prev_outbound = current_inbound, current_outbound
        
        # Log the data to the CSV file
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([elapsed_time, inbound_speed, outbound_speed])
        
        # Print the results (optional)
        print(f"Time Elapsed: {elapsed_time}s | Inbound: {inbound_speed} KB/s | Outbound: {outbound_speed} KB/s")
        
except KeyboardInterrupt:
    print("\nMonitoring stopped.")
