import unittest
import ledfloor as lf
import numpy as np
import graphics

class LedFloorTests(unittest.TestCase):
    def setUp(self):
        self.floor = lf.LedFloor(None, 3, 3)

    def test_create_floor(self):
        self.assertTrue(len(self.floor.layers), 1)
        self.assertTrue(isinstance(self.floor.layers[0], lf.Layer))
        self.assertEqual(self.floor.layers[0].name, "Background")

    def test_create_layer(self):
        layer = lf.Layer(3,3, name="Foreground")
        self.assertTrue(isinstance(layer, lf.Layer))
        self.floor + layer
        self.assertEqual(self.floor.layers[1].name, "Foreground")

    # def test_add(self):
    #     self.floor + 
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)


if __name__ == '__main__':
    floor = lf.LedFloor(None,11,11, preview=True)
    lf.axis_test(floor)
    # unittest.main()

    # from colorama import init
    # colorama.init()
    # from colorama import init
    # init()
    # from colored import fg, bg, fore, back, attr, style

    # print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')

    # color = fg('#C0C0C0') + bg('#00005f')
    # print(str(color))
    # res = attr('reset')
    # print (color + "Hello World !!!" + res)

    # print (fore.RED + back.YELLOW + style.BOLD + "Hello World !!!" + style.RESET)   
    # print (fg.LIGHT_BLUE + bg.RED + style.BOLD + "Hello World !!!" + style.RESET)
    # print ('%s Hello World !!! %s' % (fg(1), attr(0)))

    # from sty import fg, bg, ef, rs, RgbFg, RgbBg

    # foo = fg.red + 'This is red text!' + fg.rs
    # bar = bg.magenta + 'This has a blue background!' + bg.rs
    # qui = fg(255, 10, 10) + 'This is red text using 24bit colors.' + bg.rs

    # # Add new colors:

    # bg.set_style('orange', RgbBg(255, 150, 50))

    # buf = bg.orange + 'Yay, Im orange.' + bg.rs

    # print(foo, bar, qui, buf, sep='\n')
