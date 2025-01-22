# the pc receiving data

import socket
import struct
 
# Create a socket object 
s = socket.socket()         

# Define the port on which you want to connect 
port = 12345
 
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 

coordinates = []
 
# Initial handshake communication with the server -- Delete at some point
print(s.recv(1024).decode())
while True:
    size_prefix = s.recv(2)
    if size_prefix:
        packet_items = struct.unpack('!H', size_prefix)[0]
        print(packet_items)
        float_list = struct.unpack(f'!{packet_items}e', s.recv(packet_items * 2))

        coordinates = [(float_list[i], float_list[i + 1]) for i in range(0, len(float_list), 2)]
        print('Received tuple list:', coordinates)
