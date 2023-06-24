import random
from mlsolver.kripke import World, KripkeStructure
from mlsolver.tableau import *
from mlsolver.formula import *

class Day:
    def __init__(self, players, n_villagers, n_mafia, n_detectives, max_talking_rounds):
        self.players = players
        self.n_villagers = n_villagers
        self.n_mafia = n_mafia
        self.n_detectives = n_detectives
        self.max_talking_rounds = max_talking_rounds
    
    # Allows agents to talk to each other
    def discussion_phase(self,):
        print("-------------------------------- Discussion phase has started --------------------------------\n")
        for i in range(self.max_talking_rounds):
            self.talking_round()

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
    def talking_round(self):
        alive_players = []
        # Decide who's gonna try to start talking and who's gonna listen
        for player in self.players:
            if player.alive == True:
                alive_players.append(player)
        nr_talks = int(len(alive_players) / 2)
        agent_ids = list(range(len(alive_players)))
        talk_starters = random.sample(agent_ids, nr_talks)

        # Determine with which players the talk starters can talk
        talk_receivers = [player for player in agent_ids if player not in talk_starters]

        # Find out who talks to who
        for starter in talk_starters:
            receiver = talk_receivers.pop(0)

            # Only if both players want to talk, the talk starts
            if random.random() < self.players[starter].social and random.random() < self.players[receiver].social:
                # Talk starts
                print("Player " + str(starter) + " talks with player " + str(receiver))
                print(str(starter), str(self.players[starter].suspicious), str(self.players[starter].role))
                print(str(receiver), str(self.players[receiver].suspicious), str(self.players[starter].role))

                self.players[starter].talk_with(receiver)
                if self.players[receiver].suspicious:
                    formula = Atom('sus')

                self.players[receiver].talk_with(starter)

                self.reasoning_rules()
                #self.visualize_model()
        pass

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
