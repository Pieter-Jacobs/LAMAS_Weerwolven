from MafiaGame import MafiaGame


def main():
   results = {
       "Random": {
           "Mafia": 0,
           "Townfolk": 0
       },
       "Logic": {
           "Mafia": 0,
           "Townfolk": 0,
       }
   }
   avg_sociabilities = []

   for strategy in ["Random", "Logic"]:
      sociability = []
      for run in range(2):
            mafiaGame = MafiaGame(2, 1, 0, visualize_ks=True)
            result = mafiaGame.start()
            results[strategy][result] += 1
            sociability.append(mafiaGame.get_avg_sociability())
      avg_sociabilities.append(sociability)
   print(results)
   print(avg_sociabilities)

if __name__ == '__main__':
   main()
