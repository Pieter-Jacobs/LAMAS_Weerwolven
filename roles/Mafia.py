from roles.agent import Agent

class Mafia(Agent):
    def __init__(self):
        super().__init__("mafia")

    def kill_player(self, players):
        pass
    
    def discuss(self):
        print("blalbalblaa")

    def vote(self, players):
        pass

