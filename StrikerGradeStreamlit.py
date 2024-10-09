import pandas as pd
import numpy as np
from scipy.stats import norm
from datetime import datetime
import streamlit as st


def StrikerFunction(dataframe):
    # these are the columns we are using
    number_columns = ['mins played', 'Yellow Card', 'Red Card', 'Goal', 'Assist', 'Dribble',
           'Goal Against', 'Stand. Tackle', 'Unsucc Stand. Tackle', 
           'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter', 'Att 1v1', 'Efforts on Goal', 'Att Aerial',
           'Shot on Target', 'Pass into Oppo Box', 'Tackle', 'Clear', 'Unsucc Tackle',
           'Forward', 'Unsucc Forward', 'Line Break', 'Header on Target', 'Cross', 'Unsucc Cross',
           'Loss of Poss', 'Success', 'Unsuccess', 'Foul Won', 'Progr Regain ', 'Stand. Tackle Success ',
           'Pass Completion ', 'Progr Pass Attempt ', 'Progr Pass Completion ', 'Efficiency ', 'PK Missed', 'PK Scored']

    #details = selected.loc[:, ['Player Full Name', 'Team Name', 'As At Date', 'Position Tag']]
    details = dataframe.loc[:, ['Player Full Name', 'Team Name', 'Match Date', 'Position Tag', 'Starts']]
    details.reset_index(drop=True, inplace=True)
    selected = dataframe.loc[:, ~dataframe.columns.duplicated()]
    selected_p90 = selected.loc[:, number_columns].astype(float)

    per90 = ['Yellow Card', 'Red Card', 'Goal', 'Assist', 'Dribble',
           'Stand. Tackle', 'Unsucc Stand. Tackle',
           'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter',
           'Att 1v1', 'Efforts on Goal', 'Tackle', 'Clear', 'Unsucc Tackle',
           'Shot on Target', 'Pass into Oppo Box', 'Att Aerial',
           'Forward', 'Unsucc Forward', 'Line Break', 'Header on Target', 'Cross', 'Unsucc Cross',
           'Loss of Poss', 'Success', 'Unsuccess', 'Foul Won', 'PK Missed', 'PK Scored']

    selected_p90['minutes per 90'] = selected_p90['mins played']/90

    for column in per90:
        if column not in ['Goal', 'Assist', 'Yellow Card', 'Red Card', 'PK Missed']:
            selected_p90[column] = selected_p90[column] / selected_p90['minutes per 90']

    selected_p90 = selected_p90.drop(columns=['minutes per 90'])
    selected_p90.reset_index(drop=True, inplace=True)

    total_def_actions_columns = ['Tackle', 'Clear', 'Progr Inter', 'Unprogr Inter', 'Progr Rec', 
                             'Unprogr Rec', 'Stand. Tackle', 'Unsucc Stand. Tackle', 
                             'Unsucc Tackle']
    selected_p90['Total Def Actions'] = selected_p90[total_def_actions_columns].sum(axis=1)
    defending = selected_p90['Total Def Actions']
    defending.fillna(0, inplace=True)

    shooting = selected_p90[['Efforts on Goal']]
    shooting.fillna(0, inplace=True)

    dribbling = selected_p90[['Dribble']]
    dribbling.fillna(0, inplace=True)

    total_att_actions_columns = ['Goal', 'Assist', 'Att 1v1', 'Att Aerial', 'Efforts on Goal', 'Header on Target', 
                             'Shot on Target', 'Cross', 'Unsucc Cross', 'Pass into Oppo Box', 'Foul Won']
    selected_p90['Total Att Actions'] = selected_p90[total_att_actions_columns].sum(axis=1)
    attacking = selected_p90['Total Att Actions']
    attacking.fillna(0, inplace=True)



    adjustments = selected_p90[['Yellow Card', 'Red Card', 'Goal', 'Assist', 'Att Aerial', 'PK Missed', 'PK Scored']]

    for index, row in adjustments.iterrows():
        if adjustments['PK Scored'][index] == 1:
            adjustments['Goal'][index] = adjustments['Goal'][index] - 1
        elif adjustments['PK Scored'][index] == 2:
            adjustments['Goal'][index] = adjustments['Goal'][index] - 2
    adjustments.fillna(0, inplace=True)
    adjustments['Yellow Card'] = adjustments['Yellow Card'] * -.2
    adjustments['Red Card'] = adjustments['Red Card'] * -2
    adjustments['Goal'] = adjustments['Goal'] * .7
    adjustments['Assist'] = adjustments['Assist'] * .45
    adjustments['Att Aerial'] = adjustments['Att Aerial'] * .05
    adjustments['PK Missed'] = adjustments['PK Missed'] * -1
    adjustments['PK Scored'] = adjustments['PK Scored'] * 0.4

    def calculate_percentile(value):
        return norm.cdf(value) * 100

    # Function to calculate z-score for each element in a column
    def calculate_zscore(column, mean, std):
        return (column - mean) / std

    def clip_percentile(value):
        return max(min(value, 100), 50)

    player_location = []
    for index, row in details.iterrows():
        if 'ATT' in row['Position Tag']:
            player_location.append(index)
    
    final = pd.DataFrame()
    readding = []
    selected_p90 = pd.concat([details, selected_p90], axis=1)

    for i in player_location:
        more_data = selected_p90.iloc[i]
        player_name = more_data['Player Full Name']
        team_name = more_data['Team Name']
        date = more_data['Match Date']
        
        if ('U13' in team_name) or ('U14' in team_name):
            cf_df = pd.read_csv("IDP_Plan/Thresholds/StrikerThresholds1314.csv")
        elif ('U15' in team_name) or ('U16' in team_name):
            cf_df = pd.read_csv("IDP_Plan/Thresholds/StrikerThresholds1516.csv")
        elif ('U17' in team_name) or ('U19' in team_name):
            cf_df = pd.read_csv("IDP_Plan/Thresholds/StrikerThresholds1719.csv")


        mean_values = cf_df.iloc[0, 0]
        std_values = cf_df.iloc[1, 0]
        # Calculate the z-score for each data point
        z_scores_df = defending.transform(lambda col: calculate_zscore(col, mean_values, std_values))
        defending_percentile = z_scores_df.map(calculate_percentile)
        defending_percentile = defending_percentile.map(clip_percentile)
        will_defending = defending_percentile.iloc[player_location].reset_index()
        weights = np.array([0.1])
        defending_score = (
            will_defending['Total Def Actions'] * weights[0]
        )
        
        mean_values = cf_df.iloc[0, 1]
        std_values = cf_df.iloc[1, 1]
        z_scores_df = shooting.transform(lambda col: calculate_zscore(col, mean_values, std_values))
        shooting_percentile = z_scores_df.map(calculate_percentile)
        shooting_percentile = shooting_percentile.map(clip_percentile)
        player_shooting = shooting_percentile.iloc[player_location]
        weights = np.array([.1])
        shooting_score = (
            player_shooting['Efforts on Goal'] * weights[0]
        )

        mean_values = cf_df.iloc[0, 2]
        std_values = cf_df.iloc[1, 2]
        z_scores_df = dribbling.transform(lambda col: calculate_zscore(col, mean_values, std_values))
        dribbling_percentile = z_scores_df.map(calculate_percentile)
        dribbling_percentile = dribbling_percentile.map(clip_percentile)
        player_dribbling = dribbling_percentile.iloc[player_location]
        weights = np.array([.1])
        dribbling_score = (
            player_dribbling['Dribble'] * weights[0]
        )

        mean_values = cf_df.iloc[0, 3]
        std_values = cf_df.iloc[1, 3]
        z_scores_df = attacking.transform(lambda col: calculate_zscore(col, mean_values, std_values))
        attacking_percentile = z_scores_df.map(calculate_percentile)
        attacking_percentile = attacking_percentile.map(clip_percentile)
        player_attacking = attacking_percentile.iloc[player_location]
        weights = np.array([.1])
        attacking_score = (
            player_attacking * weights[0]
        )

        add = adjustments.iloc[i, :].sum()
        readding.append(add)
        
        final_grade = (defending_score * .2) + (shooting_score * .2) + (dribbling_score * 0.2) + (attacking_score * 0.2)


        final['Defending'] = defending_score
        final['Shooting'] = shooting_score
        final['Final Grade'] = final_grade
        final['Player Name'] = player_name
        final['Team Name'] = team_name
        final['Date'] = date


    player_name = []
    player_minutes = []
    player_position = []
    player_starts = []
    for i in player_location:
         player_name.append(selected_p90['Player Full Name'][i])
         player_minutes.append(selected_p90['mins played'][i])
         player_position.append(selected_p90['Position Tag'][i])
         player_starts.append(selected_p90['Starts'][i])
    final['Minutes'] = player_minutes
    final['Player Name'] = player_name
    final['Position'] = player_position
    final['Started'] = player_starts
    final['Adjustments'] = readding


    return final





