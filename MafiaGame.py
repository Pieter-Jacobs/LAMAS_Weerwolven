from mlsolver.kripke import World, KripkeStructure
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

        agents = ['agent' + str(i + 1) for i in range(n_villagers + n_mafia + n_detective)]

        # Create all possible combinations of agent roles
        game_roles = ['v'] * n_villagers + ['m'] * n_mafia + ['d'] * n_detective
        true_world = ':'.join([agent + ':' + role for agent, role in zip(agents, game_roles)])

        all_possible_roles = set(permutations(game_roles))

        # Create the worlds for the Kripke structure
        worlds = []
        for roles in all_possible_roles:
            world_name = ':'.join([agent + ':' + role for agent, role in zip(agents, roles)])
            world = World(world_name, {})
            for i, agent in enumerate(agents):
                mafia_formula = ' ^ '.join([f'(mafia{j} ∨ ¬mafia{j})' for j in range(1, len(agents) + 1) if j != (i + 1)])
                knowledge_formula = f'K{i + 1}({mafia_formula})'
                world.assignment[knowledge_formula] = True
            worlds.append(world)
        print(worlds[0])
        # Create the relations dictionary based on the agent's role in each world
        relations = {}
        for i, agent in enumerate(agents):
            agent_relations = []
            for j, world in enumerate(worlds):
                agent_roles = world.name.split(':')[1::2]
                agent_role = agent_roles[i]
                for world_2 in worlds: 
                    agent_roles = world_2.name.split(':')[1::2] 
                    if agent_roles[i] == agent_role:
                        agent_relations.append((world.name, world_2.name))
            relations[agent] = set(agent_relations)

        # Create the Kripke structure
        ks = KripkeStructure(worlds, relations)
        self.visualize_kripke_model(ks, true_world)
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
                # If we already had another agent with this edge, we expand the agent array
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
        labels = {}
        edge_labels = {}

        for node, data in graph.nodes(data=True):
            roles = node.split(':')[1::2]
            role_label = ''.join(roles)
            labels[node] = role_label

        for u, v, data in graph.edges(data=True):
            edge_labels[(u, v)] = ",".join(data['labels'])

        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=10, font_color='black')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8, font_color='gray')

        # Set plot title
        plt.title("Kripke Model Visualization")

        # Show the plot
        plt.axis('off')
        plt.show()
                
    # Creates the players without ID
    def init_players(self, n_villagers, n_mafia, n_detective):
        self.players=[]
        for x in range(0,n_villagers):  
            self.players.append(Villager())

        for x in range(0,n_mafia):  
            self.players.append(Mafia())

        for x in range(0,n_detective):  
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
        
