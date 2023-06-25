import random

# This class serves as the basis for each agent
class Agent():
    
    def __init__(self, role, id, suspicious=False):
        self.sociability = random.uniform(0.5, 1)
        self.suspicious = suspicious
        self.alive = True
        self.role = role
        self.ID = id

    # Sets the sociability value for an agent
    def set_sociability(self, sociability):
        self.sociability = sociability
    
    # Sets the ID for an agent
    def set_ID(self, ID):
        self.ID = ID

    # Gets the ID of an agent
    def get_ID(self):
        return self.ID
    
    # States whether an agent is acting suspiciously
    def is_suspicious(self):
        return self.suspicious
