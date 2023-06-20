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
        #self.init_players(n_villagers, n_mafia, n_detective)
        self.init_kripke_model(n_villagers, n_mafia, n_detective) 
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
        self.true_world = ''.join(game_roles)

        all_possible_roles = set(permutations(game_roles))

        #true_world = random.choice(list(all_possible_roles))
        #true_world = ''.join(true_world)
        self.players = self.create_players(self.true_world)
        print("True world of this game: ", self.true_world)

        # Create the worlds for the Kripke structure
        worlds = []
        for roles in all_possible_roles:
            world_name = ''.join(roles)
            world = World(world_name, {})
            for i, role in enumerate(roles):
                #if role != 'v':
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
                                agent_relations.append((world.name, world_2.name))
                        else:
                            agent_relations.append((world.name, world_2.name))
            relations[agent] = set(agent_relations)
        
        # Create the Kripke structure
        self.ks = KripkeStructure(worlds, relations)
        self.visualize_kripke_model(self.ks, self.true_world)

        #Initialise the day & night
        max_talking_rounds = 3
        self.day = Day(self.players, n_villagers, n_mafia, n_detective, max_talking_rounds)
        self.night = Night(self.players, n_villagers, n_mafia, n_detective)
        
        return self.ks
    
    # Creates the players based on the true world
    def create_players(self, true_world):
        self.players = []
        idx = 1
        for agent in true_world:
            if agent == 'v':
                self.players.append(Villager(idx))
            if agent == 'm':
                self.players.append(Mafia(idx))
            if agent == 'd':
                self.players.append(Detective(idx))
            idx += 1
        return self.players
    
    # Publicly announced that a player has been killed
    def public_announcement_killed(self, ks, killed_player):
        formula = Box_star(Atom(str(killed_player.role[0]+str(self.players.index(killed_player)+1))))
        model = ks.solve(formula)
        print("Player", str(self.players.index(killed_player)+1) + ",", "who was a", killed_player.role + ",", "was killed by the mafia! \n")
        return model

    # Publicly announced that a player has been voted out
    def public_announcement_vote(self, ks, voted_player):   
        formula = Box_star(Atom(str(voted_player.role[0]+str(self.players.index(voted_player)+1))))
        model = ks.solve(formula)
        print("Player", str(self.players.index(voted_player)+1) + ",", "who was a", voted_player.role + ",", "was voted out! \n")
        return model

    # Visualizes the kripke model
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
            
        nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=1500)

        # Draw edges (relations)
        nx.draw_networkx_edges(graph, pos, arrowstyle='->', arrowsize=10, edge_color='gray')

        # Draw labels (world roles and relation labels)
        labels = {node: node for node in graph.nodes}
        edge_labels = {(u, v): ','.join(data['labels']) for u, v, data in graph.edges(data=True)}

        # Adjust positions of self-loop labels
        for edge in graph.edges:
            u, v = edge
            if u == v:
                x, y = pos[u]
                plt.text(x, y + 0.2, ','.join(graph.edges[edge]['labels']), fontsize=8, color='gray', ha='center')
                edge_labels.pop((u,v))

        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=8, font_color='black')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8, font_color='gray')

        # Set plot title
        plt.title("Kripke Model Visualization")

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

    # Game loop
    def start(self):
        n_v, n_d, n_m = 0,0,0
        removed_players = []
        for player in self.players:
            if player.role[0] == 'v':
                n_v += 1
            elif player.role[0] == 'd':
                n_d += 1
            else:
                n_m += 1

        print("In this game there are", n_v, "villagers,", n_m, "mafia, and", n_d, "detective.")

        result = None
        finished = False
        first_run = True
        while not finished:
            #Night phase
            if n_d > 0:
                self.night.detective_phase() 
            killed_player = self.night.mafia_phase(removed_players)
            removed_players.append(killed_player)
            
            #Public announcement of the killed player
            if first_run:
                model = self.public_announcement_killed(self.ks, killed_player)
            else:
                model = self.public_announcement_killed(model, killed_player)
            self.visualize_kripke_model(model, self.true_world)

            if killed_player.role == "detective":
                n_d -= 1
            else:
                n_v -= 1
            finished = self.game_status(n_v, n_m, n_d)

            #Day phase
            voted_player = self.day.voting_phase(removed_players)
            removed_players.append(voted_player)

            #Public announcement of the voted player
            model = self.public_announcement_vote(model, voted_player)
            self.visualize_kripke_model(model, self.true_world)

            if voted_player.role == "detective":
                n_d -= 1
            elif voted_player.role == "villager":
                n_v -= 1
            else:
                n_m -= 1
            finished = self.game_status(n_v, n_m, n_d)
            first_run = False
        return result
        
