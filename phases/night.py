class Night:
    def __init__(self, players):
        self.players = players

    def mafia_phase(self):
        for player in self.players:
            if player.role == "Mafia":
                pass

    def detective_phase(self):
        for player in self.players:
            if player.role == "Detective":
                pass
            
    def game_status(self):
        number_players = 0
        number_mafia = 0
        for player in self.players:
            if player.role == "villager" or player.role == "detective":
                number_players = number_players + 1
            if player.role == "mafia":
                number_mafia = number_mafia + 1
        if number_mafia == 0:
            print("Villagers won!")
        elif number_mafia > number_players:
            print("Mafia won!")
        else:
            print("Game not over yet")       