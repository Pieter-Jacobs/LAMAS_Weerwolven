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
   for run in range(2):
      for strategy in ["Random", "Logic"]:
         mafiaGame = MafiaGame(2, 1, 0, visualize_ks=True)
         result = mafiaGame.start()
         results[strategy][result] += 1


   print(results)


if __name__ == '__main__':
   main()
