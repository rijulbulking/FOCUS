import time, threading
from functions import singlePortScanner, OpenPorts, WhitelistedPortsList

print('Port scanner is Running...')

# Port scanning
start = time.time()
for port in range(1, 65536):
    if port in WhitelistedPortsList:
        continue
    thread = threading.Thread(target=singlePortScanner, args=[port])
    thread.start()
thread.join()
end = time.time()


if len(OpenPorts) == 0:
    print('No port detected.')
input(f'Scan Complete\nTime taken: {end-start} seconds\n')