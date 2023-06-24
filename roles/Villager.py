from roles.agent import Agent
import random 

class Villager(Agent):
    def __init__(self, id, suspicious):
        super().__init__("villager", id, suspicious)

    def get_ID(self):
        return super().get_ID()
    
    def vote(self, players):
        eligible_playes = [p for p in players if p != self and p.alive == True]
        random_player = random.choice(eligible_playes)
        return random_player

