
from random import randint, choice, shuffle


# Ugly hack to fix s.a imports
import sys
sys.path.append(sys.path[0] + "/..")
sys.path.append(sys.path[0] + "/../..")

from simulated_agency.simulation import Simulation
from simulated_agency.location import Location
from simulated_agency.agents import Cell
from simulated_agency.states import State, StateMachine


# Define some custom states for this simulation

class Alive(State):
    '''
    Represents a Cell that is alive
    '''

    name = 'ALIVE'
    colour = 'white'

    def execute(self, agent):
        '''
        Any live Cell with two or three live neighbours remains alive.
        Otherwise the Cell dies.
        '''
        
        agent.dirty = False
        neighbour_count = len([x for x in agent.location.neighbours() if isinstance(x.state, Alive)]

        if neighbour_count not in [2, 3]:
            agent.set_state(Dead)
            agent.dirty = True


class Dead(State):
    '''
    Represents a Cell that is dead
    '''

    name = 'DEAD'
    colour = 'black'

    def execute(self, agent):
        '''
        Any dead Cell with exactly three live neighbors becomes a live Cell.
        '''
        
        agent.dirty = False
        neighbour_count = len([x for x in agent.location.neighbours() if isinstance(x.state, Alive))

        if neighbour_count == 3:
            agent.set_state(Alive)
            agent.dirty = True



# Initialise simulation
simulation = Simulation(cell_size=20)
Location.simulation = simulation
Cell.simulation = simulation
Cell.state_machine = StateMachine([Alive, Dead])

# Specify the appropriate neighbourhood model
Location.neighbourhood_strategy = 'moore'

# Initialise a grid of Cells with random starting state
for x in range(0, simulation.width):
    for y in range(0, simulation.width):
        initial_state = choice([Alive, Dead])
        cell = Cell(Location(x, y), initial_state)
        cell.set_state(initial_state)
                  


def loop():
    '''
    Event loop
    '''
    
    # Counter for image frame numbers
    simulation.counter += 1
    
    # Figure out what the Cells would do next
    for cell in Cell.objects:
        # Cache current Cell
        current_state = cell.state
        # Tell the Cell to act
        cell.execute()
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