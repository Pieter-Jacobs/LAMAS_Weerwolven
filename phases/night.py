import random

class Night:
    def __init__(self, players, n_villagers, n_mafia, n_detectives):
        self.players = players
        self.n_villagers = n_villagers
        self.n_mafia = n_mafia
        self.n_detectives = n_detectives

    def mafia_phase(self, removed_players):
        print("-------------------------------- Mafia phase has started --------------------------------\n")
        mafia = [player for player in self.players if player.role == "mafia"]
        killable_players = [player for player in self.players if player not in mafia and player not in removed_players]
        voted_player = random.choice(killable_players)
        return voted_player

    def detective_phase(self):
        print("-------------------------------- Detective phase has started --------------------------------\n")
        detectives = [player for player in self.players if player.role == "detective"]
        eligible_players = [player for player in self.players if player not in detectives]
        inspected_player = random.choice(eligible_players)
        if inspected_player.role == 'mafia':
            #add this knowledge
            print(f"The detective now knows player {inspected_player.get_ID()} to be a mafia! \n")
        else:
            #add this knowledge
            print(f"The detective now knows player {inspected_player.get_ID() } to be a villager! \n")
                

