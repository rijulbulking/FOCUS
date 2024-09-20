import socket

port = int(input('Enter port to be opened: '))

# create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a specific port
sock.bind(('localhost', port))

# start listening for incoming connections
sock.listen()

print(f"Listening on port {port}")

# accept incoming connections and print the client address
while True:
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")