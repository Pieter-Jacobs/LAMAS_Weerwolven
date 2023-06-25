from MafiaGame import MafiaGame


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
      for run in range(2):
            mafiaGame = MafiaGame(2, 1, 0, visualize_ks=False)
            result = mafiaGame.start()
            results[strategy][result].append(mafiaGame.get_avg_sociability()) 
   print(results)

if __name__ == '__main__':
   main()
