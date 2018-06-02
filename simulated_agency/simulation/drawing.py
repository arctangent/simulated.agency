
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

        # Colour to draw
        fill = fill or thing.colour()

        glyph = thing.current_state_instance().glyph
        glyph_size = thing.current_state_instance().size
        if glyph:
            # Establish location
            x = thing.location.x_center
            y = thing.location.y_center
            # Establish size
            size = int(thing.size * glyph_size * self.simulation.cell_size)
            # Draw the glyph
            self.simulation.canvas.create_text(x, y, fill=fill, font='Helvetica %s' % size, text=glyph)
            return

    def draw_location(self, location):
        '''
        Draw a coloured rectangle
        '''

        # Determine appropriate fill and border width
        fill = location.colour
        border_width = 0

        # Draw a rectangle
        self.simulation.canvas.create_rectangle(
            location.x_left, location.y_top, location.x_right, location.y_bottom,
            fill=fill, width=border_width
        )
