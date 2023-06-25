import random
from mlsolver.kripke import World, KripkeStructure
from mlsolver.tableau import *
from mlsolver.formula import *

# Class containing all the events that take place in the day phase
class Day:
    
    def __init__(self, ks, n_villagers, n_mafia, n_detectives, max_talking_rounds, verbose):
        self.verbose = verbose
        self.ks = ks
        self.n_villagers = n_villagers
        self.n_mafia = n_mafia
        self.n_detectives = n_detectives
        self.max_talking_rounds = max_talking_rounds

    # Allows agents to talk to each other
    def discussion_phase(self):
        if self.verbose:
            print("-------------------------------- Discussion phase has started --------------------------------\n")
        for i in range(self.max_talking_rounds):
            self.talking_round(i+1)

    # Performs reasoning rules that involve talking on two agents
    def talking_rules(self, agent1, agent2):
        # If one of two talking agents is acting suspicious, the other will know
        if agent1.is_suspicious():
            formula = Atom("sus" + str(agent1.get_ID()))
            self.ks.model.solve_a("agent" + str(agent2.get_ID()), formula)
        if agent2.is_suspicious():
            formula = Atom("sus" + str(agent2.get_ID()))
            self.ks.model.solve_a("agent" + str(agent1.get_ID()), formula)

        # Sharing suspicions
        alive_players = ["agent" + str(player.get_ID())
                         for player in self.ks.players if player.alive]
        other_players = [agent[5:] for agent in self.ks.model.relations.keys(
        ) if agent in alive_players and agent[5:] != str(agent1.get_ID()) and agent[5:] != str(agent2.get_ID())]
        for player in other_players:
            # Check whether agent 1 knows that another player is suspicious
            formula = Box_a("agent" + str(agent1.get_ID()),
                            Atom("sus" + player))
            if formula.semantic(self.ks.model, self.ks.true_world):
                # If true, agent 2 knows that agent 1 knows that another player is suspicious
                formula = Box_a("agent" + str(agent2.get_ID()), formula)
                self.ks.model.solve_a("agent" + str(agent2.get_ID()), formula)

            # Check whether agent 2 knows that another player is suspicious
            formula = Box_a("agent" + str(agent2.get_ID()),
                            Atom("sus" + player))
            if formula.semantic(self.ks.model, self.ks.true_world):
                # If true, agent 1 knows that agent 2 knows that another player is suspicious
                formula = Box_a("agent" + str(agent1.get_ID()), formula)
                self.ks.model.solve_a("agent" + str(agent1.get_ID()), formula)

    # Perform a talking round
    def talking_round(self, round):
        if self.verbose:
            print("--- Round " + str(round) + " ---")
        # Decide who's gonna try to start talking and who's gonna listen
        talking_players = [
            player for player in self.ks.players if player.alive]
        nr_talking_starters = int(len(talking_players) / 2)
        talking_starters = random.sample(
            talking_players, k=nr_talking_starters)
        talking_partners = [
            player for player in talking_players if player not in talking_starters]

        # Find out who's willing to talk
        talk_counter = 0
        for starter in talking_starters:
            # Find talking partner
            talking_partner = None
            for partner in talking_partners:
                if random.random() < starter.sociability and random.random() < partner.sociability:
                    if self.verbose:
                        print("Agent " + str(starter.get_ID()) +
                            " talked with agent " + str(partner.get_ID()))
                    talking_partner = partner
                    talk_counter += 1

                    # Exchange knowledge
                    self.talking_rules(starter, partner)
                    break

            # Remove partner from the list if starter has talked to them this round
            if talking_partner != None:
                talking_partners.remove(talking_partner)

        if talk_counter == 0 and self.verbose:
            print("Nobody wanted to talk!")

    # Allows agents to vote based on their knowledge
    def voting_phase(self, vote_randomly = False):
        if self.verbose:
            print("-------------------------------- Voting phase has started --------------------------------\n")
        votes = {}
        for player in self.ks.players:
            # Make sure the players who were removed can't vote
            if player.alive == True:
                # Random vote choice
                vote = None
                if player.role == "mafia":
                    # Mafia voting strategy
                    vote_players = [agent for agent in self.ks.players if agent.get_ID(
                    ) != player.get_ID() and agent.role != "mafia" and agent.alive == True]
                    if len(vote_players) == 1:
                        # Only one possible alive player that isn't mafia
                        vote = vote_players[0]
                    else:
                        # Check for knowledge about players that have suspicions about this mafioso
                        for agent in vote_players:
                            formula = Box_a("agent" + str(player.get_ID()), Box_a(
                                "agent" + str(agent.get_ID()), Atom("sus" + str(player.get_ID()))))
                            if formula.semantic(self.ks.model, self.ks.true_world):
                                vote = agent
                                break
                        # If no luck yet, pick randomly
                        if vote == None or vote_randomly:
                            vote = random.choice([agent for agent in vote_players if agent.get_ID(
                            ) != player.get_ID() and agent.alive])
                else:
                    # Townfolk voting strategy
                    vote_players = [agent for agent in self.ks.players if agent.get_ID(
                    ) != player.get_ID() and agent.alive == True]
                    if len(vote_players) == 1:
                        # Only one possible alive player
                        vote = vote_players[0]
                    else:
                        # Check for knowledge about suspicions
                        for agent in vote_players:
                            formula = Box_a(
                                "agent" + str(player.get_ID()), Atom("sus" + str(agent.get_ID())))
                            if formula.semantic(self.ks.model, self.ks.true_world):
                                vote = agent
                                break
                        # Check for knowledge about people who have suspicions
                        for agent in vote_players:
                            for agent2 in [other_agent for other_agent in vote_players if other_agent.get_ID() != agent.get_ID()]:
                                formula = Box_a("agent" + str(player.get_ID()), Box_a(
                                    "agent" + str(agent.get_ID()), Atom("sus" + str(agent2.get_ID()))))
                                if formula.semantic(self.ks.model, self.ks.true_world):
                                    vote = agent
                                    break
                        # If no luck yet, pick randomly
                        if vote == None or vote_randomly:
                            vote = random.choice([agent for agent in vote_players if agent.get_ID(
                            ) != player.get_ID() and agent.alive])
                    pass

                if self.verbose:
                    print(player.role, "(agent", str(self.ks.players.index(player)+1) + ")",
                          "voted for: ", vote.role, "(agent", str(self.ks.players.index(vote)+1) + ")")
                
                # Add the agent's vote to the total votes
                if vote in votes:
                    votes[vote] += 1
                else:
                    votes[vote] = 1
        if self.verbose: print("\n")

        # Determine the player to kill with the most votes
        max_votes = max(votes.values())
        removed_player = [player for player,
                          vote_count in votes.items() if vote_count == max_votes]

        if len(removed_player) == 1:
            return removed_player[0]
        else:
            # If there are 2 or more players with the max votes,
            # pick randomly from those players
            return random.choice(removed_player)
