from roles.agent import Agent
import random

class Mafia(Agent):
    def __init__(self, id):
        super().__init__("mafia", id, True)

    def vote(self, players):
        eligible_playes = [p for p in players if p != self and p.alive == True]
        random_player = random.choice(eligible_playes)
        return random_player

