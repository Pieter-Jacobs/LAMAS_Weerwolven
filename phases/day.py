class Day:
    def __init__(self, players, n_villagers, n_mafia, n_detectives):
        self.players = players
        self.n_villagers = n_villagers
        self.n_mafia = n_mafia
        self.n_detectives = n_detectives

    # Public announcement is made, adding the information to each players' knowledge
    def announcement_phase(self, information):
        for player in self.players:
            player.add_knowledge(information)
    
    # Allows agents to talk to each other
    def discussion_phase(self):
        for player in self.players:
            #might not use this and instead just do the talking here, but its here if needed
            player.discuss()

    # Allows agents to vote based on their knowledge
    def voting_phase(self):
        print("Voting phase has started \n")
        votes = {}
        for player in self.players:
            vote = player.vote(self.players)
            if vote in votes:
                votes[vote] += 1
            else:
                votes[vote] = 1
        max_votes = max(votes.values())
        removed_player = [player for player, vote_count in votes.items() if vote_count == max_votes]
        return removed_player

    
