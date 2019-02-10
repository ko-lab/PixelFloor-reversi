import neopixel as neo
from time import sleep
import colorsys as cs

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


class LedFloor:
    def __init__(self, strip, height, width, flip_x = False, flip_y = False, flip_axes = False):

        self.strip = strip
        self.strip.begin()
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.flip_axes = flip_axes

        self.height = height if not self.flip_axes else width
        self.width = width if not self.flip_axes else height
        #self.colors = [None] * (height * width) # TODO: Store current state

    def pos_to_led_nr(self, coord):
        """ convert [x,y] coordinates into corresponding LED number
        """
        x = coord[0] if not self.flip_axes else coord[1]
        y = coord[1] if not self.flip_axes else coord[0]
        xpos = x if not self.flip_x else self.width - x
        ypos = y if not self.flip_y else self.height - y
        assert x <= self.width and y <= self.height
        
        led_nr = int(ypos * self.height) + int(xpos)
        return led_nr 

    def set(self, coords, colors):
        """ set LEDs at coordinate(s) to given color(s)
        """
        if all(isinstance(e, list) for e in coords):
            # unpack list of coordinates
            assert len(coords) == len(colors)
            for e, c in zip(coords, colors):
               self.set(e, c)
        else:
            led_nr = self.pos_to_led_nr(coords)
            print "Setting LED at [%d, %d] (nr. %d) to color %s" % (coords[0], coords[1], led_nr, colors)
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

    def demo(self):
        """ "Show me what you gaat!"
        """
        self.clear()

        white = neo.Color(255, 255, 255)
        black = neo.Color(0, 0, 0)
        red   = neo.Color(120, 0, 0)
        green = neo.Color(0, 255, 0)
        blue  = neo.Color(0, 0, 255)
        pink  = neo.Color(255, 102, 178)

        # for color in [red, green, blue]:
        #     self.clear()
        #     sleep(0.5)
        #     self.set_all(color)
        #     self.draw()
        #     sleep(0.5)
        #     self.clear()

        #     for x in range(self.width):
        #         for y in range(self.height):
        #             self.set([x,y], color)
        #             self.draw()
        #             sleep(0.01)

        
        self.clear()

        n_leds = self.width + self.height
        state = [[[0,0,0]] * self.width] * self.height
        stepsize = (1.0/n_leds)
        for y in range(self.width):
            for x in range(self.height):
                h_start = 0 + stepsize * self.pos_to_led_nr([x,y])
                s_start = 1
                v_start = 1
                state[x][y] = [h_start,s_start,v_start]

        while(True): 
            for y in range(self.width):
                for x in range(self.height):
                    hsv = state[x][y]
                    self.set([x,y], hsv_to_neopixel_color(hsv[0], hsv[1], hsv[2]))
                    state[x][y][0] = (state[x][y][0] + stepsize/3.0) % 1.0

            self.draw()
            sleep(1.0/30)

def hsv_to_neopixel_color(h, s, v):
    rgb = [int(round(e * 255, 0)) for e in cs.hsv_to_rgb(h, s, v)]
    rgb = neo.Color(rgb[0], rgb[1], rgb[2])
    return rgb
