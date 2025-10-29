import numpy as np
import pandas as pd
import plotly.express as px
import re

import plotly.io as pio
pio.renderers.default = "browser"

allyears = pd.concat(pd.read_csv(f'wta_matches_{year}.csv')
                     .assign(year=year) for year in range(2020,2025))

def get_unique_players(matches):
    unique_players = pd.concat([matches['winner_name'],matches['loser_name']]).unique()
    return unique_players

def build_serve_stats_graph(matches = allyears):

    unique_players = pd.concat([matches['winner_name'],matches['loser_name']]).unique()
    serve = pd.DataFrame(columns=['name','a_per_match','df_per_match', 'fs_per_match', 'ss_per_match'])

    for player in unique_players:

        all_games_played = pd.concat([matches[matches.winner_name==player],matches[matches.loser_name==player]])
        if len(all_games_played) >= 50:

            count1 = matches[matches.winner_name==player]['w_ace'].sum()
            count2 = matches[matches.loser_name==player]['l_ace'].sum()
            a_per_match = (count1 + count2) / len(all_games_played)
            #aces

            count1 = matches[matches.winner_name==player]['w_1stWon'].sum()
            count2 = matches[matches.loser_name==player]['l_1stWon'].sum()
            fs_per_match = (count1 + count2) / len(all_games_played)
            #first serves

            count1 = matches[matches.winner_name==player]['w_2ndWon'].sum()
            count2 = matches[matches.loser_name==player]['l_2ndWon'].sum()
            ss_per_match = (count1 + count2) / len(all_games_played)
            #second serves

            count1 = matches[matches.winner_name==player]['w_df'].sum()
            count2 = matches[matches.loser_name==player]['l_df'].sum()
            df_per_match = (count1 + count2) / len(all_games_played)
            #second serves

            serve.loc[len(serve)] = [player, a_per_match,df_per_match, fs_per_match, ss_per_match]
    
    for h in ['a_per_match','df_per_match', 'fs_per_match', 'ss_per_match']:
        max = serve[h].max()
        serve[h] = serve[h] / max

    serve['df_per_match'] = 1 - serve['df_per_match']
    serve['serve_score'] = serve.drop('name',axis=1).sum(axis=1)
    serve['serve_score'] = serve['serve_score'] / 4

    sorted_serves = serve.sort_values(by='serve_score', ascending=False).reset_index(drop=True)
    sorted_serves.index.name = 'rank'


    fig = px.scatter(
        sorted_serves,
        x=sorted_serves.index,
        y='serve_score',
        text='name', 
        title='WTA Servers ranked (serve_score calculated between 0 and 1 for each player, with 1 being the greatest possible score).'
    )
    fig.update_traces(textposition='top center')
    return fig

def build_match_length_graph(matches = allyears):

    winners = matches[['winner_name','minutes']].rename(
        columns= {
            'winner_name': 'name',
            'minutes': 'length'
        }
    )

    losers = matches[['loser_name','minutes']].rename(
        columns= {
            'loser_name': 'name',
            'minutes': 'length'
        }
    )

    allmatches = pd.concat([losers, winners], ignore_index=True)
    length_totals = allmatches.groupby('name')[['length']].sum()
    matches_played = allmatches.groupby('name').size().rename('matches_played')

    length_stats = length_totals.join(matches_played)
    length_stats = length_stats[length_stats['length'] > 0]
    length_stats = length_stats[length_stats['matches_played'] >= 50]
    length_stats = (length_stats['length'] / length_stats['matches_played']).rename("average_length")

    df = length_stats.reset_index()  # index becomes 'name' column
    df.columns = ['name', 'average_length']
    df = df.sort_values(by='average_length', ascending=False).reset_index(drop=True)
    df.index.name = 'rank'
    print(df)
    
    fig = px.scatter(
        df,
        x=df.index,
        y='average_length',
        text='name', 
        title='Players ranked by average match length (minutes)'
    )
    fig.update_traces(textposition='top center')
    return fig





#build_serve_stats_graph(matches = allyears)
build_match_length_graph()