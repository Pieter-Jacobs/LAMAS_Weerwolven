from MafiaGame import MafiaGame
import matplotlib.pyplot as plt
from plot import *

def main():
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
      for run in range(100):
            mafiaGame = MafiaGame(1, 1, 1, visualize_ks=False, verbose=False)
            result = mafiaGame.start()
            results[strategy][result].append(mafiaGame.get_avg_sociability()) 

   plot_sociability_box(results)
   plot_win_percentages(results)

if __name__ == '__main__':
   main()
