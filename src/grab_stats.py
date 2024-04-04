from argparse import ArgumentParser

import pandas as pd

from grabber import Grabber

def parse_args():

    parser = ArgumentParser(
        prog='dataGrabber',
        description='Grabs the data required for the game to run.'
    )

    parser.add_argument('-f', '--fbref_json',
                        type=str,
                        help='Path to .json file containing team-fbrefLink \
                        dictionary')

    args = parser.parse_args()

    return args


def main():

    args = parse_args()

    grabber = Grabber(args.fbref_json)

    grabber.grab()

    player_df = grabber.generate_players()

    sorted_player_df = player_df.sort_values('Playing Time Min',
                                             ascending=False)

    sorted_player_df.to_csv('data/player_list.csv', index=False)


if __name__ == "__main__":
    main()
