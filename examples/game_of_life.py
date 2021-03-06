
from simulated_agency.simulation import Simulation
from simulated_agency.agents import Locatable as Cell
from simulated_agency.states import State


# Define some custom states for this simulation

class Alive(State):
    '''
    Represents a Cell that is alive
    '''

    name = 'ALIVE'
    colour = (255, 255, 255)

    def handle(self):
        '''
        Any live Cell with two or three live neighbours remains alive.
        Otherwise the Cell dies.
        '''
        
        super().handle()

        agent = self.agent

        neighbour_count = len([x for x in agent.location.neighbours() if x.is_in_state(Alive)])
        
        if neighbour_count not in [2, 3]:
            agent.replace_state(Dead)


class Dead(State):
    '''
    Represents a Cell that is dead
    '''

    name = 'DEAD'
    colour = (0, 0, 0)

    def handle(self):
        '''
        Any dead Cell with exactly three live neighbors becomes a live Cell.
        '''
        
        super().handle()

        agent = self.agent

        neighbour_count = len([x for x in agent.location.neighbours() if x.is_in_state(Alive)])
        
        if neighbour_count == 3:
            agent.replace_state(Alive)



# Initialise simulation
simulation = Simulation(name='GameOfLife')

# Bind models to simulation
simulation.bind(Cell)

# Specify the appropriate neighbourhood model
simulation.neighbourhood_strategy = 'moore'

# Initialise a grid of Cells with random starting state
simulation.seed_all(Cell, [Alive, Dead])
        
# Run the simulation
# Setting the synchronous flag updates all cells simultaneosly
simulation.execute(synchronous=True, draw_locations=False)
