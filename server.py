# server in this case is the raspberry pi
import socket
import struct
import ctypes
import random
import numpy as np
from time import sleep 
 
s = socket.socket()         
print ("Socket successfully created")
 
port = 12345               
 
s.bind(('', port))         
print ("socket binded to %s" %(port)) 

 
s.listen(5)     
print ("socket is listening")            
 
while True: 
    c, addr = s.accept()     
    # Establish connection with client.
    print ('Got connection from', addr )
    
    # Initial handshake communication with the client -- Delete at some point
    c.send('Thank you for connecting'.encode()) 

    # buf = (ctypes.c_float * 2 * len(floatList))()
    # buf[:] = floatList
    shift = 0
    dir = 1
    while True:
        interval = np.arange(-10, 10, 0.04) + shift
        sinData = np.sin(interval) * 50
        sinData = [(x, y) for x, y in zip(interval, sinData)]

        # floatList = [(random.uniform(-72, 72), random.uniform(-72, 72)) for _ in range(500)]
        flattenedList = [item for sublist in sinData for item in sublist]
        buf = struct.pack(f'H{len(flattenedList)}e', len(flattenedList), *flattenedList)
        # print(struct.calcsize(f'H{len(flattenedList)}e'))
        try:
            c.send(buf)
        except:
            print('Connection closed')
            break
        shift += 0.1 * dir
        if shift > 50 or shift < -50:
            dir *= -1
        # sleep(1/60.0)
