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

        all_possible_worlds = [list(per) for per in set(permutations(atoms))]
        for i in range(len(all_possible_worlds)):
            for j in range(len(all_possible_worlds[i])):
                all_possible_worlds[i][j] = str(j) + ":" + all_possible_worlds[i][j] 
        print(all_possible_worlds)
        pass

    def start(self):
        result = None
        finished = False

        while not finished:
            finished = True

        return result
