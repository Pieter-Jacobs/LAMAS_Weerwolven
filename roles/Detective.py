from roles.agent import Agent
import random

class Detective(Agent):

    def __init__(self, id):
        super().__init__("detective", id)

    def inspect(self):
        pass

    def discuss(self):
        print("blalbalblaa")

    def vote(self, players, removed_players):
        eligible_playes = [p for p in players if p != self and p not in removed_players]
        random_player = random.choice(eligible_playes)
        return random_player
    
