import argparse
from pathlib import Path

import pandas as pd

from grabber import Grabber

def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        prog='dataGrabber',
        description='Grabs the data required for the game to run.'
    )

    parser.add_argument('-f', '--fbref_json',
                        type=str,
                        help='Path to .json file containing team-fbrefLink \
                        dictionary',
                        required=True)

    args = parser.parse_args()

    return args


def main():

    args = parse_args()

    if Path(args.fbref_json).exists():
        print(f'Grabbing data from links provided at {str(args.fbref_json)}')
        grabber = Grabber(args.fbref_json)
    else:
        print('No valid fbref path provided... exiting')

    grabber.grab()
    player_df = grabber.generate_players()
    sorted_player_df = player_df.sort_values('Playing Time Min',
                                             ascending=False)
    sorted_player_df.to_csv('data/player_list.csv', index=False)


if __name__ == "__main__":
    main()
