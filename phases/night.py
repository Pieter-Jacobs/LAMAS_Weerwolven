import random

from mlsolver.formula import Atom, Box_a

class Night:
    def __init__(self, model, true_world, players, n_villagers, n_mafia, n_detectives):
        self.model = model
        self.true_world = true_world
        self.players = players
        self.n_villagers = n_villagers
        self.n_mafia = n_mafia
        self.n_detectives = n_detectives

    def mafia_phase(self):
        print("-------------------------------- Mafia phase has started --------------------------------\n")
        mafia = [player for player in self.players if player.role == "mafia" and player.alive]
        killable_players = [player for player in self.players if player not in mafia and player.alive]

        # Add townfolk that are known to suspect the mafioso to target list
        targets = []
        for mafioso in mafia:
            for player in killable_players:
                formula = Box_a("agent" + str(mafioso.get_ID()),Box_a("agent" + str(player.get_ID()),Atom("sus" + str(mafioso.get_ID()))))
                if formula.semantic(self.model, self.true_world):
                    targets.append(player)

        voted_player = random.choice(killable_players)
        if len(targets) != 0:
            voted_player = random.choice(targets)

        return voted_player

    def detective_phase(self):
        print("-------------------------------- Detective phase has started --------------------------------\n")
        detectives = [player for player in self.players if player.role == "detective"]
        eligible_players = [player for player in self.players if player not in detectives and player.alive == True]
        random_player = random.choice(eligible_players)
        if random_player.role == 'mafia':
            print("The detective (agent", str(self.players.index(detectives[0])+1) + ") now knows the chosen player to be a mafia! (agent", str(self.players.index(random_player)+1) + ")\n" )
            return random_player
        else:
            print("The detective (agent", str(self.players.index(detectives[0])+1) + ") now knows the chosen player to be a villager! (agent", str(self.players.index(random_player)+1) + ")\n")
            return random_player
                
