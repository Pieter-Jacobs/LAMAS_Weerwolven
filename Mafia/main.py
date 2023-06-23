import random
import matplotlib.pyplot as plt
import networkx as nx
from enum import Enum
from itertools import permutations, combinations
from difflib import SequenceMatcher

from mlsolver.kripke import World, KripkeStructure
from mlsolver.formula import Atom, Implies, Box_a

# Role class
class Role(Enum):
    Villager = 1
    Mafioso = 2
    Detective = 3

# GameEnd class
class GameEnd(Enum):
    Mafia_Wins = -1
    Continue = 0
    Townfolk_Wins = 1   

# Player class
class Player:
    def __init__(self, id, role, suspicious = False):
        self.id = id
        self.role = role
        self.suspicious = suspicious
        self.alive = True

        # Social parameters
        self.social = random.uniform(0.5, 1)
        self.talk_list = []
    
    def talk_with(self, player_id):
        # Add to player to talk list
        if player_id not in self.talk_list:
            self.talk_list.append(player_id)

# MafiaGame class
class MafiaGame:
    def __init__(self, nr_villagers, nr_mafia, nr_detectives):
        self.nr_villagers = nr_villagers
        self.nr_mafia = nr_mafia
        self.nr_detectives = nr_detectives

        self.initiate_players()
        self.initiate_model()

    def initiate_players(self):
        # Determine chance for townsfolk to be suspicious
        suspicious_chance = 0.5

        # Determine number of players
        self.nr_players = self.nr_villagers + self.nr_mafia + self.nr_detectives

        # Generate players
        self.players = []
        for id in range(self.nr_players):
            suspicious = False
            if random.random() < suspicious_chance:
                suspicious = True

            if id < self.nr_villagers:
                self.players.append(Player(id, Role.Villager, suspicious))
            elif id < self.nr_villagers + self.nr_mafia:
                self.players.append(Player(id, Role.Mafioso, True))
            elif id < self.nr_villagers + self.nr_mafia + self.nr_detectives:
                self.players.append(Player(id, Role.Detective, suspicious))
    
    def initiate_model(self):
        # Initiate world names
        roles = ['v'] * self.nr_villagers + ['m'] * self.nr_mafia + ['d'] * self.nr_detectives
        world_names = [''.join(world) for world in set(permutations(roles))]
        
        # Initiate worlds
        self.true_world = ''.join(roles)
        worlds = []
        for name in world_names:
            # Skip worlds in which none of the roles match the roles in the true world
            similar_roles = [letter for idx, letter in enumerate(name) if self.true_world[idx] == name[idx]]
            if len(similar_roles) == 0:
                continue

            # Make a new world
            world = World(name, {})

            # Determine initial propositions
            atoms = [name[idx] + str(idx) for idx in range(len(name))]
            for atom in atoms:
                world.assignment[atom] = True
                if self.players[int(atom[1])].suspicious:
                    # In every world, mafia are acting suspiciously
                    world.assignment['sus' + atom[1]] = True
            
            # Add world to world list
            worlds.append(world)
        
        # Initiate relations
        relations = {}
        for player_id, player_role in enumerate(self.true_world):
            # Initialize player relations
            player_relations = []

            # Create relations for worlds in which a player knows its own role
            related_worlds = [name for name in world_names if name[player_id] == player_role]
            for world1 in related_worlds:
                for world2 in related_worlds:
                    player_relations.append((world1, world2))

            # Create relations for worlds in which the mafia knows who their fellow mafia are
            if self.nr_mafia > 1 and player_role == 'm':
                for world1 in world_names:
                    mafia_ids = [id for id, role in enumerate(world1) if role == 'm']
                    for world2 in world_names:
                        other_mafia_ids = [id for id, role in enumerate(world2) if role == 'm']
                        if mafia_ids == other_mafia_ids:
                            player_relations.append((world1, world2))
            
            # Delete duplicate relations
            player_relations = list(dict.fromkeys(player_relations))
            relations[str(player_id)] = player_relations

        # Initiate Kripke structure
        self.model = KripkeStructure(worlds, relations)
        self.visualize_model()
    
    def visualize_model(self):
        """Visualizes the Kripke model worlds and relations."""
        # Create an empty directed graph
        graph = nx.DiGraph()

        # Add nodes (worlds) to the graph
        for world in self.model.worlds:
            graph.add_node(world.name)

        # Add edges (relations) to the graph
        for agent, relations in self.model.relations.items():
            for relation in relations:
                if relation in graph.edges:
                    current_labels = graph.edges[relation]['labels']
                    current_labels.append('R' + str(agent))
                    graph.edges[relation]['labels'] = current_labels
                else:
                    graph.add_edge(relation[0], relation[1], labels=['R' + str(agent)])

        # Set node positions using a spring layout algorithm
        pos = nx.circular_layout(graph)

        # Draw nodes (worlds)
        node_colors = ['lightblue'] * len(graph.nodes)
        if self.true_world in graph.nodes:
            true_world_index = list(graph.nodes).index(self.true_world)
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
                plt.text(x, y + 0.2, ','.join(graph.edges[edge]['labels']), fontsize=12, color='gray', ha='center')
                edge_labels.pop((u,v))

        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=12, font_color='black')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=12, font_color='gray')

        # Set plot title
        plt.title("Kripke Model Visualization")

        # Show the plot
        plt.axis('off')
        plt.show()

    def start(self):
        # Parameters
        self.max_talking_rounds = 2

        # Initial day phase (only discussion)
        print("--- Day phase ---")
        self.discussion_phase()

        while True:
            # Start day phase
            outcome = self.night_phase()
            if outcome != GameEnd.Continue:
                if outcome == GameEnd.Townfolk_Wins:
                    print("The townfolk win!")
                elif outcome == GameEnd.Mafia_Wins:
                    print("The mafia wins!")
                break
            
            # Start night phase
            outcome = self.day_phase()
            if outcome != GameEnd.Continue:
                if outcome == GameEnd.Townfolk_Wins:
                    print("The townfolk win!")
                elif outcome == GameEnd.Mafia_Wins:
                    print("The mafia wins!")
                break

    def reasoning_rules(self):
        # Talking with suspicious players
        for id1 in range(self.nr_players):
            for id2 in range(self.nr_players):
                id2_suspicious = self.players[id2].suspicious
                talk_list1 = self.players[id1].talk_list
                talk_list2 = self.players[id2].talk_list
                if id1 != id2 and id1 in talk_list2 and id2 in talk_list1 and id2_suspicious:
                    formula = Atom('sus' + str(id2))
                    print(formula)
                    self.model.solve_a(str(id1), formula)
                    pass
        pass

    def talking_round(self):
        # Determine which players start the talk
        nr_talks = int(self.nr_players / 2)
        agent_ids = list(range(self.nr_players))
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

                #self.reasoning_rules()
                self.visualize_model()

    def discussion_phase(self):
        print("-> Discussion phase")
        for round in range(self.max_talking_rounds):
            print("Talking round:", str(round+1))
            self.talking_round()

    def day_phase(self):
        print("--- Day phase ---")
        return GameEnd.Townfolk_Wins

    def night_phase(self):
        print("--- Night phase ---")
        return GameEnd.Continue

def main():
    game = MafiaGame(2,1,1)
    game.start()

if __name__ == "__main__":
    main()