
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


from .location import Location


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
        self.width = int(self.canvas_width / self.cell_size)
        self.height = int(self.canvas_height / self.cell_size)
        self.init_locations()

        # Preferences
        self.record_video = False

        # Wrapping
        self.wrap_x = True
        self.wrap_y = True

        # Track simulation age
        self.age = 0

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

    def set_cell_size(self, cell_size):
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

    def random_x(self):
        return randint(0, self.width - 1)

    def random_y(self):
        return randint(0, self.height - 1)

    def random_xy(self):
        return self.random_x(), self.random_y()

    def random_location(self):
        return self.locations[self.random_xy()]

    #
    # Geometry - wrapping and constraining
    #

    def _wrap(self, val, min_val, max_val):
        '''
        Utility function to help with wrapping edges.
        '''
        
        if val < min_val:
            return 1 + max_val + val
        elif val > max_val:
            return val - max_val - 1
        else:
            return val

    def _constrain(self, val, min_val, max_val):
        '''
        Utility function to help with non-wrapping edges.
        '''

        if val < min_val:
            return min_val
        elif val > max_val:
            return max_val
        else:
            return val
        
    def normalise_width(self, val):
        '''
        Ensure a value remains within Simulation width
        either by wrapping or constraining
        '''

        if self.wrap_x:
            # Wrap
            return self._wrap(val, 0, self.width - 1)
        else:
            # Constrain
            return self._constrain(val, 0, self.width - 1)

    
    def normalise_height(self, val):
        '''
        Ensure a value remains within Simulation height
        either by wrapping or constraining
        '''

        if self.wrap_y:
            # Wrap
            return self._wrap(val, 0, self.height - 1)
        else:
            # Constrain
            return self._constrain(val, 0, self.height - 1)

    #
    # Drawing
    #

    def draw_agent(self, thing, fill=None):
        '''
        A very simple way to draw something
        '''

        # Colour to draw
        fill = fill or thing.colour()

        #
        # Can we draw a unicode glyph?
        #

        glyph = thing.current_state().glyph
        glyph_size = thing.current_state().size
        if glyph:
            # Establish location
            x = thing.location.x_center
            y = thing.location.y_center
            # Establish size
            size = int(thing.size * glyph_size * self.cell_size)
            # Draw the glyph
            self.canvas.create_text(x, y, fill=fill, font='Helvetica %s' % size, text=glyph)
            return

    def draw_location(self, location):
        '''
        Draw a coloured rectangle
        '''

        # Determine appropriate fill and border width
        fill = location.colour
        border_width = 0

        # Draw a rectangle
        self.canvas.create_rectangle(
            location.x_left, location.y_top, location.x_right, location.y_bottom,
            fill=fill, width=border_width
        )

    def save_image(self, path):
        ''' Basic save image '''

        # The name of our image
        image_name = 'simulated_agency/images/%s_%s.png' % (path, str(self.age).zfill(8))

        # Compute location of screen to grab
        x1 = self.window.winfo_rootx() + self.canvas.winfo_x()
        y1 = self.window.winfo_rooty() + self.canvas.winfo_y()
        x2 = x1 + self.canvas.winfo_width()
        y2 = y1 + self.canvas.winfo_height()
        
        # Save the image
        ImageGrab.grab((x1, y1, x2, y2)).save(image_name)

    def create_obstruction_rectangle(self, x_start, y_start, width, height):
        '''
        Marks a rectangular area of the world as impassable.
        Note: Does not take into account screen wrapping.
        '''

        for x in range(x_start, x_start + width):
            for y in range(y_start, y_start + height):
                location = self.locations[x, y]
                location.capacity = 0
                location.colour = "yellow"


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
                location = self.locations[x, y]
                object_instance = object_class(location)
                chosen_state = choice(possible_state_list)
                try:
                    # States with params
                    initial_state_class, initial_state_params = chosen_state
                    object_instance.add_state(initial_state_class(object_instance, **initial_state_params))
                except:
                    # Unadorned states
                    object_instance.add_state(chosen_state(object_instance))

    def execute(self, agent_class_or_class_list, before_each_loop=None, before_each_agent=None, synchronous=False):
        '''
        Run the simulation's loop for the agent_classes listed.
        
        By default the list of agents is shuffled and each is executed
        one at a time, with the simulation being immediately updated. 

        If preferred, the synchronous flag can be set. This will execute all agents
        to determine their 'next' state and then update all of them at the same time.
        This mode of execution only makes sense if agents do not have side effects on
        the rest of the simulation i.e. they only update their own state and do not
        modify properties of the locations they are in.

        The agent_classes param can be either a single class or a list of classes.
        '''
        
        # Get a list of all the objects to be executed/drawn
        if isinstance(agent_class_or_class_list, list):
            agent_list = [a for agent_class in agent_class_or_class_list for a in agent_class.objects]
        else:
            agent_list = agent_class_or_class_list.objects
       
        # Define our simulation loop
        def loop():

            # Increment simulation age
            self.age += 1

            # Clear the canvas
            self.canvas.delete('all')

            # Execute user-defined function
            if before_each_loop:
                # We capture any emitted variables for use
                # in the before_each_agent section
                before_each_loop_vars = before_each_loop()

            # Draw all the locations which have a colour
            for location in self.locations.values():
                if location.colour:
                    self.draw_location(location)

            # Go through the list of agents and tell each of them to do something
             
            if synchronous:
                
                # Figure out what the agents' future state will be
                for agent in agent_list:
                    # Increment agent age
                    agent.age += 1
                    # Execute user-defined function
                    if before_each_agent:
                        before_each_agent(agent, before_each_loop_vars)
                    # Cache the current state
                    agent.state_before = agent.current_state()
                    # Tell the agent to act
                    agent.execute()
                    # Cache the next agent state
                    agent.state_after = agent.current_state()
                    # Restore the current agent state
                    agent.replace_state(agent.state_before)

                # Update and then draw them
                for agent in agent_list:
                    # Update to current state
                    agent.replace_state(agent.state_after)
                    # Draw
                    self.draw_agent(agent)

            else:

                shuffle(agent_list)
                for agent in agent_list:
                    # Increment agent age
                    agent.age += 1
                    # Execute user-defined function
                    if before_each_agent:
                        before_each_agent(agent, before_each_loop_vars)
                    # Tell the agent to act
                    agent.execute()
                    # Draw them
                    self.draw_agent(agent)

            # Save images
            if self.record_video:
                self.save_image(self.name)

            # Continue simulation loop
            self.canvas.after(20, loop)

        # Execute our simulation loop
        loop()

        # Handle GUI events etc.
        self.window.mainloop()
