import json
import time
from pathlib import Path

import pandas as pd


class Grabber:

    def __init__(self, team_json_path: Path):

        self.team_links_dict = self._load_json(team_json_path)
        self.team_list = self.team_links_dict.keys()

        self.team_dfs = {}
        self.player_df = []

    def _load_json(self, team_json: Path) -> dict:

        with open(team_json, 'r') as f:
            data = json.load(f)

        return data

    def grab(self):

        team_dfs = {}

        for team in self.team_list:
            print(f'Grabbing data for {team}...')
            data_link = self.team_links_dict[team]
            team_df = pd.read_html(data_link)[0]

            time.sleep(5.0)  # fbref only accepts 10 requests per min

            team_df.columns = [' '.join(col).strip()
                               for col in team_df.columns]
            team_df = team_df.reset_index(drop=True)

            team_df['Team'] = team

            cleaned_df = self._clean(team_df)

            team_dfs[team] = cleaned_df

        self.team_dfs = team_dfs

    def generate_players(self) -> pd.DataFrame:

        player_df = pd.concat(self.team_dfs.values())

        return player_df

    def _clean(self, df):

        new_columns = []
        for col in df.columns:
            if 'level_0' in col:
                new_col = col.split()[-1]  # takes the last name
            else:
                new_col = col
            new_columns.append(new_col)

        df.columns = new_columns
        df = df.fillna(0)

        bad_indices = list(df.index[df['Player'].isin(['Squad Total', 'Opponent Total'])])
        df = df.drop(bad_indices)


        df['Position'] = df['Pos'].str[:2]
        df['Position_2'] = df['Pos'].str[3:]
        df['Nation'] = df['Nation'].str.split(' ').str.get(1)
        df = df.drop(columns=['Pos', 'Matches'])

        df['Position'] = df['Position'].replace({'MF': 'Midfielder',
                                                 'DF': 'Defender',
                                                 'FW': 'Forward',
                                                 'GK': 'Goalkeeper'})
        df['Position_2'] = df['Position_2'].replace({'MF': 'Midfielder',
                                                     'DF': 'Defender',
                                                     'FW': 'Forward',
                                                     'GK': 'Goalkeeper'})

        df.columns = [col.replace(' ', '_') for col in df.columns]
        return df
