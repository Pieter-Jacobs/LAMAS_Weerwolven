import random
from mlsolver.kripke import World, KripkeStructure
from mlsolver.tableau import *
from mlsolver.formula import *

from mlsolver.formula import Atom, Box_a

class Day:
    def __init__(self, model, players, n_villagers, n_mafia, n_detectives, max_talking_rounds):
        self.model = model
        self.players = players
        self.n_villagers = n_villagers
        self.n_mafia = n_mafia
        self.n_detectives = n_detectives
        self.max_talking_rounds = max_talking_rounds
    
    # Allows agents to talk to each other
    def discussion_phase(self,):
        print("-------------------------------- Discussion phase has started --------------------------------\n")
        for i in range(self.max_talking_rounds):
            self.talking_round(i+1)
        print("")

    def reasoning_rules(self):
        alive_players =[]
        for player in self.players:
            if player.alive == True:
                alive_players.append(player)
        # Talking with suspicious players
        for id1 in range(len(alive_players)):
            for id2 in range(len(alive_players)):
                id2_suspicious = alive_players[id2].suspicious
                talk_list1 = alive_players[id1].talk_list
                talk_list2 = alive_players[id2].talk_list
                if id1 != id2 and id1 in talk_list2 and id2 in talk_list1 and id2_suspicious:
                    formula = Atom('sus' + str(id2))
                    #model.solve_a(str(id1), formul)
                    pass
        pass

    # Perform a talking round
    def talking_round(self, round):
        print("--- Round " + str(round) + " ---")
        # Decide who's gonna try to start talking and who's gonna listen
        nr_talking_starters = int(len(self.players) / 2)
        talking_starters = random.sample(self.players, k=nr_talking_starters)
        talking_partners = [player for player in self.players if player not in talking_starters]

        # Find out who's willing to talk
        talk_counter = 0
        for starter in talking_starters:
            # Find talking partner
            talking_partner = None
            for partner in talking_partners:
                if random.random() < starter.get_social() and random.random() < partner.get_social():
                    print("Agent " + str(starter.get_ID()) + " talked with agent " + str(partner.get_ID()))
                    talking_partner = partner
                    talk_counter += 1
                    
                    # Add partners to talk lists
                    starter.add_talk(partner.get_ID())
                    partner.add_talk(starter.get_ID())

                    # Exchange knowledge
                    if starter.is_suspicious():
                        formula = Box_a(partner.get_ID()+1, "sus")
                        pass
                    if partner.is_suspicious():
                        print("sus2")
                        pass
                    break
            
            # Remove partner from the list if starter has talked to them this round
            if talking_partner != None:
                talking_partners.remove(talking_partner)
        
        if talk_counter == 0:
            print("Nobody wanted to talk!")

    # Allows agents to vote based on their knowledge
    def voting_phase(self):
        print("-------------------------------- Voting phase has started --------------------------------\n")
        votes = {}
        for player in self.players:
            # Make sure the players who were removed can't vote
            if player.alive == True:
                vote = player.vote(self.players)
                print(player.role, "(agent", str(self.players.index(player)+1) + ")", "voted for: ", vote.role, "(agent",str(self.players.index(vote)+1) + ")")
                if vote in votes:
                    votes[vote] += 1
                else:
                    votes[vote] = 1
            else:
                pass
        print("\n")
        max_votes = max(votes.values())
        removed_player = [player for player, vote_count in votes.items() if vote_count == max_votes]

        if len(removed_player) == 1:
            return removed_player[0]
        else:
            return random.choice(removed_player)
