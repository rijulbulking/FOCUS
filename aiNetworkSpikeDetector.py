import psutil, csv, time, joblib
import pandas as pd


#importing ai models
inboundModel = joblib.load('inboundModel.joblib')
outboundModel = joblib.load('outboundModel.joblib')

# Function to get the current network I/O
def get_network_data():
    net_io = psutil.net_io_counters()
    return net_io.bytes_recv, net_io.bytes_sent

# Convert bytes to megabits per second and round to 2 decimal places
def bytes_to_mbps(bytes_value):
    kb_value = bytes_value / 1024  # Convert bytes to kilobytes
    mbps_value = (kb_value * 8) / 1000  # Convert kilobytes to Mbps
    return round(mbps_value, 2)

# Initial time and network usage to calculate elapsed time and data speed
start_time = time.time()
prev_inbound, prev_outbound = get_network_data()

# Infinite loop to log data every second
spikesDetected = 0
try:
    while True:
        # Sleep for 1 second
        time.sleep(1)
        
        # Get current time and network data
        current_time = time.time()
        elapsed_time = int(current_time - start_time)
        input_data = pd.DataFrame([[elapsed_time - 1]], columns=["elapsed_time"])
        
        current_inbound, current_outbound = get_network_data()
        
        # Calculate inbound and outbound speeds (Mbps)
        inbound_speed = bytes_to_mbps(current_inbound - prev_inbound)
        outbound_speed = bytes_to_mbps(current_outbound - prev_outbound)
        inboundPrediction = inboundModel.predict(input_data)
        outboundPrediction = outboundModel.predict(input_data)
        
        if inbound_speed-outbound_speed > 3:
            spikesDetected+=1
        else:
            spikesDetected = 0

        if spikesDetected == 3:
            print('Warning, Network Surge detected!')

        
        # Update previous values for the next iteration
        prev_inbound, prev_outbound = current_inbound, current_outbound
        
        # Print the results (optional)
        print(f"Time Elapsed: {elapsed_time}s | Inbound: {inbound_speed} Mbps | Outbound: {outbound_speed} Mbps")
        print(f"Time Elapsed: {elapsed_time}s | Predicted Inbound: {round(inboundPrediction[0], 2)} Mbps | Predicted Outbound: {round(outboundPrediction[0], 2)} Mbps")
        print()

except KeyboardInterrupt:
    print("\nMonitoring stopped.")



# data = pd.read_csv('network_data_log.csv')
# X = data[['elapsed_time']]
# Y_inbound = data['inbound_data']
# Y_outbound = data['outbound_data']

# inboundPrediction = inboundModel.predict([ [n-1] ])
# outboundPrediction = outboundModel.predict([ [ n-1] ])


# print(f'Actual download: {Y_inbound.iloc[n-1]}')
# print(f'Predicted download: {inboundPrediction}')
# print(f'Actual upload: {Y_outbound.iloc[n-1]}')
# print(f'Predicted upload: {outboundPrediction}')