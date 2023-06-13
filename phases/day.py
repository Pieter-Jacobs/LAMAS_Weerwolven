class Day:
    def __init__(self, players):
        self.players = players

    # Public announcement is made, adding the information to each players' knowledge
    def announcement_phase(self, information):
        for player in self.players:
            player.add_knowledge(information)
    
    # Allows agents to talk to each other
    def discussion_phase(self):
        for player in self.players:
            #might not use this and instead just do the talking here, but its here if needed
            player.discuss()

    def voting_phase(self):
        votes = {}
        for player in self.players:
            vote = player.vote(self.players)
            if vote in votes:
                votes[vote] += 1
            else:
                votes[vote] = 1

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
