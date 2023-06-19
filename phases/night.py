import random

class Night:
    def __init__(self, players, n_villagers, n_mafia, n_detectives):
        self.players = players
        self.n_villagers = n_villagers
        self.n_mafia = n_mafia
        self.n_detectives = n_detectives

    def mafia_phase(self):
        print("Mafia phase has started \n")
        for player in self.players:
            if player.role == "mafia":
                killable_players = [p for p in self.players if p != player and p.role != "mafia"]
                voted_player = random.choice(killable_players)
                return voted_player

    def detective_phase(self):
        print("Detective phase has started \n")
        for player in self.players:
            if player.role == "detective":
                eligible_playes = [p for p in self.players if p != player]
                random_player = random.choice(eligible_playes)
                if random_player.role == 'mafia':
                    #add this knowledge
                    print("The detective now knows the chosen player to be a mafia! \n")
                else:
                    #add this knowledge
                    print("The detective now knows the chosen player to be a villager! \n")
            
