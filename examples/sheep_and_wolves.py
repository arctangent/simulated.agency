
from random import choice, randint

from simulated_agency.simulation import Simulation
from simulated_agency.agents import Mobile
from simulated_agency.states import *


class WolfChasingTarget(State):
    '''
    A wolf in this state will move towards its
    target and kill that target if it ends up
    adjacent to the target after the move.
    '''

    name = "WOLF_CHASING_TARGET"
    colour = (0, 0, 255)
    required_params = ['target']

    def handle(self):
        super().handle()
        target = self.context['target']
        agent = self.agent
        agent.move_towards_target(target, adjacent_ok=True)
        # Can it kill the sheep it is chasing?
        neighbours = agent.location.neighbours()
        if target in neighbours:
            target.replace_state(Dead)
            agent.replace_state(WolfSelectingTarget)
        # Are there any targets of opportunity available?
        else:
            careless_sheep = [s for s in neighbours if isinstance(s, Sheep)]
            if careless_sheep:
                target = choice(careless_sheep)
                target.replace_state(Dead)
                agent.replace_state(WolfSelectingTarget)



class WolfSelectingTarget(State):
    '''
    Agents in this state will choose a target
    to follow and then begin following it.
    '''

    name = 'WOLF_SELECTING_TARGET'
    colour = (0, 0, 255)

    def handle(self):
        super().handle()
        target_list = Sheep.objects
        # Wolves will only chase Sheep that are alive
        live_target_list = [x for x in target_list if not x.is_in_state(Dead)]
        # Choose target
        if live_target_list:
            # Choose the nearest live target and pursue it
            target = self.agent.nearest(live_target_list)
            self.agent.add_state(WolfChasingTarget, target=target)
        else:
            # No sheep left to chase
            self.agent.add_state(MoveRandomly)


class SheepGrazing(State):
    '''
    Sheep that are grazing occasionally move around.
    But mainly they are recovering their energy.
    '''
    
    name = 'SHEEP_GRAZING'
    colour = (0, 255, 0)

    def handle(self):
        super().handle()
        agent = self.agent
        # Restore energy up to max
        if agent.energy < 5:
            agent.energy += 1
        # Is there a wolf nearby?
        nearest_wolf = agent.nearest(Wolf, radius=3)
        if nearest_wolf:
            agent.replace_state(SheepFleeing, enemy=nearest_wolf)
            return
        # Occasionally move
        if randint(1, 10) <= 3:
            self.agent.move_randomly()


class SheepFleeing(State):
    '''
    Sheep that are fleeing will do so until they tire.
    '''

    name = 'SHEEP_FLEEING'
    colour = (0, 255, 0)
    required_params = ['enemy']

    def handle(self):
        super().handle()
        agent = self.agent
        # Burn energy
        agent.energy -= 1
        if agent.energy == 0:
            agent.replace_state(SheepGrazing)
            return
        # Flee
        enemy = self.context['enemy']
        if agent.distance_to(enemy) < 3:
            agent.move_away_from_target(enemy)
        else:
            agent.replace_state(SheepGrazing)


# Initialise simulation
simulation = Simulation(name='SheepAndWolves')

# Use same base model for two types of object
class Sheep(Mobile): energy = 5
class Wolf(Mobile): pass

# Bind models to simulation
simulation.bind(Wolf, Sheep)

# Add some sheep to the simulation
simulation.seed(Sheep, 0.15, SheepGrazing)

# Add some wolves to the simulation
simulation.seed(Wolf, 20, WolfSelectingTarget)

# Run the simulation
simulation.execute(draw_locations=False)
