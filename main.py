from MafiaGame import MafiaGame


def main():
   # for run in range(100):
   #    for use_reasoning in [True, False]:
   
   mafiaGame = MafiaGame(2,1, 0, visualize_ks=True)
   mafiaGame.start()

if __name__ == '__main__':
   main() 
