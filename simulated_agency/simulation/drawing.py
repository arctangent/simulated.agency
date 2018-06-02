
from ..agents import Mobile


class Painter(object):
    '''
    Provides object drawing functionality
    '''

    def __init__(self, simulation):
        self.simulation = simulation
        # Bind methods
        self.simulation.draw_agent = self.draw_agent
        self.simulation.draw_location = self.draw_location

    def draw_agent(self, thing, fill=None):
        '''
        A very simple way to draw something
        '''

        # Localise variables for faster lookup
        simulation = self.simulation
        canvas = simulation.canvas
        create_text = canvas.create_text
        itemconfig = canvas.itemconfig
        coords = canvas.coords

        # Colour to draw
        fill = fill or thing.colour()

        # Glyph shape and size
        glyph = thing.current_state_instance().glyph
        glyph_size = thing.current_state_instance().size

        # Establish location
        x = thing.location.x_center
        y = thing.location.y_center

        # Establish size to draw
        size = int(thing.size * glyph_size * simulation.cell_size)
        
        # Draw the glyph
        if not hasattr(thing, 'canvas_id'):
            # Create the canvas element for the first time
            thing.canvas_id = create_text(x, y, fill=fill, font='Helvetica %s' % size, text=glyph)
        else:
            # Update the canvas element
            itemconfig(thing.canvas_id, fill=fill, font='Helvetica %s' % size, text=glyph)
            # If the thing can move, then we need to update it's canvas coordinates
            if isinstance(thing, Mobile):
                coords(thing.canvas_id, x, y)

    def draw_location(self, location):
        '''
        Draw a coloured rectangle
        '''

        # Localise variables for faster lookup
        canvas = self.simulation.canvas
        create_rectangle = canvas.create_rectangle
        itemconfig = canvas.itemconfig
        
        # Determine appropriate fill and border width
        fill = location.colour
        border_width = 0

        # Draw a rectangle
        canvas = self.simulation.canvas
        if not hasattr(location, 'canvas_id'):
            # Create the canvas element for the first time
            canvas.create_rectangle(
                location.x_left, location.y_top, location.x_right, location.y_bottom,
                fill=fill, width=border_width
            )
        else:
            # Update the canvas element
            canvas.itemconfig(location.canvas_id, fill=fill)
