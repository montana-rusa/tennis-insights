import numpy as np
import pandas as pd
import plotly.express as px
import re

import plotly.io as pio
pio.renderers.default = "browser"

allyears = pd.concat(pd.read_csv(f'wta_matches_{year}.csv')
                     .assign(year=year) for year in range(2020,2025))

def calculate_games(score):

    sets = re.findall(r'(\d+)-(\d+)',score)
    sets = [(int(w),int(l)) for w, l in sets]
    
    w_games = 0
    l_games = 0

    for w, l in sets:
        w_games += w
        l_games += l

    return w_games, l_games

def get_won_games(name, matches):
    matches_won = matches[matches.winner_name==name]
    count = sum(calculate_games(score)[0] for _,score in matches_won.score.items())
    return count
   
def get_lost_games(name, matches):
    matches_lost = matches[matches.loser_name==name]
    count = sum(calculate_games(score)[1] for _,score in matches_lost.score.items())
    return count

def calc_average_games(name,matches):

    games1 = get_won_games(name, matches)
    games2 = get_lost_games(name, matches)
    all_games_played = pd.concat([matches[matches.winner_name==name],matches[matches.loser_name==name]])
    game_count = len(pd.concat([matches[matches.winner_name==name],matches[matches.loser_name==name]]))
    return (games1 + games2)/game_count

def average_game_length(name, matches):
    all_matches = pd.concat([matches[matches.winner_name==name], matches[matches.loser_name==name]])
    average = all_matches.minutes.sum() / len(all_matches)
    return average

def build_graph(name, metric_name, matches=allyears):
    ys = []
    for year in range(2020,2025):
        matches = pd.read_csv(f'wta_matches_{year}.csv')

        if metric_name == "average_games_per_match":
            ys.append(calc_average_games(name,matches))
            data = {
            'years': [2020,2021,2022,2023,2024],
            metric_name : ys }

        
        if metric_name == "average_game_length":
            ys.append(average_game_length(name,matches))
            data = {
            'years': [2020,2021,2022,2023,2024],
            metric_name : ys }
    df = pd.DataFrame(data)

    fig = px.line(df, y=metric_name, x='years')
    return fig
#average games per match

#build_graph("Iga Swiatek", "average_game_length", allyears)