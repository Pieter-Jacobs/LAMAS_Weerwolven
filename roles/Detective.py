from roles.agent import Agent
import random

# Detective class
class Detective(Agent):

    def __init__(self, id, suspicious):
        super().__init__("detective", id, suspicious)

    # Gets the ID of a detective
    def get_ID(self):
        return super().get_ID()
    
