import neopixel as neo
from time import sleep
import colorsys as cs
import math
#import colorutils as cu

# some default colors 
white = neo.Color(255, 255, 255)
black = neo.Color(0, 0, 0)
red   = neo.Color(255, 0, 0)
green = neo.Color(0, 255, 0)
blue  = neo.Color(0, 0, 255)
pink  = neo.Color(255, 102, 178)
lime  = neo.Color(102, 255, 102)
electric = neo.Color(126, 249, 255)
tiger = neo.Color(253, 106, 2)
teal = neo.Color(0, 128, 129)


class LedFloor:
    def __init__(self, strip, height, width, flip_x = False, flip_y = False, flip_axes = False):

        self.strip = strip
        self.strip.begin()
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.flip_axes = flip_axes

        self.height = height if not self.flip_axes else width
        self.width = width if not self.flip_axes else height
        self.n_leds = self.width + self.height
        #self.colors = [None] * (height * width) # TODO: Store current state

    def pos_to_led_nr(self, coord):
        """ convert [x,y] coordinates into corresponding LED number
        """
        x = coord[0] if not self.flip_axes else coord[1]
        y = coord[1] if not self.flip_axes else coord[0]
        xpos = x if not self.flip_x else (self.width) - (x+1)
        ypos = y if not self.flip_y else (self.height) - (y+1)
        assert x <= self.width and y <= self.height
        
        led_nr = int(ypos * self.height) + int(xpos)
        return led_nr 

    def set(self, coords, colors):
        """ set LEDs at coordinate(s) to given color(s)
        """
        if all(isinstance(e, list) for e in coords):
            # unpack list of coordinates
            for e, c in zip(coords, colors):
               self.set(e, c)
        else:
            led_nr = self.pos_to_led_nr(coords)
            #print "Setting LED at [%d, %d] (nr. %d) to color %s" % (coords[0], coords[1], led_nr, colors)
            self.strip.setPixelColor(led_nr, colors)       

    def set_all(self, color):
        """ Set ALL LEDs to the same color
        """
        for x in range(self.width):
            for y in range(self.height):
                self.set([x,y], color)
    
    def draw(self):
        """ refresh the LED strip to show new colors 
        """
        self.strip.show()

    def clear(self):
        """ Set all LEDs to black (no light)
        """
        black = neo.Color(0,0,0)
        self.set_all(black)
        self.draw()

    def get_column_coords(self, x):
        col = [[x,y] for x,y in zip([x] * self.width, range(self.height))]
        return col

    def get_row_coords(self, y):
        row = [[x,y] for x,y in zip(range(self.width), [y] * self.height)]
        return row

    def axis_test(self):
        electric = neo.Color(126, 249, 255)
        tiger = neo.Color(253, 106, 2)
        black = neo.Color(0, 0, 0)
        royal = neo.Color(29, 41, 81)

        for i in range(self.width):
            self.set(self.get_column_coords(i), [tiger]*i + [electric]*(self.height-i))    
        
        self.draw()

    def demo(self):
        """ "Show me what you gaaaaat!"
        """
        self.clear()

        white = neo.Color(255, 255, 255)
        black = neo.Color(0, 0, 0)
        red   = neo.Color(120, 0, 0)
        green = neo.Color(0, 255, 0)
        blue  = neo.Color(0, 0, 255)
        pink  = neo.Color(255, 102, 178)
        
        state = [[[0,0,0]] * self.width] * self.height
        stepsize = (1.0/self.n_leds)
        lednr = 0
        for x in range(self.width):
            for y in range(self.height):
                h_start = (0 + lednr * (2*stepsize)) % 1 #* (y*self.width + x)
                lednr = lednr + 1
                s_start = 0
                v_start = 1
                hsv = [h_start,s_start,v_start]
                state[x][y] = hsv
                self.set([x,y], hsv_to_neopixel_color(hsv[0], hsv[1], hsv[2]))

        tint = 0
        while(True): 
            for x in range(self.width):
                for y in range(self.height):
                    hsv = state[x][y]

                    new_h = (hsv[0] + stepsize/60.0) % 1.0
                    new_s = (hsv[1] + stepsize/20.0) % 1.0
                    new_v = hsv[2] #+ stepsize/20.0) % 1.0

                    state[x][y][0] = new_h
                    state[x][y][1] = new_h
                    state[x][y][2] = new_v

                    self.set([x,y], hsv_to_neopixel_color(
                        (translate(new_h, 0.0, 1.0, 0.0, 0.1) + tint) % 1.0, 
                        to_sine(new_s), 
                        new_v))
                    
            tint = (tint + stepsize/20.0) % 1

            self.draw()
            sleep(1.0/40)

        

def hsv_to_neopixel_color(h, s, v):
    rgb = [int(round(e * 255, 0)) for e in cs.hsv_to_rgb(h, s, v)]
    rgb = neo.Color(rgb[0], rgb[1], rgb[2])
    return rgb


def translate(value, leftMin, leftMax, rightMin, rightMax):
            # Figure out how 'wide' each range is
            leftSpan = leftMax - leftMin
            rightSpan = rightMax - rightMin
            # Convert the left range into a 0-1 range (float)
            valueScaled = float(value - leftMin) / float(leftSpan)
            # Convert the 0-1 range into a value in the right range
            res = rightMin + (valueScaled * rightSpan)
            return res


def to_sine(x):
    """ maps range 0, 1 to sine function
    """
    res = (math.sin(math.pi * x))
    return res


