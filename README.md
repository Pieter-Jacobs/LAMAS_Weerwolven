# Mafia: a game project for LAMAS

Authors: Pieter Jacobs, Tom Veldhuis, Twan Vos

## Requirements
The necessary packages for this program to run can be found in `requirements.txt`.

## Usage
The program can either perform a single run, which can show intermediate Kripke structures during phases of the game and show the events taking place through the terminal:
```
python main.py [number of villagers] [number of mafia] [number of detectives] --vis --verbose
```

Or perform a simulation of a specified number of runs, after which results will be shown regarding the relation between win percentages of townfolk/mafia and sociability:
```
python main.py [number of villagers] [number of mafia] [number of detectives] --sim [number of runs]
```

More details about the used arguments can be found by running `python main.py -h`.

## References
- The 'mlsolver' library: https://github.com/erohkohl/mlsolver
    - Used for creating Kripke structures and interacting with modal logic
- The 'solve_a' function: https://github.com/JohnRoyale/MAS2018/blob/master/mlsolver/kripke.py#L36
    - Used for simulating private announcements within a Kripke structure