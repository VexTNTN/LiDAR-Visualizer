import random
import socket
import struct

from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from matplotlib.animation import FuncAnimation

s = socket.socket()

port = 12345
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
print(s.recv(1024).decode())

image = mpimg.imread("H2H.png")

plt.figure(figsize=(10, 10))
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

ax = plt.gca()
ax.imshow(image, extent=[-72,72,-72,72])
ax.set_xticks(range(-72, 73, 12))
ax.set_yticks(range(-72, 73, 12))

scat = ax.scatter([], [], color='red')

def get_packet() -> list[tuple[float, float]]:
    while True:
        size_prefix = s.recv(2)
        if size_prefix:
            packet_items = struct.unpack('H', size_prefix)[0]
            print(packet_items)
            float_list = struct.unpack(f'{packet_items}e', s.recv(packet_items * 2))

            coordinates = [(float_list[i], float_list[i + 1]) for i in range(0, len(float_list), 2)]
            print('Received tuple list:', coordinates)
            return coordinates

def update(frame):
    fakeData = get_packet()
    scat.set_offsets(fakeData)
    return scat,

ani = FuncAnimation(plt.gcf(), update, frames=100, interval=1000, repeat=False)

plt.show()


