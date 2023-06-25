from roles.agent import Agent
import random

# Mafia class
class Mafia(Agent):

    def __init__(self, id, suspicious):
        super().__init__("mafia", id, suspicious)
    
    # Gets the ID of a mafioso
    def get_ID(self):
        return super().get_ID()

