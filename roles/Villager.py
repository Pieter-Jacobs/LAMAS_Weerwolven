from roles.agent import Agent
import random 

class Villager(Agent):
    def __init__(self):
        super().__init__("villager")

    def init_kripke_model(self):
        """Builds the initial Kripke model world, where everyone can be any role"""
        pass
    
    # In here we can implement how the villagers are going to be communicating
    def discuss(self):
        print("blalbalblaa")

    def vote(self, players):
        eligible_playes = [p for p in players if p != self]
        random_player = random.choice(eligible_playes)
        return random_player

