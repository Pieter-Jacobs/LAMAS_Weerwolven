from MafiaGame import MafiaGame
import matplotlib.pyplot as plt
import argparse
from plot import *
import random
# Runs a simulation of multiple runs of the game of Mafia
# and returns results regarding win percentages and sociability
def simulate_results(n_villagers, n_mafia, n_detectives, sim_runs):
   results = {
       "Random": {
           "Mafia": [],
           "Townfolk": []
       },
       "Logic": {
           "Mafia": [],
           "Townfolk": []
       }
   }

   for strategy in ["Random", "Logic"]:
      for run in range(sim_runs):
            mafiaGame = MafiaGame(n_villagers, n_mafia, n_detectives, visualize_ks=False, verbose=False)
            if strategy == "Random":
                result = mafiaGame.start(True, True)
            elif strategy == "Logic":
                result = mafiaGame.start()
            results[strategy][result].append(mafiaGame.get_avg_sociability()) 

   plot_sociability_box(results)
   plot_win_percentages(results)

def main():
   # Initialize the argument parser
   parser = argparse.ArgumentParser()
   parser.add_argument("n_v", help="number of villagers")
   parser.add_argument("n_m", help="number of mafia")
   parser.add_argument("n_d", help="number of detectives")
   parser.add_argument("-s", "--sim", nargs='?', default=-1, const=100, help="run a simulation of SIM runs (comparing random vs. strategy)")
   parser.add_argument("--vis", action="store_true", help="visualize the Kripke structures (during a single run)")
   parser.add_argument("-v", "--verbose", action="store_true", help="turn verbose on (during a single run)")
   args = parser.parse_args()

   # Determine the parameter values
   n_villagers = int(args.n_v)
   n_mafia = int(args.n_m)
   n_detectives = int(args.n_d)
   sim_runs = int(args.sim)
   vis = args.vis
   verbose = args.verbose
   
   # Run the program
   if sim_runs != -1:
      # Perform a simulation
      simulate_results(n_villagers, n_mafia, n_detectives, sim_runs)
   else:
      # Perform a single run
      mafiaGame = MafiaGame(n_villagers, n_mafia, n_detectives, visualize_ks=vis, verbose=verbose)
      mafiaGame.start()

if __name__ == '__main__':
   main()
