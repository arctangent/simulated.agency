
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
        neighbour_count = len([x for x in cell.location.neighbours() if isinstance(x.state, Alive)])

        if neighbour_count not in [2, 3]:
            cell.set_state(Dead)


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
        neighbour_count = len([x for x in cell.location.neighbours() if isinstance(x.state, Alive)])

        if neighbour_count == 3:
            cell.set_state(Alive)



# Initialise simulation
simulation = Simulation(cell_size=40)
Location.simulation = simulation
Cell.simulation = simulation

# Constants
NUM_CELLS = int(simulation.width * simulation.height * 0.3)

# Specify the appropriate neighbourhood model
Location.neighbourhood_strategy = 'moore'

# Initialise a grid of Cells with random starting state
for x in range(0, simulation.width):
    for y in range(0, simulation.width):
        initial_state = choice([Alive, Dead])
        Cell(Location(x, y), initial_state)
            


while True:
    '''
    Event loop
    '''
    print(len(Cell.objects))
    # Counter for image frame numbers
    simulation.counter += 1

    # Go through the list of agents and tell each of them to do something
    shuffle(Cell.objects)
    for agent in Cell.objects:
        # Tell the agent to act
        agent.state.execute()
        simulation.draw(agent)

    # Update the canvas
    simulation.canvas.after(20)
    simulation.canvas.update()

    # Save images
    if simulation.record_video:
        simulation.save_image('game_of_life')
        

simulation.window.mainloop()