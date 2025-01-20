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

fig, ax = plt.subplots(figsize=(10, 10))
# ax.imshow(image, extent=[-72,72,-72,72])
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
ax.set_xticks(range(-72, 73, 12))
ax.set_yticks(range(-72, 73, 12))
ax.grid(True)
scat, = ax.plot([], [], color='red', ms=1, marker='o', ls='')
plt.show(block=False)


def get_packet() -> list[tuple[float, float]]:
    while True:
        size_prefix = s.recv(2)
        if size_prefix:
            packet_items = struct.unpack('H', size_prefix)[0]
            print(packet_items)
            float_list = struct.unpack(f'{packet_items}e', s.recv(packet_items * 2))

            coordinates = [(float_list[i], float_list[i + 1]) for i in range(0, len(float_list), 2)]
            # print('Received tuple list:', coordinates)
            return coordinates

def draw():
    for i in range(50):
        fakeData = get_packet()
        x = [coord[0] for coord in fakeData]
        y = [coord[1] for coord in fakeData]
        scat.set_data(x, y)
        ax.draw_artist(ax.patch)
        ax.draw_artist(scat)
        fig.canvas.draw()
        fig.canvas.flush_events()
