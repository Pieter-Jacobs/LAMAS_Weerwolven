from mlsolver.kripke import World, KripkeStructure
from itertools import permutations
from roles.detective import Detective
from roles.villager import Villager
from roles.mafia import Mafia
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
        atom v1: agent 1 isvillager
        """
        atoms = ['v' for i in range(n_villagers)] + ['m' for i in range(n_mafia)] + ['d' for i in range(n_detective)]

        # --- TODO When creating the worlds, we can assign ID's to the agents depending on the assigned roles in the world. ---#
        all_possible_worlds = [list(per) for per in set(permutations(atoms))]
        for i in range(len(all_possible_worlds)):
            for j in range(len(all_possible_worlds[i])):
                all_possible_worlds[i][j] = str(j) + ":" + all_possible_worlds[i][j] 
        #print(all_possible_worlds)
        pass

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
        
