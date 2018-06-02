
import sys

from random import randint, choice, shuffle
from time import time
from tkinter import *

# Linux doesn't have ImageGrab but we can use pyscreenshot instead
try:
    from PIL import ImageGrab
except:
    try:
        import pyscreenshot as ImageGrab
    except:
        print("Can't do video!")


from ..location import Location
from .drawing import *
from .executor import *
from .geometry import *
from .seeder import *
from .video import *


class Simulation(object):
    '''
    Represents the universe in which our simulation unfolds.
    '''

    # Strategy pattern for neighbour location
    neighbourhood_strategy = 'von_neumann'
    
    def __init__(self, width=None, height=None, cell_size=None, name=None):

        # Name of this simulation - used for file output
        self.name = name or 'simulation'

        # Locations
        self.locations = {}

        # Constants - do not change these directly after simulation instantiation
        self.canvas_width = width or 800
        self.canvas_height = height or 800
        self.cell_size = cell_size or 8
        
        # Computed properties
        self.set_cell_size(cell_size)
        self.init_locations()

        # Preferences
        self.record_video = False

        # Wrapping
        self.wrap_x = True
        self.wrap_y = True

        # Track simulation age
        self.age = 0

        # Delegate functionality
        seeder = Seeder(self)
        geometry = Geometry(self)
        executor = Executor(self)
        painter = Painter(self)
        video_recorder = VideoRecorder(self)

        # GUI
        self.window = Tk()
        self.window.resizable(False, False)
        # GUI - Canvas
        self.canvas = Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg='black', bd=0, highlightthickness=0)
        self.canvas.pack()

        # Sane program termination
        def _quit(event=None):
            self.window.destroy()
            sys.exit()
        self.window.protocol("WM_DELETE_WINDOW", _quit)

        # Keyboard - Quit
        self.window.bind('q', _quit)

    def set_cell_size(self, cell_size=8):
        '''
        Call this method instead of changing cell_size directly
        '''
        self.cell_size = cell_size
        self.width = int(self.canvas_width / self.cell_size)
        self.height = int(self.canvas_height / self.cell_size)

    def init_locations(self):
        Location.simulation = self
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.locations[x, y] = Location(x, y)
