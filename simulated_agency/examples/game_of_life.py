
from ..simulation import Simulation
from ..location import Location
from ..agents import Cell
from ..states import State


# Define some custom states for this simulation

class Alive(State):
    '''
    Represents a Cell that is alive
    '''

    name = 'ALIVE'
    colour = 'white'

    def handle(self):
        '''
        Any live Cell with two or three live neighbours remains alive.
        Otherwise the Cell dies.
        '''
        
        super().handle()

        agent = self.agent

        agent.dirty = False
        neighbour_count = len([x for x in agent.location.neighbours() if x.is_in_state(Alive)])
        
        if neighbour_count not in [2, 3]:
            agent.replace_state(Dead(agent))
            agent.dirty = True


class Dead(State):
    '''
    Represents a Cell that is dead
    '''

    name = 'DEAD'
    colour = 'black'

    def handle(self):
        '''
        Any dead Cell with exactly three live neighbors becomes a live Cell.
        '''
        
        super().handle()

        agent = self.agent

        agent.dirty = False
        neighbour_count = len([x for x in agent.location.neighbours() if x.is_in_state(Alive)])
        
        if neighbour_count == 3:
            agent.replace_state(Alive(agent))
            agent.dirty = True



# Initialise simulation
simulation = Simulation(cell_size=20, name='GameOfLife')

# Bind models to simulation
Location.simulation = simulation
Cell.simulation = simulation

# Specify the appropriate neighbourhood model
Location.neighbourhood_strategy = 'moore'

# Initialise a grid of Cells with random starting state
simulation.seed_all(Cell, [Alive, Dead])
        
# Run the simulation
# Setting the synchronous flag updates all cells simultaneosly
simulation.execute(Cell, synchronous=True)

# Handle GUI events etc
simulation.window.mainloop()
