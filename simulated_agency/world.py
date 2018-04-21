
import sys
from time import time
from tkinter import *

# Linux doesn't have ImageGrab but we can use pyscreenshot instead
try:
    from PIL import ImageGrab
except:
    import pyscreenshot as ImageGrab


class World(object):
    '''
    Represents the universe in which our simulation unfolds.
    '''
    
    def __init__(self):
        # Constants
        self.record_video = False
        self.canvas_width = 800
        self.canvas_height = 800
        self.cell_size = 8
        
        # Computed properties
        self.width = int(self.canvas_width / self.cell_size)
        self.height = int(self.canvas_height / self.cell_size)

        # Wrapping
        self.wrap_x = True
        self.wrap_y = True

        # Initial values
        self.counter = 0

        # Attribute storage
        self.locations = {}
        self.agents = []

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

    def draw(self, x, y, fill):
        ''' The most basic way to draw something '''
        if self.cell_size < 4:
            width = 0
        else:
            width = int(self.cell_size / 5)
            self.canvas.create_rectangle(self.cell_size * x, self.cell_size * y, self.cell_size * (x + 1), self.cell_size * (y + 1), fill=fill, width=width)

    def save_image(self, path):
        ''' Basic save image '''

        # The name of our image
        image_name = path + str(self.counter).zfill(8) + '.png'

        # Compute location of screen to grab
        x1 = self.window.winfo_rootx() + self.canvas.winfo_x()
        y1 = self.window.winfo_rooty() + self.canvas.winfo_y()
        x2 = x1 + self.canvas.winfo_width()
        y2 = y1 + self.canvas.winfo_height()
        
        # Save the image
        ImageGrab.grab((x1, y1, x2, y2)).save(image_name)
