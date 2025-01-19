# server in this case is the raspberry pi
import socket
import struct
import ctypes
import random
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
    
    c.send('Thank you for connecting'.encode()) 

    # buf = (ctypes.c_float * 2 * len(floatList))()
    # buf[:] = floatList
    for i in range(5):
        floatList = [(random.uniform(-72, 72), random.uniform(-72, 72)) for _ in range(100)]
        flattenedList = [item for sublist in floatList for item in sublist]
        buf = struct.pack(f'H{len(flattenedList)}e', len(flattenedList), *flattenedList)
        print(struct.calcsize(f'H{len(flattenedList)}e'))
        c.send(buf)
        sleep(5)

    c.close()
    break
