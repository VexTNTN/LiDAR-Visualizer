import dearpygui.dearpygui as dpg
import math
import time
import collections
import threading
import pdb
import socket
import struct
import base64

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

is_logging = False
log_file = None

def get_packet() -> list[tuple[float, float]]:
    """
    Receives a packet from a socket, unpacks it into a list of 
    coordinate tuples, and optionally logs the raw packet data to a file.
    Returns:
        list[tuple[float, float]]: A list of (x, y) coordinate tuples 
        extracted from the packet. Returns an empty list if no packet 
        is received within 0.5 seconds.
    """

    startTime = time.time()
    while True:
        if (time.time() - startTime) > 0.5:
            return []
        size_prefix = s.recv(2)
        if size_prefix:
            # get the number of items in the packet as an unsigned short (2 bytes)
            packet_items = struct.unpack('H', size_prefix)[0]
            packet = s.recv(packet_items * 2)
            # logs the data to a file if the recording button is pressed
            if is_logging and log_file:
                # open the file in append and binary mode, then write the packet straight from the socket
                log_file.write(packet)
            # unpack the packet into a list of floats [x, y, x, y, ...]
            float_list = struct.unpack(f'{packet_items}e', packet)

            coordinates = [(float_list[i], float_list[i + 1])
                           for i in range(0, len(float_list), 2)]
            return coordinates


def update_data():
    sample = 1
    startTime = time.time()
    lastUpdateTime = startTime
    iters = 0
    while True:
        dataPacket = get_packet()
        if dataPacket == []:
            print("Finished")
            # print(time.time() - startTime)
            break

        # set the series x and y to the last nsamples
        dpg.set_value('series_tag', [[coord[0] for coord in dataPacket], [
                      coord[1] for coord in dataPacket]])
        # updating the fps counter 30 times a second
        if time.time() - lastUpdateTime > 1/30:
            try:
                dpg.set_value('fps', str(
                    iters / (time.time() - lastUpdateTime)))
                lastUpdateTime = time.time()
                iters = 0
            except:
                pass

        # Delay to keep the framerate at a certain value, but it wont be exaclty that value
        # because of the time it takes to process the data
        time.sleep(1/500.0)
        sample = sample+1
        iters += 1


def log_data():
    """
    Toggles the logging state and updates the label of the logging button.
    If the logging button label is 'Stop Recording', it changes the label to 'Start Recording',
    sets the global variable `is_logging` to False, and prints a message indicating that logging has stopped.
    Otherwise, it changes the label to 'Stop Recording', sets `is_logging` to True, clears the contents of 'log.bin',
    and prints a message indicating that logging has started.
    """
    global is_logging, log_file
    if dpg.get_item_label('logging') == 'Stop Recording':
        dpg.set_item_label('logging', 'Start Recording')
        is_logging = False
        if log_file:
            log_file.close()
            log_file = None
        print('Stopped logging data')
    else:
        dpg.set_item_label('logging', 'Stop Recording')
        is_logging = True
        open('log.bin', 'w').close()
        log_file = open('log.bin', 'ab')
        print('Logging data')


dpg.create_context()

width, height, channels, data = dpg.load_image("H2H.png")

with dpg.texture_registry(show=False):
    dpg.add_static_texture(width, height, default_value=data, tag="H2H")

with dpg.window(label='Tutorial', tag='Primary', width=1000, height=1000, no_title_bar=True):
    # dpg.add_image("H2H", width=1000, height=1000)
    dpg.add_button(label='Start Recording', tag='logging', callback=log_data)
    dpg.add_same_line()
    dpg.add_text(tag='fps_label', default_value='FPS: ')
    dpg.add_same_line()
    dpg.add_text(tag='fps', default_value='0')

    with dpg.plot(label='Line Series', height=-1, width=-1):
        # optionally create legend
        # dpg.add_plot_legend()

        # REQUIRED: create x and y axes, set to auto scale.
        with dpg.plot_axis(dpg.mvXAxis, label='x', tag='x_axis'):
            dpg.add_image_series("H2H", [-74, -74], [74, 74])
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label='y', tag='y_axis')

        # series belong to a y axis. Note the tag name is used in the update
        # function update_data
        dpg.add_scatter_series(x=list((0,)), y=list((0,)),
                               label='Temp', parent='y_axis',
                               tag='series_tag')
        dpg.set_axis_limits('x_axis', -74, 74)
        dpg.set_axis_limits('y_axis', -74, 74)
        # Sets the ticks for the x and y axis
        dpg.set_axis_ticks('x_axis', tuple((str(i), i)
                           for i in range(-72, 73, 12)))
        dpg.set_axis_ticks('y_axis', tuple((str(i), i)
                           for i in range(-72, 73, 12)))


def resize():
    # keep the aspect ratio of the dpg window a square
    width = dpg.get_viewport_width()
    height = dpg.get_viewport_height()
    dpg.set_viewport_height(min(width, height))
    dpg.set_viewport_width(min(width, height))


dpg.create_viewport(title='Custom Title', width=1000,
                    height=1000, resizable=True)
dpg.set_viewport_resize_callback(resize)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('Primary', True)

thread = threading.Thread(target=update_data)
thread.start()
dpg.start_dearpygui()

dpg.destroy_context()
