import random
import math

class Day:
    def __init__(self, players, n_villagers, n_mafia, n_detectives, max_talking_rounds):
        self.players = players
        self.n_villagers = n_villagers
        self.n_mafia = n_mafia
        self.n_detectives = n_detectives
        self.max_talking_rounds = max_talking_rounds

    # Public announcement is made, adding the information to each players' knowledge
    def announcement_phase(self, information):
        for player in self.players:
            player.add_knowledge(information)
    
    # Allows agents to talk to each other
    def discussion_phase(self):
        for i in range(self.max_talking_rounds):
            self.talking_round()

    # Perform a talking round
    def talking_round(self):
        # Decide who's gonna try to start talking and who's gonna listen
        nr_talking_starters = math.floor(len(self.players) / 2)
        talking_starters = random.choices(self.players, k=nr_talking_starters)
        talking_partners = [player for player in self.players if player not in talking_starters]

        # Find out who's willing to talk
        for starter in talking_starters:
            idx = 0
            while idx < len(talking_partners):
                partner = talking_partners[idx]
                if starter.talk_with(partner):
                    print("Agent " + str(starter.get_ID()) + " talked with agent " + str(partner.get_ID()))
                    talking_partners.remove(partner)

                    # Add knowledge

                    break
                idx += 1
        pass

    # Allows agents to vote based on their knowledge
    def voting_phase(self, removed_players):
        print("-------------------------------- Voting phase has started --------------------------------\n")
        votes = {}
        for player in self.players:
            # Make sure the players who were removed can't vote
            if player not in removed_players:
                vote = player.vote(self.players, removed_players)
                if vote in votes:
                    votes[vote] += 1
                else:
                    votes[vote] = 1
            else:
                pass
        max_votes = max(votes.values())
        removed_player = [player for player, vote_count in votes.items() if vote_count == max_votes]

        if len(removed_player) == 1:
            return removed_player[0]
        else:
            return random.choice(removed_player)
