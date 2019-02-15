try:
    import neopixel as neo
except:
    print("Warning: Could not import neopixel module. Are you woking offline?")

from time import sleep
import colorsys as cs
import math
import numpy as np
import graphics  # graphics.py
import random
from math import sqrt
#import colorutils as cu

# some default colors 
# white    = Color(255, 255, 255)
# black    = Color(0, 0, 0)
# red      = Color(255, 0, 0)
# green    = Color(0, 255, 0)
# blue     = Color(0, 0, 255)
# pink     = Color(255, 102, 178)
# lime     = Color(102, 255, 102)
# electric = neo.Color(126, 249, 255)
# tiger    = neo.Color(253, 106, 2)
# teal     = neo.Color(0, 128, 129)


class Color:
    '''
    A color of the LED floor
    '''
    def __init__(self, r, g, b, a=1):
        # TODO: accept other color types, too
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        
    def __str__(self):
        return str("%s%s%s%s" % (self.r, self.g, self.b, self.a))

    def __blendColorValue(self, a, b, t):
        return sqrt((1 - t) * a**2 + t * b**2)

    def __blendAlphaValue(self, a, b, t):
        return (1-t)*a + t*b

    def __add__(self, otherColor):
        t = 0.5 # point along the blend [0, 1]
        r = self.__blendColorValue(self.r, otherColor.r, t)
        g = self.__blendColorValue(self.g, otherColor.g, t)
        b = self.__blendColorValue(self.b, otherColor.b, t)
        a = self.__blendAlphaValue(self.a, otherColor.a, t)
        return Color(r, g, b, a)

    def __repr__(self):
        return str(self)



class Layer:
    '''
    A layer of the LED floor

    When it comes to setting colors directly, we are outsourcing all the
    heavy lifting to numpy. That is, we use numpy functions and numpy indexing
    on Layer.color to update the color values directly

    Args:
        height (int): height of the layer (number of rows)
        width (int): width of the layer (number of columns)
        tick_fun (function): function to call on each tick
    '''
    def __init__(self, height, width, tick_fun=None, name=None, visible=True, offset=[0,0], **kwargs):
        self.height = height
        self.width = width
        self.colors = np.full([self.height, self.width], None)
        self.tick_fun = tick_fun
        self.name = name
        self.visible = visible
        self.offset = offset

        for key, value in kwargs.items():
            setattr(self, key, value) 
            
    def tick(self):
        ''' The update function that gets called on every tick. Normally this will
        be once per refresh of the LED floor '''
        if self.tick_fun:
            self.tick_fun(self)

    def __add__(self, otherLayer):
        # TODO: add colors of the two layers, return a new layer
        return self

    def __mul__(self, otherLayer):
        # ToDo: multiply (blend) colors of the two layers, return a new layer
        return self   

    def set_all(self, color):
        ''' Set ALL LEDs to the same color 
        '''
        self.colors = np.full([self.height, self.width], color)
        return self # useful for chaining functions

    def __str__(self):
        return str(self.colors)

    def __getitem__(self, index):
        return colors.__getitem__[index]

    # def get_column_coords(self, x):
    #     col = [[x,y] for x,y in zip([x] * self.width, range(self.height))]
    #     return col

    # def get_row_coords(self, y):
    #     row = [[x,y] for x,y in zip(range(self.width), [y] * self.height)]
    #     return row

    

class LedFloor:
    '''
    A class for working with the ko-lab LED floor

    Args:
        strip (neopixel Adafruit_NeoPixel object): The LED strip to woork with
    '''
    def __init__(self, strip, height, width, flip_x = False, flip_y = False, 
        flip_axes = False, preview = True):

        self.strip     = strip
        self.flip_x    = flip_x
        self.flip_y    = flip_y
        self.flip_axes = flip_axes
        self.height    = height if not self.flip_axes else width
        self.width     = width if not self.flip_axes else height
        self.n_leds    = self.width + self.height
        self.layers    = [] # left to right = bottom to top layer
        self.colors    = Layer(self.height, self.width)
        self.preview   = preview

        if self.preview:
            # create preview window
            self.win = graphics.GraphWin("Preview", self.width * 30, self.height * 30)
            self.win.autoflush = False
            self.win.yUp()
            self.preview_colors = np.full([self.height, self.width], None)
            for x in range(self.width):
                for y in range(self.height):
                    corner1 = graphics.Point(x*30, y*30)
                    corner2 = graphics.Point(x*30+30, y*30+30)
                    self.preview_colors[x,y] = graphics.Rectangle(corner1, corner2)
                    self.preview_colors[x,y].setFill('black')
                    self.preview_colors[x,y].draw(self.win)

        self.__led_nr_map = self.__make_led_nr_map()    
        self.clear() 

        try:
            self.strip.show()
        except:
            print("Warning: Cannot connect to LED strip!")   

    def __getitem__(self, index):
        return self.layers[index]

    def __len__(self):
        return len(self.layers)

    def __str__(self):
        txt = "LedFloor object with %d Layers" % len(self)
        for i, layer in enumerate(self.layers):
            txt = txt + '\n %d - %s' % (i, layer.name)
        return txt

    def add_layer(self, layer):
        assert isinstance(layer, Layer)
        self.layers.append(layer)

    def tick(self):
        ''' update all layers using their tick functions (if any) 
        '''
        for layer in self.layers:
            layer.tick()

    def flatten_colors(self):
        ''' flatten all layers using color blending
        '''
        # TODO; Add layers from bottom to top
        a = self.layers[0].colors
        b = self.layers[1].colors
        c = self.layers[2].colors
        a[a == None] = Color(0,0,0,0)
        b[b == None] = Color(0,0,0,0)
        c[c == None] = Color(0,0,0,0)
        flattened = np.add(a, b)
        flattened = np.add(flattened, c)
        return flattened

    def draw(self):
        ''' refresh the LED strip to show new colors 
        '''
        colors = self.flatten_colors()
        
        if self.preview:
            # draw matrix to screen
            for x in range(self.width):
                for y in range(self.height):
                    col = colors[x, y]
                    
                    col = graphics.color_rgb(int(col.r), int(col.g), int(col.b))
                    self.preview_colors[x,y].setFill(col)
            
            # TODO: also draw representation of LED strip to screen
            self.win.flush()

        # set colors on LED strip
        # try:
        #     for x in range(self.width):
        #             for y in range(self.height):
        #                 led_nr = self.__led_nr_map[x,y]
        #                 col = colors[x, y]
        #                 self.strip.setPixelColor(led_nr, colors[x, y])   
        #     self.strip.show()
        # except:
        #     pass

    def clear(self):
        background = (Layer(self.height, self.width, name="Background")
                        .set_all(Color(0,0,0)))
        self.layers = []
        self.layers.append(background)

    def __make_led_nr_map(self):
        ''' convert [x,y] coordinates of the LED matrix into corresponding 
        LED number of the LED strip
        '''
        led_nr_map = np.full([self.height, self.width], None)
        for x in range(self.width):
            for y in range(self.height):
                led_nr_map[y,x] = self.__coords_to_led_nr([x,y])
                # This is becoming messy becaiue numpy uses matrix indexing, and I use cartesian xy... mhhh..
        return led_nr_map

    def __coords_to_led_nr(self, coords):
        x     = coords[0] if not self.flip_axes else coords[1]
        y     = coords[1] if not self.flip_axes else coords[0]
        xpos  = x if not self.flip_x else (self.width) - (x+1)
        ypos  = y if not self.flip_y else (self.height) - (y+1)
        return int(ypos * self.height) + int(xpos)



def axis_test(floor):
    electric = Color(126, 249, 255)
    tiger = Color(253, 106, 2)
    white = Color(255, 255, 255, 0.5)
    black = Color(0, 0, 0, 0.5)

    floor.clear()
    floor[0].set_all(electric)

    for i in range(floor.width):
        floor[0].colors[i, 0:i+1] = tiger 

    def move_dot(ly):
        ly.lastpos = ly.pos.copy()
        
        ly.colors[ly.lastpos[0], ly.lastpos[1]] = None

        if ly.pos[0] >= floor.width-1:
            ly.pos[0] = 0
            ly.pos[1] = (ly.pos[1] + 1) % ly.height
        else:
            ly.pos[0] = ly.pos[0] + 1
            ly.pos[1] = ly.pos[1]
  
        ly.colors[ly.pos[0], ly.pos[1]] = electric

    animationLayer1 = Layer(floor.width, floor.height, move_dot, pos = [0, 0], lastpos = [0, 0]) 
    floor.add_layer(animationLayer1)
    animationLayer2 = Layer(floor.width, floor.height, move_dot, pos = [3, 3], lastpos = [3, 3]) 
    floor.add_layer(animationLayer2)

    while True:
        floor.tick()
        floor.draw()
        sleep(1/30)



# def demo(self):
#     ''' "Show me what you gaaaaat!"
#     '''
#     self.clear()
    
#     state = [[[0,0,0]] * self.width] * self.height
#     stepsize = (1.0/self.n_leds)
#     lednr = 0
#     for x in range(self.width):
#         for y in range(self.height):
#             h_start = (0 + lednr * (2*stepsize)) % 1 #* (y*self.width + x)
#             lednr = lednr + 1
#             s_start = 0
#             v_start = 1
#             hsv = [h_start,s_start,v_start]
#             state[x][y] = hsv
#             self.set([x,y], hsv_to_neopixel_color(hsv[0], hsv[1], hsv[2]))

#     tint = 0
#     while(True): 
#         for x in range(self.width):
#             for y in range(self.height):
#                 hsv = state[x][y]

#                 new_h = (hsv[0] + stepsize/60.0) % 1.0
#                 new_s = (hsv[1] + stepsize/20.0) % 1.0
#                 new_v = hsv[2] #+ stepsize/20.0) % 1.0

#                 state[x][y][0] = new_h
#                 state[x][y][1] = new_h
#                 state[x][y][2] = new_v

#                 self.set([x,y], hsv_to_neopixel_color(
#                     (translate(new_h, 0.0, 1.0, 0.0, 0.1) + tint) % 1.0, 
#                     to_sine(new_s), 
#                     new_v))
                
#         tint = (tint + stepsize/20.0) % 1

#         self.draw()
#         sleep(1.0/40)





# def set(self, coords, colors):
# ''' set LEDs at coordinate(s) to given color(s) '''
#     if all(isinstance(e, list) for e in coords):
#         # unpack list of coordinates
#         for e, c in zip(coords, colors):
#            self.set(e, c)
#     else:
#         led_nr = self.pos_to_led_nr(coords)
#         #print "Setting LED at [%d, %d] (nr. %d) to color %s" % (coords[0], coords[1], led_nr, colors)
#         self.strip.setPixelColor(led_nr, colors)   



        

# def hsv_to_neopixel_color(h, s, v):
#     rgb = [int(round(e * 255, 0)) for e in cs.hsv_to_rgb(h, s, v)]
#     rgb = neo.Color(rgb[0], rgb[1], rgb[2])
#     return rgb


# def translate(value, leftMin, leftMax, rightMin, rightMax):
#             # Figure out how 'wide' each range is
#             leftSpan = leftMax - leftMin
#             rightSpan = rightMax - rightMin
#             # Convert the left range into a 0-1 range (float)
#             valueScaled = float(value - leftMin) / float(leftSpan)
#             # Convert the 0-1 range into a value in the right range
#             res = rightMin + (valueScaled * rightSpan)
#             return res


# def to_sine(x):
#     ''' maps range 0, 1 to sine function
#     '''
#     res = (math.sin(math.pi * x))
#     return res


