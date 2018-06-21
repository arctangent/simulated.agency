
from simulated_agency.simulation import Simulation
from simulated_agency.agents import Locatable as Cell
from simulated_agency.states import State


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

        # Never needs to be drawn again after the
        # initial screen draw unless it changes state
        agent.dirty = False

        neighbour_count = len([x for x in agent.location.neighbours() if x.is_in_state(Alive)])
        
        if neighbour_count not in [2, 3]:
            agent.replace_state(Dead)
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

        # Never needs to be drawn again after the
        # initial screen draw unless it changes state
        agent.dirty = False

        neighbour_count = len([x for x in agent.location.neighbours() if x.is_in_state(Alive)])
        
        if neighbour_count == 3:
            agent.replace_state(Alive)
            agent.dirty = True



# Initialise simulation
simulation = Simulation(cell_size=16, name='GameOfLife')

# Bind models to simulation
Cell.simulation = simulation

# Specify the appropriate neighbourhood model
simulation.neighbourhood_strategy = 'moore'

# Initialise a grid of Cells with random starting state
simulation.seed_all(Cell, [Alive, Dead])
        
# Run the simulation
# Setting the synchronous flag updates all cells simultaneosly
simulation.execute(Cell, synchronous=True, draw_locations=False)
