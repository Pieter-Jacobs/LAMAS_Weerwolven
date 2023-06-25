from mlsolver.kripke import World, KripkeStructure
from mlsolver.tableau import *
from mlsolver.formula import *

from itertools import permutations, product
from roles.Detective import Detective
from roles.Villager import Villager
from roles.Mafia import Mafia
from phases.day import Day
from phases.night import Night
import matplotlib.pyplot as plt
import networkx as nx
import random
from MafiaKripkeStructure import MafiaKripkeStructure


class MafiaGame:
    def __init__(self, n_villagers, n_mafia, n_detective, n_talking_round=1, visualize_ks=False):
        self.vizualize_ks = visualize_ks
        self.ks = MafiaKripkeStructure(n_villagers, n_mafia, n_detective)
        if visualize_ks:
            self.ks.visualize("Initial Kripke Model")
        self.day = Day(self.ks, self.ks.true_world, self.ks.players,
                       n_villagers, n_mafia, n_detective, n_talking_round)
        self.night = Night(self.ks, self.ks.true_world,
                           self.ks.players, n_villagers, n_mafia, n_detective)

    # Publicly announced that a player has been killed
    def public_announcement_killed(self, ks, killed_player):
        self.mafiaKripkeStructure.relations.pop(
            "agent" + str(killed_player.get_ID()))
        print("Player", str(self.players.index(killed_player)+1) + ",",
              "who was a", killed_player.role + ",", "was killed by the mafia! \n")
        return self.ks

    # Publicly announced that a player has been voted out
    def public_announcement_vote(self, ks, voted_player):
        self.mafiaKripkeStructure.relations.pop(
            "agent" + str(voted_player.get_ID()))
        print("Player", str(self.players.index(voted_player)+1) + ",",
              "who was a", voted_player.role + ",", "was voted out! \n")
        return self.ks

    # Checks if the game is over or not
    def game_status(self, n_v, n_m, n_d):
        print("Number of villagers: ", n_v)
        print("Number of detective: ", n_d)
        print("Number of mafia: ", n_m, "\n")
        if n_m == 0:
            print("Villagers won!")
            exit()
        if n_m > (n_d + n_v):
            print("Mafia won!")
            exit()
        else:
            print("Next round! \n")
            return False

    # Private announcement detective
    def update_detective_knowledge(self, agent, discovered_agent):
        formula = Atom(
            discovered_agent.role[0] + str(discovered_agent.get_ID()))
        self.ks.solve_a("agent" + str(agent.get_ID()), formula)
        return self

    # Game loop
    def start(self):
        self.max_talking_rounds = 2
        n_v, n_d, n_m = 0, 0, 0
        for player in self.ks.players:
            if player.role[0] == 'v':
                n_v += 1
            elif player.role[0] == 'd':
                n_d += 1
            else:
                n_m += 1
        print("In this game there are", n_v, "villagers,",
              n_m, "mafia, and", n_d, "detective. \n")

        result = None
        finished = False

        # Discussion phase
        self.day.discussion_phase()
        if self.vizualize_ks:
            self.ks.visualize(
                self.ks, self.ks.true_world, "Discussion phase")
        while not finished:
            #Night phase

            #Detective
            if n_d > 0:
                for player in self.players:
                    if player.role == "detective":
                        discovered_player = self.night.detective_phase()
                        self.update_detective_knowledge(
                            player, discovered_player)
                        self.visualize_kripke_model(self.ks, self.ks.true_world, str("Agent " + str(self.players.index(
                            player)+1) + " (detective) discovered the role of agent " + str(self.players.index(discovered_player)+1) + " (" + str(discovered_player.role)+")"))
                        first_run = False

            killed_player = self.night.mafia_phase()
            killed_player.alive = False

            #Public announcement of the killed player
            model = self.public_announcement_killed(self.ks, killed_player)
            self.visualize_kripke_model(model, self.ks.true_world, str(
                "Agent " + str(self.players.index(killed_player)+1) + " (" + str(killed_player.role) + ")" + " was killed!"))

            if killed_player.role == "detective":
                n_d -= 1
            else:
                n_v -= 1
            finished = self.game_status(n_v, n_m, n_d)

            #Discussion
            self.day.discussion_phase()

            #Voting
            voted_player = self.day.voting_phase()
            voted_player.alive = False

            #Public announcement of the voted player
            model = self.public_announcement_vote(model, voted_player)
            self.visualize_kripke_model(model, self.ks.true_world, str(
                "Agent " + str(self.players.index(voted_player)+1) + " (" + str(voted_player.role) + ")" + " was voted out!"))

            if voted_player.role == "detective":
                n_d -= 1
            elif voted_player.role == "villager":
                n_v -= 1
            else:
                n_m -= 1
            finished = self.game_status(n_v, n_m, n_d)
        return result
