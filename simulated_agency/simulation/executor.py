
from random import shuffle
import sys


class Executor(object):
    '''
    Provides simulation execution
    '''

    def __init__(self, simulation):
        self.simulation = simulation
        # Bind methods
        self.simulation.execute = self.execute


    def execute(
        self, agent_class_or_class_list,
        before_each_loop=None, before_each_agent=None,
        synchronous=False, timer=None,
        draw_locations=True
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
        background_colour = simulation.background_colour
        draw_location = simulation.draw_location
        draw_agent = simulation.draw_agent
        record_video = simulation.record_video
        save_image = simulation.save_image
        name = simulation.name
        canvas = simulation.canvas
        
        # Get a list of all the objects to be executed/drawn
        if isinstance(agent_class_or_class_list, list):
            agent_list = [a for agent_class in agent_class_or_class_list for a in agent_class.objects]
        else:
            agent_list = agent_class_or_class_list.objects

        # Do an initial draw of all locations and all agents
        if draw_locations:
            # Draw all the locations which have a colour
            for location in locations.values():
                if location.colour and location.colour != background_colour:
                    draw_location(location)
        for agent in agent_list:
            draw_agent(agent)
       
        # Define our simulation loop
        def loop():

            # Increment simulation age
            simulation.age += 1

            # Decrement simulation timer
            if self.timer:
                self.timer -= 1
                if self.timer == 0:
                    simulation.window.destroy()
                    print('Timer expired')
                    sys.exit()

            # Execute user-defined function
            if before_each_loop:
                # We capture any emitted variables for use
                # in the before_each_agent section
                before_each_loop_vars = before_each_loop()

            if draw_locations:
                # Draw all the locations which have a colour
                for location in locations.values():
                    if location.colour and location.colour != background_colour:
                        draw_location(location)

            # Go through the list of agents and tell each of them to do something
             
            if synchronous:
                
                # Figure out what the agents' future state will be
                for agent in agent_list:
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

                # Update and then draw them
                for agent in agent_list:
                    # Update to current state
                    agent.replace_state_instance(agent.state_after)
                    # Draw them
                    # If we don't draw locations then we can skip
                    # drawing agents too if we know they haven't changed.
                    if draw_locations:
                        draw_agent(agent)
                    elif agent.dirty:
                        draw_agent(agent)

            else:

                shuffle(agent_list)
                for agent in agent_list:
                    # Increment agent age
                    agent.age += 1
                    # Execute user-defined function
                    if before_each_agent:
                        before_each_agent(agent, before_each_loop_vars)
                    # Tell the agent to act
                    agent.execute()
                    # Draw them
                    # If we don't draw locations then we can skip
                    # drawing agents too if we know they haven't changed.
                    if draw_locations:
                        draw_agent(agent)
                    elif agent.dirty:
                        draw_agent(agent)

            # Save images
            if record_video:
                save_image(name)

            # Continue simulation loop
            canvas.after(5, loop)

        # Execute our simulation loop
        loop()

        # Handle GUI events etc.
        self.simulation.window.mainloop()
