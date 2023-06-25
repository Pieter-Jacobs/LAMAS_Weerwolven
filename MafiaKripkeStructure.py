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


class MafiaKripkeStructure:
    def __init__(self, n_villagers, n_mafia, n_detective, sus_chance=0.1):
        self.sus_chance = sus_chance
        self.init_kripke_model(n_villagers, n_mafia, n_detective)

    def init_kripke_model(self, n_villagers, n_mafia, n_detective):
        agents = [
            f'agent{i + 1}' for i in range(n_villagers + n_mafia + n_detective)]
        game_roles = ['v'] * n_villagers + \
            ['m'] * n_mafia + ['d'] * n_detective
        # The true world is always the regular order of roles
        self.true_world = ''.join(game_roles)

        all_possible_roles = set(permutations(game_roles))

        sus_worlds = self.init_sus_worlds(all_possible_roles)
        self.players = self.create_sus_players(self.true_world)
        worlds = self.init_worlds(sus_worlds)
        relations = self.init_relations(worlds, agents)

        self.model = KripkeStructure(worlds, relations)

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

            # Randomly add suspicious townfolk
            self.true_world = list(sus_worlds[0])
            for i, role in enumerate(self.true_world):
                if role != 'm*' and random.random() <= self.sus_chance:
                    self.true_world[i] += '*'
            self.true_world = ''.join(tuple(self.true_world))
        return sus_worlds

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
            for world in worlds:
                agent_role = world.name.replace("*", "")[i]
                agent_world_mafia = [
                    j + 1 for j, role in enumerate(world.name.replace("*", "")) if role == "m"]
                agent_relations.extend(
                    [(world.name, w.name) for w in worlds if w.name.replace("*", "")[i] == agent_role and (agent_role != "m" or sorted(agent_world_mafia) == sorted([k + 1 for k, role in enumerate(w.name.replace("*", "")) if role == "m"]))])
            relations[agent] = set(agent_relations)
        return relations

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

    def visualize(self, title):
        """Visualizes the Kripke model worlds and relations."""
        graph = nx.DiGraph()

        # Add nodes (worlds) to the graph
        for world in self.model.worlds:
            graph.add_node(world.name)

        # Add edges (relations) to the graph
        for agent, relations in self.model.relations.items():
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
        if self.true_world in graph.nodes:
            true_world_index = list(graph.nodes).index(self.true_world)
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
