import time
from functions import singlePortScanner, OpenPorts, WhitelistedPortsList

print('Port scanner is Running...')

# Port scanning via multi-thread distribution
start = time.time()
for port in range(1, 65536):
    if port in WhitelistedPortsList:
        continue

    singlePortScanner(port)
end = time.time()

#Message formatting
message = ''
for port in OpenPorts:
    message = message + str(port) + '\n'

if len(OpenPorts) == 0:
    print('No port detected.')
input('Scan Complete\n')
