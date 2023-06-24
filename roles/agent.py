import random

''' This class serves as the basis for each agent'''
class Agent():

    def __init__(self, role, id, suspicous):
        self.knowledge = []
        self.social = random.uniform(0.5, 1)
        self.suspicious = suspicous
        self.role = role
        self.ID = id
        self.talk_list = []

    def add_knowledge(self, item):
        self.knowledge.append(item)
    
    def add_talk(self, id):
        if id not in self.talk_list:
            self.talk_list.append(id)

    def set_social(self, social):
        self.social = social
    
    def set_ID(self, ID):
        self.ID = ID

    def get_ID(self):
        return self.ID
    
    def get_social(self):
        return self.social
    
    def is_suspicious(self):
        return self.suspicious