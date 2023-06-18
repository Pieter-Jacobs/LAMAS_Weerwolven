from mlsolver.kripke import World, KripkeStructure
from mlsolver.tableau import *
from mlsolver.formula import *

from itertools import permutations
from roles.Detective import Detective
from roles.Villager import Villager
from roles.Mafia import Mafia
from phases.day import Day
from phases.night import Night
import matplotlib.pyplot as plt
import networkx as nx


class MafiaGame:
    def __init__(self, n_villagers, n_mafia, n_detective):
        self.init_kripke_model(n_villagers, n_mafia, n_detective)
        self.init_players(n_villagers, n_mafia, n_detective)
        pass

    def init_kripke_model(self, n_villagers, n_mafia, n_detective):
        """Builds the initial Kripke model world, where everyone believes everyone can be any role,
        m1: agent 1 is mafia
        d1: agent 1 is detective
        v1: agent 1 is villager
        """

        agents = [f'agent{i + 1}' for i in range(n_villagers + n_mafia + n_detective)]

        # Create all possible combinations of agent roles
        game_roles = ['v'] * n_villagers + ['m'] * n_mafia + ['d'] * n_detective
        true_world = ''.join(game_roles)

        all_possible_roles = set(permutations(game_roles))

        # Create the worlds for the Kripke structure
        worlds = []
        for roles in all_possible_roles:
            world_name = ''.join(roles)
            world = World(world_name, {})
            for i, role in enumerate(roles):
                if role != 'v':
                    atom = f'{role}{i + 1}'
                    world.assignment[atom] = True
                
            worlds.append(world)

        # Create the relations dictionary based on the agent's role in each world
        relations = {}
        for i, agent in enumerate(agents):
            agent_relations = []
            for j, world in enumerate(worlds):
                agent_role = world.name[i]
                for world_2 in worlds:
                    # We add the world to the relation if the agents role is the same in the other, since he only knows his own role
                    if world_2.name[i] == agent_role:
                        if agent_role == 'm': 
                             # However, the mafia also knows the role of ther mafiosi, so they have extra knowledge and only get relations to worlds where the mafia is the same as in the other
                            world_1_mafia = [i+1 for i, x in enumerate(world.name) if x == "m"]
                            world_2_mafia = [i+1 for i, x in enumerate(world_2.name) if x == "m"]
                            if sorted(world_1_mafia) == sorted(world_2_mafia):
                                print("same")
                                agent_relations.append((world.name, world_2.name))
                        else:
                            agent_relations.append((world.name, world_2.name))
            relations[agent] = set(agent_relations)

        # Create the Kripke structure
        ks = KripkeStructure(worlds, relations)
        self.visualize_kripke_model(ks, true_world)
        self.test_initialization(ks)
        return ks

    def visualize_kripke_model(self, kripke_model, true_world):
        """Visualizes the Kripke model worlds and relations."""
        # Create an empty directed graph
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
                    graph.add_edge(relation[0], relation[1], labels=['R' + agent[5:]])

        # Set node positions using a spring layout algorithm
        pos = nx.spring_layout(graph)

        # Draw nodes (worlds)
        node_colors = ['lightblue'] * len(graph.nodes)
        if true_world in graph.nodes:
            true_world_index = list(graph.nodes).index(true_world)
            node_colors[true_world_index] = 'green'
        nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=500)

        # Draw edges (relations)
        nx.draw_networkx_edges(graph, pos, arrowstyle='->', arrowsize=10, edge_color='gray')

        # Draw labels (world roles and relation labels)
        labels = {node: node for node in graph.nodes}
        edge_labels = {(u, v): ','.join(data['labels']) for u, v, data in graph.edges(data=True)}

        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=10, font_color='black')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8, font_color='gray')

        # Set plot title
        plt.title("Kripke Model Visualization")

        # Show the plot
        plt.axis('off')
        plt.show()

    # Creates the players without ID
    def init_players(self, n_villagers, n_mafia, n_detective):
        self.players = []
        for x in range(0, n_villagers):
            self.players.append(Villager())

        for x in range(0, n_mafia):
            self.players.append(Mafia())

        for x in range(0, n_detective):
            self.players.append(Detective())

    def start(self):
        result = None
        finished = False

        day = Day(self.players)

        day.game_status()
        print(self.players)
        while not finished:
            finished = True

        return result

    def test_initialization(self, ks):
        formula = Box_a('agent1', Atom('m3'))
        model = ks.solve(formula)
        self.visualize_kripke_model(model, 'vvmm')