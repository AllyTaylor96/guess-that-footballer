import os
import random
import shutil

import pandas as pd

from game_functions import choose_player, parse_difficulty, guess_player

def main() -> None:

    # terminal stuff
    terminal_width = shutil.get_terminal_size(fallback=(80, 20))[0]
    os.system('cls' if os.name == 'nt' else 'clear')

    welcome = ['Welcome to Guess That Footballer! You will try to guess',
               'a Premier League footballer, based on limited information.',
               'There are three difficulties you can choose from, which',
               'changes how obscure the chosen footballer may be.'
               ]

    for line in welcome:
        print(line.center(terminal_width), sep='\n')

    player_df = pd.read_csv('data/player_list.csv')

    play_again = True
    while play_again:

        difficulty = parse_difficulty(terminal_width)

        chosen_player = choose_player(player_df, difficulty)

        guess_player(chosen_player, terminal_width)

        # guessing logic in and working
        # need to implement scoring mechanism - ie. how many points for right,
        # how many lives player has, high score tracking etc.

        # maybe a good idea to remove some of the 'text' like the above welcome
        # into a separate location - either pickle it all or store it somewhere else
        # as it clogs up the actual code as is

        play_again = False



if __name__ == "__main__":
    main()
