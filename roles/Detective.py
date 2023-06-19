from roles.agent import Agent
import random

class Detective(Agent):

    def __init__(self):
        super().__init__("detective")

    def inspect(self):
        pass

    def discuss(self):
        print("blalbalblaa")

    def vote(self, players):
        eligible_playes = [p for p in players if p != self]
        random_player = random.choice(eligible_playes)
        return random_player
    
