from mlsolver.kripke import World, KripkeStructure
from itertools import permutations
from roles.Detective import Detective
from roles.Villager import Villager
from roles.Mafia import Mafia
from phases.day import Day
from phases.night import Night


class MafiaGame:
    def __init__(self, n_villagers, n_mafia, n_detective):
        self.init_kripke_model(n_villagers, n_mafia, n_detective)
        self.init_players(n_villagers, n_mafia, n_detective)
        pass
    
    def init_kripke_model(self, n_villagers, n_mafia, n_detective):
        """Builds the initial Kripke model world, where everyone believes everyone can be any role,
        atom m1: agent 1 is mafia
        atom d1: agent 1 is detective
        atom v1: agent 1 is villager
        """
        agents = ['agent' + str(i + 1) for i in range(n_villagers + n_mafia + n_detective)]

        # Create all possible combinations of agent roles
        game_roles = ['v'] * n_villagers + ['m'] * n_mafia + ['d'] * n_detective
        all_possible_roles = set(permutations(game_roles))

        # Create the worlds for the Kripke structure
        worlds = []
        for roles in all_possible_roles:
            world_name = ':'.join([agent + ':' + role for agent, role in zip(agents, roles)])
            world = World(world_name, {})
            worlds.append(world)

        # Create the relations dictionary based on the agent's role in each world
        relations = {}
        for i, agent in enumerate(agents):
            agent_relations = []
            for j, world in enumerate(worlds):
                agent_roles = world.name.split(':')[1::2]
                agent_role = agent_roles[i]
                for world_2 in worlds[j:]: 
                    agent_roles = world_2.name.split(':')[1::2] 
                    if agent_roles[i] == agent_role:
                        agent_relations.append((world.name, world_2.name))
            relations[agent] = set(agent_relations)
            
        # Create the Kripke structure
        ks = KripkeStructure(worlds, relations)


        return ks
        
    # Creates the players without ID
    def init_players(self, n_villagers, n_mafia, n_detective):
        self.players=[]
        for x in range(0,n_villagers):  
            self.players.append(Villager())

        for x in range(0,n_mafia):  
            self.players.append(Mafia())

        for x in range(0,n_detective):  
            self.players.append(Detective())

    def start(self):
        result = None
        finished = False
        
        day = Day(self.players)

        day.game_status()
        print(self.players)
        while not finished:
            finished = True

        return result
        
