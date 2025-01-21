# LiDAR Visualizer Work in Progress
This is a tool for realtime LiDAR visualization over the air from a microcomputer interfacing with a LiDAR sensor. It uses the TCP protocol to send data between the server (microcomputer/raspberry pi) and the client (the rendering computer). 

## Socket Specifications
See `client.py` for isolated example of retrieving data.

The client expects data sent over the socket connection to be formatted in a certain way:
- Each packet starts with a 2 byte unsigned short (0 to 65,535) *H* that denotes the *number of values the packet contains*, consider a value to be one x or y coordinate.
- The remaining *H * 2* bytes of data are alternating x and y coonrdiates.
- Each coordinate is a 2 byte float.
- Thus, for each packet you receive *H/2* points to be plotted.

## To-Do
- [ ] read and replay data from the log
- [ ] set up interfacing with the pi