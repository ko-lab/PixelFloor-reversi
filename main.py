import ledfloor as lf
import neopixel as neo

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

floor = lf.LedFloor(strip, board_height, board_width, flip_x=False)

# some default colors 
white = neo.Color(255, 255, 255)
black = neo.Color(0, 0, 0)
red   = neo.Color(255, 0, 0)
green = neo.Color(0, 255, 0)
blue  = neo.Color(0, 0, 255)
pink  = neo.Color(255, 102, 178)

floor.clear()
floor.demo()

#floor.set_all(pink)
#floor.set([0,0], red)
#floor.set([1,1], green)
#floor.set([1,2], blue)
#floor.draw()

