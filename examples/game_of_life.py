
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
simulation = Simulation(cell_size=25)
Location.simulation = simulation
Cell.simulation = simulation

# Specify the appropriate neighbourhood model
Location.neighbourhood_strategy = 'moore'

# Initialise a grid of Cells with random starting state
simulation.seed_all(Cell, [Alive, Dead])
                

def loop():
    '''
    Event loop
    '''
    
    # Counter for image frame numbers
    simulation.counter += 1

    # Clear the canvas
    simulation.canvas.delete('all')

   
    # Execute in parallel
    # This sort of thing only works if a Cell
    # makes no direct change on anything but itself
    # i.e. if it has no side effects

    # Figure out what the Cells would do next
    for cell in Cell.objects:
        # Cache the current cell state
        cell.state_before = cell.current_state()
        # Tell the Cell to act
        cell.execute()
        # Cache the next cell state
        cell.state_after = cell.current_state()
        # Restore the current cell state
        cell.replace_state(cell.state_before)

    # Update and then draw them
    for cell in Cell.objects:
        # Update to current state
        cell.replace_state(cell.state_after)
        # Draw
        if cell.dirty:
            simulation.draw(cell)
    

    # Save images
    if simulation.record_video:
        simulation.save_image('game_of_life')

    simulation.canvas.after(20, loop)

        
loop()
simulation.window.mainloop()