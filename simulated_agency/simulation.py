
import sys

from random import randint, choice
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


    def seed(self, object_class, num_or_density, state_class, **kwargs):
        '''
        Create a number of objects within the simulation,
        guaranteed to all be placed (i.e. will retry if
        it randomly chooses a full location.

        Note that since it just retries a new random location
        it isn't well suited to creating dense intial populations
        because the likelihood of choosing an occupied location
        increases as the density rises, leading to more and more
        re-tries being required. However, if you wait long enough
        then it will eventually finish. 

        If num_or_density >= 1 then that is the number
        of objects that will be placed.

        If 0 < num_or_density < 1 then that is the proportion
        of objects that will be placed relative to the area
        of the simulation.

        Returns the number of agents successfully placed.
        '''

        # How many objects do we need to place?
        if 0 < num_or_density < 1:
            number_to_place = int(num_or_density * self.width * self.height)
        elif num_or_density >= 1:
            number_to_place = num_or_density
        else:
            raise Exception("Can't seed %s objects")

        # Begin planting
        for _ in range(0, number_to_place):
            # Find a location
            location_found = False
            while not location_found:
                location = self.random_location()
                if not location.is_full():
                    location_found = True
            # Create the object
            object_class(location, state_class, **kwargs)

        return number_to_place

    def seed_all(self, object_class, possible_state_list):
        '''
        Create an object in every location within the simulation,
        with the initial state chosen at random from possible_states.

        The possible_stats parameter should be a list, with each
        entry being either an unadorned state class name OR a tuple/list.
        If a tuple/list, then the first element should be a state class name
        and then the second element should be a dictionary of state params
        with which to initialise the state.

        Example:
            simulation.seed_all(MyState, [StateOne, [StateTwo, {timer:1}], StateThree]
        '''

        for x in range(0, self.width):
            for y in range(0, self.height):
                object_instance = object_class(Location(x, y))
                chosen_state = choice(possible_state_list)
                try:
                    # States with params
                    initial_state_class, initial_state_params = chosen_state
                    object_instance.add_state(initial_state_class(object_instance, **initial_state_params))
                except:
                    # Unadorned states
                    object_instance.add_state(chosen_state(object_instance))

