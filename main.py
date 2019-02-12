""" control the LED floor with OSC messages
"""

import ledfloor as lf
import neopixel as neo
import OSC
import time
from time import sleep
import random
import osccontroller as oc

board_height = 11
board_width = 11

# LED strip configuration
LED_COUNT      = board_height * board_width 
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = neo.ws.WS2811_STRIP_GRB 

strip = neo.Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
    LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

floor = lf.LedFloor(strip, board_height, board_width, flip_x=True)

floor.clear()
floor.axis_test()
sleep(2)
floor.clear()
#sleep(1)
#floor.demo() # rainbow demo, runs forever


# create server (not started yet)
server = oc.create_osc_server('10.90.154.80', 4559)

# register handlers for OSC messages
# (More a proof of concept than anything at the moment....)
def position_handler(addr, tags, data, source):
    # takes an xy coordinate and draws a cross to that coordinate
    global cross_color
    x = int(round(data[0],0))
    y = int(round(data[1],0))

    coord = [x, y]
    color = cross_color #random.choice([lf.electric, lf.tiger, lf.teal, lf.lime])

    floor.clear()
    floor.set(floor.get_column_coords(x), [color]*floor.height) 
    floor.set(floor.get_row_coords(y), [color]*floor.width)   
    floor.draw()


def shoot_handler(addr, tags, data, source):
    global cross_color
    cross_color = lf.tiger
    sleep(1)
    cross_color = lf.electric


cross_color = lf.electric
  
server.addMsgHandler("/set", position_handler)
server.addMsgHandler("/shoot", shoot_handler)
oc.print_handlers(server) # Did it work?

# Let's go!
oc.start_osc_server(server)