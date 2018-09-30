

import pyglet

class Grid():
    
    def __init__(self):
        '''
        Initialise the grid with some sensible parameters.
        '''
        # Window dimensions
        self.window_width = 800
        self.window_height = 800
        # Background colour (r, g, b, alpha)
        self.background = (0, 0, 0, 255)
        # Window
        self.window = None
        # Cell dimensions
        self.cell_height = 10
        self.cell_width = 10
        self.cell_border = 1
        # Grid size
        self.w = None
        self.h = None
        # Vertex List
        self.vertex_list = None
    
    def simple_prepare(self):
        '''
        Ready pyglet_grid for action. Best used when the default parameters are OK.
        '''
        self.init_window()
        self.init_grid()
        self.init_vertex_list()
        
    def init_window(self):
        '''
        Initialise the window.
        '''
        # Make the window
        self.window = pyglet.window.Window(self.window_width, self.window_height)
        # Set the background color to black - note tuple unpacking with "*"
        pyglet.gl.glClearColor(*self.background)
        # We need to clear the window background or else it will be full of garbage
        self.window.clear()
    
    def init_grid(self):
        '''
        Initialise the grid.
        '''
        self.w = int(self.window_width / self.cell_width)
        self.h = int(self.window_height / self.cell_height)
    
    def init_vertex_list(self):
        '''
        Initialise the vertex list.
        '''
        self.vertex_list = pyglet.graphics.vertex_list(4 * self.w * self.h, 'v2i/static', 'c3B/stream')
        verts = []
        cell_width = self.cell_width
        cell_height = self.cell_height
        cell_border = self.cell_border
        for x in range(self.w):
            for y in range(self.h):
                # Calculate box area
                x1, y1 = x * cell_width, y * cell_height
                x2, y2 = x1 + cell_width, y1
                x3, y3 = x2, y1 + cell_height
                x4, y4 = x1, y3
                # Apply borders to boxes
                if cell_border > 0:
                    x1, y1 = x1 + cell_border, y1 + cell_border
                    x2, y2 = x2 - cell_border, y2 + cell_border
                    x3, y3 = x3 - cell_border, y3 - cell_border
                    x4, y4 = x4 + cell_border, y4 - cell_border
                # Add the vertex coords to our list of vertices
                verts.extend([x1, y1, x2, y2, x2, y3, x4, y4])
        self.vertex_list.vertices = verts
        # Unpack colour values
        r, g, b, alpha = self.background
        # Initialise colours to background colour
        self.vertex_list.colors = [r, g, b] * 4 * self.w * self.h
        
    
    def set_cell(self, x, y, c):
        '''
        Set the color of a cell.
        The variables x and y should be in the range (0, self.w) and (0, self.h) respectively.
        The variable c should be a 3-tuple with values in the range (0, 255).
        '''
        # Unpack colour values
        r, g, b = c
        # There are 4 vertices per coordinate, each with 3 values for the colour
        c1 = 12 * (x + y * self.w)
        self.vertex_list.colors[c1:c1+12] = [r, g, b] * 4
        
    def unset_cell(self, x, y):
        '''
        Unset a cell back to the background colour.
        '''
        # Unpack colour values
        r, g, b, alpha = self.background
        # There are 4 vertices per coordinate, each with 3 values for the colour
        c1 = 12 * (x + y * self.w)
        self.vertex_list.colors[c1:c1+12] = [r, g, b] * 4
        
    def clear_all_cells(self):
        '''
        Clear the color of all cells.
        '''
        # Unpack colour values
        r, g, b, alpha = self.background
        # There are 4 vertices per coordinate, each with 3 values for the colour
        c_max = 12 * (self.h * self.w)
        self.vertex_list.colors[0:c_max] = [r, g, b] * int(c_max / 3)

    def draw(self):
        '''
        Draw the vertex list using the currently assigned colours.
        '''
        self.vertex_list.draw(pyglet.gl.GL_QUADS)
