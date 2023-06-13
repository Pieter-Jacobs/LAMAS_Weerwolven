from roles.agent import Agent

class Detective(Agent):

    def __init__(self):
        super().__init__("detective")

    def inspect(self):
        pass

    def discuss(self):
        print("blalbalblaa")

    def vote(self, players):
        pass
    
