import random

''' This class serves as the basis for each agent'''
class Agent():

    def __init__(self, role, id):
        self.knowledge = []
        self.social = random.uniform(0.5, 1)
        self.suspicion = 'no'
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
        talk_chance = random.random()
        receive_chance = random.random()
        if talk_chance < self.social and receive_chance < agent.social:
            # Both agents want to talk
            self.talk_list.append(agent.get_ID())
            agent.talk_list.append(self.get_ID())
            return True
        # Agents don't want to talk
        return False