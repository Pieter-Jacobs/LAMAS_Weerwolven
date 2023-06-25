from roles.agent import Agent
import random 

# Villager class
class Villager(Agent):

    def __init__(self, id, suspicious):
        super().__init__("villager", id, suspicious)

    # Gets the ID of a villager
    def get_ID(self):
        return super().get_ID()
