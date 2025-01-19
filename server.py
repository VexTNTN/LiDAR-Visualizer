# server in this case is the raspberry pi
import socket
import struct
import ctypes
from struct import calcsize
 
s = socket.socket()         
print ("Socket successfully created")
 
port = 12345               
 
s.bind(('', port))         
print ("socket binded to %s" %(port)) 

floatList = [(0, 36), (36, 36), (36, 0), (-36, 0), (-36, -36), (0, -36)]
 
s.listen(5)     
print ("socket is listening")            
 
while True: 
    # Establish connection with client.
    c, addr = s.accept()     
    print ('Got connection from', addr )
    
    c.send('Thank you for connecting'.encode()) 

    # buf = (ctypes.c_float * 2 * len(floatList))()
    # buf[:] = floatList
    flattenedList = [item for sublist in floatList for item in sublist]
    buf = struct.pack(f'H{len(flattenedList)}e', len(flattenedList), *flattenedList)
    print(calcsize(f'H{len(flattenedList)}e'))
    c.send(buf)

    c.close()
    break
