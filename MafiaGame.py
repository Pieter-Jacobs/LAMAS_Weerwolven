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


class MafiaGame:
    def __init__(self, n_villagers, n_mafia, n_detective, visualize_steps=False):
        self.init_kripke_model(n_villagers, n_mafia, n_detective)

    def init_kripke_model(self, n_villagers, n_mafia, n_detective):
        agents = [
            f'agent{i + 1}' for i in range(n_villagers + n_mafia + n_detective)]
        game_roles = ['v'] * n_villagers + \
            ['m'] * n_mafia + ['d'] * n_detective

        # The true world is always the regular order of roles
        self.true_world = ''.join(game_roles)
        print("True world of this game: ", self.true_world)
        
        all_possible_roles = set(permutations(game_roles))

        sus_worlds = self.init_sus_worlds(all_possible_roles)
        self.players = self.create_sus_players(self.true_world)

        worlds = self.init_worlds(sus_worlds)
        relations = self.init_relations(worlds, agents)

        self.ks = KripkeStructure(worlds, relations)
        self.visualize_kripke_model(
            self.ks, self.true_world, "Initial Kripke Model")

        max_talking_rounds = 2
        self.day = Day(self.ks, self.true_world, self.players,
                       n_villagers, n_mafia, n_detective, max_talking_rounds)
        self.night = Night(self.ks, self.true_world,
                           self.players, n_villagers, n_mafia, n_detective)


    def init_sus_worlds(self, all_possible_roles):
        sus_worlds = []
        for world in all_possible_roles:
            sus_combinations = list(product([0, 1], repeat=len(world)))
            mafia_indexes = [idx for idx,
                             role in enumerate(world) if role == "m"]
            binary_worlds = []
            for sus in sus_combinations:
                add_to_worlds = True
                for idx in mafia_indexes:
                    if sus[idx] == 0:
                        add_to_worlds = False
                if add_to_worlds:
                    binary_worlds.append(sus)
            current_sus_worlds = self.apply_suspicion_markings(
                world, binary_worlds)
            sus_worlds += current_sus_worlds
            if ''.join(world) == self.true_world:
                self.true_world = ''.join(random.choice(current_sus_worlds))
        return sus_worlds

    def apply_suspicion_markings(self, world, binary_worlds):
        current_sus_worlds = []
        for binary_world in binary_worlds:
            sus_world = []
            for idx, sus in enumerate(binary_world):
                if sus == 0:
                    sus_world.append(world[idx])
                elif sus == 1:
                    sus_world.append(world[idx] + '*')
            current_sus_worlds.append(tuple(sus_world))
        return current_sus_worlds

    def init_worlds(self, sus_worlds):
        worlds = []
        for roles in sus_worlds:
            world_name = ''.join(roles)
            world = World(world_name, {})
            for i, role in enumerate(roles):
                if len(role) == 2 or role[0] == "m":
                    atom = f'{role[0]}{i + 1}'
                    sus_atom = f'sus{i + 1}'
                    world.assignment[atom] = True
                    world.assignment[sus_atom] = True
                else:
                    atom = f'{role}{i + 1}'
                    world.assignment[atom] = True
            worlds.append(world)
        return worlds

    def init_relations(self, worlds, agents):
        relations = {}
        for i, agent in enumerate(agents):
            agent_relations = []
            for j, world in enumerate(worlds):
                agent_role = world.name.replace("*", "")[i]
                for world_2 in worlds:
                    agent2_role = world_2.name.replace("*", "")[i]
                    if agent_role == agent2_role:
                        if agent_role == "m":
                            world_1_mafia = [
                                i + 1 for i, x in enumerate(world.name.replace("*", "")) if x == "m"]
                            world_2_mafia = [
                                i + 1 for i, x in enumerate(world_2.name.replace("*", "")) if x == "m"]
                            if sorted(world_1_mafia) == sorted(world_2_mafia):
                                agent_relations.append(
                                    (world.name, world_2.name))
                        else:
                            agent_relations.append((world.name, world_2.name))
            relations[agent] = set(agent_relations)
        return relations

    # Creates the players based on the true world
    def create_players(self, true_world):
        self.players = []
        idx = 1
        for agent in true_world:
            suspicious = False
            print(random.random())
            if random.random() < 0.25:
                suspicious = True

            if agent == 'v':
                self.players.append(Villager(idx, suspicious))
            if agent == 'm':
                self.players.append(Mafia(idx, True))
            if agent == 'd':
                self.players.append(Detective(idx, suspicious))
            idx += 1
        return self.players

    def create_sus_players(self, true_world):
        # Determine which players are suspicious
        sus_indexes = [idx for idx, char in enumerate(
            true_world) if char == "*"]
        idx = 1
        for char in true_world:
            if char == "*":
                sus_indexes[idx-1] -= idx
                idx += 1

        # Generate players of true world
        self.players = []
        for idx, agent in enumerate(true_world.replace("*", "")):
            suspicious = False
            if idx in sus_indexes or agent == "m":
                suspicious = True

            if agent == 'v':
                self.players.append(Villager(idx+1, suspicious))
            if agent == 'm':
                self.players.append(Mafia(idx+1, suspicious))
            if agent == 'd':
                self.players.append(Detective(idx+1, suspicious))
        return self.players

    # Publicly announced that a player has been killed
    def public_announcement_killed(self, ks, killed_player):
        self.ks.relations.pop("agent" + str(killed_player.get_ID()))
        print("Player", str(self.players.index(killed_player)+1) + ",",
              "who was a", killed_player.role + ",", "was killed by the mafia! \n")
        return self.ks

    # Publicly announced that a player has been voted out
    def public_announcement_vote(self, ks, voted_player):
        self.ks.relations.pop("agent" + str(voted_player.get_ID()))
        print("Player", str(self.players.index(voted_player)+1) + ",",
              "who was a", voted_player.role + ",", "was voted out! \n")
        return self.ks

    # Visualizes the kripke model
    def visualize_kripke_model(self, kripke_model, true_world, title):
        """Visualizes the Kripke model worlds and relations."""
        # Create an empty directed graph
        # if len(kripke_model.worlds) > 150:
        #     return

        graph = nx.DiGraph()

        # Add nodes (worlds) to the graph
        for world in kripke_model.worlds:
            graph.add_node(world.name)

        # Add edges (relations) to the graph
        for agent, relations in kripke_model.relations.items():
            for relation in relations:
                if relation in graph.edges:
                    current_labels = graph.edges[relation]['labels']
                    current_labels.append('R' + agent[5:])
                    graph.edges[relation]['labels'] = current_labels
                else:
                    graph.add_edge(relation[0], relation[1], labels=[
                                   'R' + agent[5:]])

        # Set node positions using a spring layout algorithm
        pos = nx.circular_layout(graph)

        # Draw nodes (worlds)
        node_colors = ['lightblue'] * len(graph.nodes)
        if true_world in graph.nodes:
            true_world_index = list(graph.nodes).index(true_world)
            node_colors[true_world_index] = 'green'

        nx.draw_networkx_nodes(
            graph, pos, node_color=node_colors, node_size=1500)

        # Draw edges (relations)
        nx.draw_networkx_edges(graph, pos, arrowstyle='->',
                               arrowsize=10, edge_color='gray')

        # Draw labels (world roles and relation labels)
        labels = {node: node for node in graph.nodes}
        edge_labels = {(u, v): ','.join(data['labels'])
                       for u, v, data in graph.edges(data=True)}

        # Adjust positions of self-loop labels
        for edge in graph.edges:
            u, v = edge
            if u == v:
                x, y = pos[u]
                plt.text(
                    x, y + 0.2, ','.join(graph.edges[edge]['labels']), fontsize=8, color='gray', ha='center')
                edge_labels.pop((u, v))

        nx.draw_networkx_labels(graph, pos, labels=labels,
                                font_size=8, font_color='black')
        nx.draw_networkx_edge_labels(
            graph, pos, edge_labels=edge_labels, font_size=8, font_color='gray')

        # Set plot title
        plt.title(title)

        # Show the plot
        plt.axis('off')
        plt.show()

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
        for player in self.players:
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
        self.visualize_kripke_model(
            self.ks, self.true_world, "Discussion phase")
        while not finished:
            #Night phase

            #Detective
            if n_d > 0:
                for player in self.players:
                    if player.role == "detective":
                        discovered_player = self.night.detective_phase()
                        self.update_detective_knowledge(
                            player, discovered_player)
                        self.visualize_kripke_model(self.ks, self.true_world, str("Agent " + str(self.players.index(
                            player)+1) + " (detective) discovered the role of agent " + str(self.players.index(discovered_player)+1) + " (" + str(discovered_player.role)+")"))
                        first_run = False

            killed_player = self.night.mafia_phase()
            killed_player.alive = False

            #Public announcement of the killed player
            model = self.public_announcement_killed(self.ks, killed_player)
            self.visualize_kripke_model(model, self.true_world, str(
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
            self.visualize_kripke_model(model, self.true_world, str(
                "Agent " + str(self.players.index(voted_player)+1) + " (" + str(voted_player.role) + ")" + " was voted out!"))

            if voted_player.role == "detective":
                n_d -= 1
            elif voted_player.role == "villager":
                n_v -= 1
            else:
                n_m -= 1
            finished = self.game_status(n_v, n_m, n_d)
        return result
