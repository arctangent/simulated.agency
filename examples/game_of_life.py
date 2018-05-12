
from random import randint, choice, shuffle


# Ugly hack to fix s.a imports
import sys
sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../..")

from simulated_agency.simulation import Simulation
from simulated_agency.location import Location
from simulated_agency.agents import Cell
from simulated_agency.states import State


# Define some custom states for this simulation

class Alive(State):
    '''
    Represents a cell that is alive
    '''

    def __init__(self, agent):
        super().__init__(agent)
        self.name = 'ALIVE'
        self.colour = 'white'

    def execute(self):
        '''
        Any live cell with two or three live neighbours remains alive.
        Otherwise the cell dies.
        '''
        
        cell = self.agent
        cell.dirty = False
        neighbour_count = len([x for x in cell.location.neighbours() if x.state.name == 'ALIVE'])

        if neighbour_count not in [2, 3]:
            cell.set_state(Dead)
            cell.dirty = True


class Dead(State):
    '''
    Represents a cell that is dead
    '''

    def __init__(self, agent):
        super().__init__(agent)
        self.name = 'DEAD'
        self.colour = 'black'

    def execute(self):
        '''
        Any dead cell with exactly three live neighbors becomes a live cell.
        '''

        cell = self.agent
        cell.dirty = False
        neighbour_count = len([x for x in cell.location.neighbours() if x.state.name == 'ALIVE'])

        if neighbour_count == 3:
            cell.set_state(Alive)
            cell.dirty = True



# Initialise simulation
simulation = Simulation(cell_size=20)
Location.simulation = simulation
Cell.simulation = simulation

# Constants
NUM_CELLS = int(simulation.width * simulation.height * 0.5)

# Specify the appropriate neighbourhood model
Location.neighbourhood_strategy = 'moore'

# Initialise a grid of Cells with random starting state
for x in range(0, simulation.width):
    for y in range(0, simulation.width):
        initial_state = choice([Alive, Dead])
        Cell(Location(x, y), initial_state)
            


def loop():
    '''
    Event loop
    '''
    
    # Counter for image frame numbers
    simulation.counter += 1

    # Figure out what the cells would do next
    
    for cell in Cell.objects:
        # Cache current cell
        current_state = cell.state
        # Tell the cell to act
        cell.state.execute()
        # Restore state
        cell.next_state = cell.state
        cell.state = current_state

    # Update all state at once and draw them
    for cell in Cell.objects:
        cell.state = cell.next_state
        if cell.dirty:
            simulation.draw(cell)

    # Save images
    if simulation.record_video:
        simulation.save_image('game_of_life')

    simulation.canvas.after(20, loop)
        
loop()
simulation.window.mainloop()