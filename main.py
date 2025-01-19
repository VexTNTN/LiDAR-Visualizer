import random

from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from matplotlib.animation import FuncAnimation

image = mpimg.imread("H2H.png")

plt.figure(figsize=(10, 10))
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

ax = plt.gca()
ax.imshow(image, extent=[-72,72,-72,72])
ax.set_xticks(range(-72, 73, 12))
ax.set_yticks(range(-72, 73, 12))

scat = ax.scatter([], [], color='red')



def update(frame):
    fakeData = [(random.randint(-72, 72), random.randint(-72, 72)) for _ in range(100)]
    scat.set_offsets(fakeData)
    return scat,

ani = FuncAnimation(plt.gcf(), update, frames=100, interval=10, repeat=False)

plt.show()
