from mlsolver.kripke import World, KripkeStructure
from itertools import permutations


class MafiaGame:
    def __init__(self, n_villagers, n_mafia, n_detective):
        self.init_kripke_model(n_villagers, n_mafia, n_detective)
        pass

    def init_kripke_model(self, n_villagers, n_mafia, n_detective):
        """Builds the initial Kripke model world, where everyone believes everyone can be any role,
        atom m1: agent 1 is mafia
        atom d1: agent 1 is detective
        atom v1: agent 1 isvillager
        """
        atoms = ['v' for i in range(n_villagers)] + ['m' for i in range(n_mafia)] + ['d' for i in range(n_detective)]

        all_possible_worlds = {}
        for per in set(permutations(atoms)):
            world = "".join(per)
            all_possible_worlds[world] = True

        world_titles = list(all_possible_worlds.keys())

        world_values = []
        for i in range(len(world_titles)):
            world = world_titles[i]
            world_values.append({})
            for j in range(len(world)):
                world_values[i][str(j) + ":" + world[j]] = True
        
        worlds = [World(world_titles[i], world_values[i]) for i in range(len(world_titles))]
        print(worlds)
        pass

    def start(self):
        result = None
        finished = False

        while not finished:
            finished = True

        return result
