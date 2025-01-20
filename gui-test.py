import dearpygui.dearpygui as dpg
import math
import time
import collections
import threading
import pdb
import socket
import struct

nsamples = 500


s = socket.socket()

port = 12345
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
print(s.recv(1024).decode())

# global data_y
# global data_x
# # Can use collections if you only need the last 100 samples
# data_y = collections.deque([0.0, 0.0],maxlen=nsamples)
# data_x = collections.deque([0.0, 0.0],maxlen=nsamples)

# Use a list if you need all the data. 
# Empty list of nsamples should exist at the beginning.
# Theres a cleaner way to do this probably.
# data_y = [0.0] * nsamples
# data_x = [0.0] * nsamples


def get_packet() -> list[tuple[float, float]]:
    startTime = time.time()
    while True:
        if (time.time() - startTime) > 0.5:
            return []
        size_prefix = s.recv(2)
        if size_prefix:
            packet_items = struct.unpack('H', size_prefix)[0]
            # print(packet_items)
            float_list = struct.unpack(f'{packet_items}e', s.recv(packet_items * 2))

            coordinates = [(float_list[i], float_list[i + 1]) for i in range(0, len(float_list), 2)]
            # print('Received tuple list:', coordinates)
            return coordinates
        

def update_data():
    sample = 1
    t0 = time.time()
    frequency=1.0
    startTime = time.time()
    iters = 0
    while True:

        # Get new data sample. Note we need both x and y values
        # if we want a meaningful axis unit.
        # t = time.time() - t0
        # y = math.sin(2.0 * math.pi * frequency * t)
        # data_x.append(t)
        # data_y.append(y)

        fakeData = get_packet()
        if fakeData == []:
            print("Finished")
            print(time.time() - startTime)
            break

        #set the series x and y to the last nsamples
        dpg.set_value('series_tag', [[coord[0] for coord in fakeData], [coord[1] for coord in fakeData]])          
        print(iters / (time.time() - startTime))
        # time.sleep(1/60.0)
        sample=sample+1
        iters += 1
           


dpg.create_context()
with dpg.window(label='Tutorial', tag='win',width=800, height=600):

    with dpg.plot(label='Line Series', height=-1, width=-1):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes, set to auto scale.
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, label='x', tag='x_axis')
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label='y', tag='y_axis')


        # series belong to a y axis. Note the tag name is used in the update
        # function update_data
        dpg.add_scatter_series(x=list((0,)),y=list((0,)), 
                            label='Temp', parent='y_axis', 
                            tag='series_tag')
        dpg.set_axis_limits('x_axis', -72, 72)
        dpg.set_axis_limits('y_axis', -72, 72)
        
            
                            
dpg.create_viewport(title='Custom Title', width=850, height=640)

dpg.setup_dearpygui()
dpg.show_viewport()

thread = threading.Thread(target=update_data)
thread.start()
dpg.start_dearpygui()

dpg.destroy_context()
