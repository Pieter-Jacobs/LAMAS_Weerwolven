import random

''' This class serves as the basis for each agent'''
class Agent():

    def __init__(self, role, id, suspicious=False):
        self.knowledge = []
        self.social = random.uniform(0.5, 1)
        self.suspicious = suspicious
        self.alive = True
        self.role = role
        self.ID = id
        self.talk_list = []

    def add_knowledge(self, item):
        self.knowledge.append(item)

    def set_social(self, social):
        self.social = social
    
    def set_suspicion(self, suspicion):
        self.suspicion = suspicion
    
    def set_ID(self, ID):
        self.ID = ID

    def get_ID(self):
        return self.ID
    
    def talk_with(self, agent):
        # Add to player to talk list
        if agent not in self.talk_list:
            self.talk_list.append(agent)
