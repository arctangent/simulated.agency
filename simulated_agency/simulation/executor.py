
import curses
from random import shuffle, random
import sys
from time import sleep

import pyglet
from .pyglet_grid import Grid

class Executor(object):
    '''
    Provides simulation execution
    '''

    def __init__(self, simulation):
        self.simulation = simulation
        # Bind methods
        self.simulation.execute = self.execute
        # Init Grid
        self.init_grid(simulation)

    def init_grid(self, simulation):
        # Initialise the Grid
        grid = Grid()
        grid.window_width = 800
        grid.window_height = 800
        grid.background = simulation.background_colour
        grid.init_window()
        # 2. Set up the cell size and border
        grid.cell_height = int(grid.window_height / simulation.height)
        grid.cell_width = int(grid.window_width / simulation.width)
        grid.cell_border = 0
        grid.init_grid()
        # 3. Initialise the vertex list
        grid.init_vertex_list()
        # Finally, bind to self
        self.grid = grid

    def draw(self, agent):
        self.grid.set_cell(agent.location.x, agent.location.y, agent.colour())

    def undraw(self, agent):
        self.grid.unset_cell(agent.location.x, agent.location.y)

    def execute(
        self, before_each_loop=None, before_each_agent=None,
        synchronous=False, timer=None, draw_locations=True
    ):
        '''
        Run the simulation's loop for the agent_classes listed.
        
        By default the list of agents is shuffled and each is executed
        one at a time, with the simulation being immediately updated. 

        If preferred, the synchronous flag can be set. This will execute all agents
        to determine their 'next' state and then update all of them at the same time.
        This mode of execution only makes sense if agents do not have side effects on
        the rest of the simulation i.e. they only update their own state and do not
        modify properties of the locations they are in.

        The agent_classes param can be either a single class or a list of classes.
        '''

        self.timer = timer
        # Localise names for faster access, because we
        # do a lot of this inside the simulation loop
        simulation = self.simulation
        locations = simulation.locations
        name = simulation.name
        draw = self.draw
        undraw = self.undraw

        # Initial screen draw
        self.grid.clear_all_cells()
        agent_list = [a for agent_class in simulation.bound_agent_classes for a in agent_class.objects]
        for agent in agent_list:
            draw(agent)
        self.grid.draw()

        # Define our simulation loop
        def loop(dt):

            # Increment simulation age
            simulation.age += 1

            # Decrement simulation timer
            if self.timer:
                self.timer -= 1
                if self.timer == 0:
                    print('Timer expired')
                    sys.exit(0)

            # Get a list of all the objects to be executed/drawn
            # NOTE: We do this every loop because some agents
            #       may have been born or died since last turn
            agent_list = [a for agent_class in simulation.bound_agent_classes for a in agent_class.objects]
            if not agent_list:
                raise Exception('No bound agent classes, so nothing to simulate!')

            # Execute user-defined function
            if before_each_loop:
                # We capture any emitted variables for use
                # in the before_each_agent section
                before_each_loop_vars = before_each_loop()

            # Go through the list of agents and tell each of them to do something
            
            if synchronous:
                
                # Figure out what the agents' future state will be
                for agent in agent_list:
                    undraw(agent)
                    # Increment agent age
                    agent.age += 1
                    # Execute user-defined function
                    if before_each_agent:
                        before_each_agent(agent, before_each_loop_vars)
                    # Cache the current state
                    agent.state_before = agent.current_state_instance()
                    # Tell the agent to act
                    agent.execute()
                    # Cache the next agent state
                    agent.state_after = agent.current_state_instance()
                    # Restore the current agent state
                    agent.replace_state_instance(agent.state_before)

                # Update to current state
                for agent in agent_list:
                    agent.replace_state_instance(agent.state_after)
                    draw(agent)

            else:

                shuffle(agent_list)
                for agent in agent_list:
                    undraw(agent)
                    # Increment agent age
                    agent.age += 1
                    # Execute user-defined function
                    if before_each_agent:
                        before_each_agent(agent, before_each_loop_vars)
                    # Tell the agent to act
                    agent.execute()
                    draw(agent)


            # Update the grid
            self.grid.draw()
        
        pyglet.clock.schedule(loop)
        pyglet.app.run()
