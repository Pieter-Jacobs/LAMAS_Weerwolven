import random

''' This class serves as the basis for each agent'''
class Agent():

    def __init__(self, role):
        self.knowledge = []
        self.social = random.uniform(0,1)
        self.suspicion = 'no'
        self.role = role
        self.ID = 0

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