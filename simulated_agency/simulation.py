
import sys

from random import randint
from time import time
from tkinter import *

# Linux doesn't have ImageGrab but we can use pyscreenshot instead
try:
    from PIL import ImageGrab
except:
    import pyscreenshot as ImageGrab


from .location import Location


class Simulation(object):
    '''
    Represents the universe in which our simulation unfolds.
    '''
    
    def __init__(self, width=None, height=None, cell_size=None):
        # Constants - do not change these directly after simulation instantiation
        self.canvas_width = width or 800
        self.canvas_height = height or 800
        self.cell_size = cell_size or 8
        
        # Computed properties
        self.width = int(self.canvas_width / self.cell_size)
        self.height = int(self.canvas_height / self.cell_size)

        # Preferences
        self.record_video = False

        # Wrapping
        self.wrap_x = True
        self.wrap_y = True

        # Initial values
        self.counter = 0

        # GUI
        self.window = Tk()
        self.window.resizable(False, False)
        self.canvas = Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg='black', bd=0, highlightthickness=0)
        self.canvas.pack()

        # Sane program termination
        def _quit():
            self.window.destroy()
            sys.exit()
        self.window.protocol("WM_DELETE_WINDOW", _quit)

    def set_cell_size(self, cell_size):
        '''
        Call this method instead of changing cell_size directly
        '''
        self.cell_size = cell_size
        self.width = int(self.canvas_width / self.cell_size)
        self.height = int(self.canvas_height / self.cell_size)

    def random_x(self):
        return randint(0, self.width - 1)

    def random_y(self):
        return randint(0, self.height - 1)

    def random_xy(self):
        return self.random_x(), self.random_y()

    def random_location(self):
        return Location(*self.random_xy())

    def draw(self, thing, fill=None):
        '''
        A very simple way to draw something
        '''

        # Location to draw
        x = thing.location.x
        y = thing.location.y

        # Colour to draw
        fill = fill or thing.colour()

        # Determine appropriate border width
        if self.cell_size <= 4:
            border_width = 0
        else:
            border_width = int(self.cell_size / 5)

        # Draw a rectangle
        x1 = self.cell_size * x
        x2 = self.cell_size * (x + 1)
        y1 = self.cell_size * y
        y2 = self.cell_size * (y + 1)
        self.canvas.create_rectangle(x1, y1, x2, y2 , fill=fill, width=border_width)

    def save_image(self, path):
        ''' Basic save image '''

        # The name of our image
        image_name = path + '_' + str(self.counter).zfill(8) + '.png'

        # Compute location of screen to grab
        x1 = self.window.winfo_rootx() + self.canvas.winfo_x()
        y1 = self.window.winfo_rooty() + self.canvas.winfo_y()
        x2 = x1 + self.canvas.winfo_width()
        y2 = y1 + self.canvas.winfo_height()
        
        # Save the image
        ImageGrab.grab((x1, y1, x2, y2)).save(image_name)
