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

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


while True:
    size_prefix = s.recv(2)
    if size_prefix:
        packet_items = struct.unpack('!H', size_prefix)[0]
        packet = recvall(s, packet_items * 4)
        if not packet:
            break
        print(packet_items)
        print(len(packet))
        float_list = struct.unpack(f'!{packet_items}f', packet)

        coordinates = [(float_list[i], float_list[i + 1]) for i in range(0, len(float_list), 2)]
        print('Received tuple list:', coordinates)



