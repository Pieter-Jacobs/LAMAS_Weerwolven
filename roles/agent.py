import random

''' This class serves as the basis for each agent'''
class Agent():

    def __init__(self, role, id, suspicious=False):
        self.knowledge = []
        self.sociability = random.uniform(0, 1)
        self.suspicious = suspicious
        self.alive = True
        self.role = role
        self.ID = id
        self.talk_list = []

    def add_knowledge(self, item):
        self.knowledge.append(item)
    
    def add_talk(self, id):
        if id not in self.talk_list:
            self.talk_list.append(id)

    def set_sociability(self, sociability):
        self.sociability = sociability
    
    def set_ID(self, ID):
        self.ID = ID

    def get_ID(self):
        return self.ID
    
    def is_suspicious(self):
        return self.suspicious
