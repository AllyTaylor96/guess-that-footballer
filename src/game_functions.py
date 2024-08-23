import os
import random
from difflib import SequenceMatcher

import pandas as pd


def choose_player(player_df: pd.DataFrame, difficulty: str) -> dict:

    # cut pool of players based on difficulty
    filtered_df = filter_on_difficulty(player_df, difficulty)

    player_pool_size = filtered_df.shape[0]
    player_idx = random.randint(0, player_pool_size-1)

    return dict(filtered_df.iloc[player_idx])

def guess_player(player_info: dict, terminal_width: int) -> bool:

    player_name = player_info['Player']

    os.system('cls' if os.name == 'nt' else 'clear')

    player_detail = [
        f"\n",
        f"Age: {int(player_info['Age'])}",
        f"Nationality: {player_info['Nation']}",
        f"Team: {player_info['Team']}",
        f"Position: {player_info['Position']}",
        f"Starts: {player_info['Playing_Time_Starts']}",
        f"Goals: {int(player_info['Performance_Gls'])}",
        f"Assists: {int(player_info['Performance_Gls'])}\n",
        f"Who am I?"
    ]

    for line in player_detail:
        print(line.center(terminal_width), sep='\n')

    player_guess = str(input(f"> "))
    correctness = assess_player_guess(player_name, player_guess)

    if correctness > 0.75:
        correct = True
    else:
        correct = False

    result = [
        "\n",
        f"Guessed player: {player_guess}",
        f"True player: {player_name}",
        f"Correct? {correct}"
    ]

    for line in result:
        print(line.center(terminal_width), sep='\n')

def assess_player_guess(true_name: str, guessed_name: str) -> bool:

    closeness = SequenceMatcher(None, true_name, guessed_name).ratio()
    return closeness


def parse_difficulty(terminal_width: int) -> str:

    # ensure difficulty is valid
    allowed_inputs = ['easy', 'e', 'medium', 'm', 'hard', 'h', 'exit', 'quit']

    difficulty_preamble = [
        "\n",
        "What difficulty would you like to play?",
        "Choose from 'Easy (e)', 'Medium (m)' or 'Hard (h)'."
    ]

    while True:
        try:
            for line in difficulty_preamble:
                print(line.center(terminal_width), sep='\n')

            difficulty_input = str(input(f"> ".rjust(terminal_width//2)))

            if difficulty_input not in allowed_inputs:
                raise ValueError()
        except ValueError:
            print(f'{difficulty_input} not acceptable input. Try again - allowed inputs are -> {str(allowed_inputs)}')
        else:
            break

    # return appropriate input
    if difficulty_input.lower() in ['easy', 'e']:
        return 'easy'
    elif difficulty_input.lower() in ['medium', 'm']:
        return 'medium'
    elif difficulty_input.lower() in ['hard', 'h']:
        return 'hard'
    elif difficulty_input.lower() in ['exit', 'quit']:
        exit()


def filter_on_difficulty(player_df: pd.DataFrame, difficulty: str) -> pd.DataFrame:

    if difficulty == 'hard':
        hard_df = player_df[(player_df.Playing_Time_Starts > 5)]
        return hard_df

    elif difficulty == 'medium':
        medium_df = player_df[(player_df.Playing_Time_Starts > 19)]
        return medium_df

    elif difficulty == 'easy':
        top_six_teams = [
            'Arsenal',
            'Chelsea',
            'Liverpool',
            'Manchester United',
            'Manchester City',
            'Tottenham'
        ]

        easy_df = player_df[(player_df.Playing_Time_Starts > 19)
                            & (player_df.Team.isin(top_six_teams))]
        return easy_df
