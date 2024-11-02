import pandas as pd
import numpy as np
from scipy.stats import norm

def creatingPercentilesCB(merged_df):

    raw_columns = ['Stand. Tackle Success ', 'Line Break', 'Pass Completion ', 'Progr Regain ']

    def calculate_percentile(value):
        return norm.cdf(value) * 100

        # Function to calculate z-score for each element in a column
    def calculate_zscore(column, mean, std):
        return (column - mean) / std

    per90 = ['Goal', 'Dribble',
        'Stand. Tackle', 'Unsucc Stand. Tackle', 'Tackle',
        'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter',
        'Att 1v1', 'Efforts on Goal',
        'Shot on Target', 'Forward', 'Unsucc Forward', 'Line Break',
        'Loss of Poss', 'Success', 'Unsuccess']

    merged_df['minutes per 90'] = merged_df['mins played']/90

    for column in per90:
        merged_df[column] = merged_df[column] / merged_df['minutes per 90']
        
    merged_df = merged_df.drop(columns=['minutes per 90'])
    merged_df.fillna(0, inplace=True)

    merged_df = merged_df.drop_duplicates()
    raw_df = merged_df[raw_columns]

    passing = merged_df[['Forward', 'Unsucc Forward', 'Success', 'Unsuccess', 'Pass Completion ']]
    passing['Forward Total'] = passing['Forward'] + passing['Unsucc Forward']
    passing['Forward Completion'] = (passing['Forward'] / passing['Forward Total']) * 100
    passing['Total'] = passing['Success'] + passing['Unsuccess']
    passing.fillna(0, inplace=True)
    passing = passing.loc[:,['Forward Total', 'Forward Completion', 'Total', 'Pass Completion ']]

    defending = merged_df[['Stand. Tackle', 'Unsucc Stand. Tackle', 'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter', 'Progr Regain ', 
                            'Stand. Tackle Success ']]
    defending['Stand. Tackle Total'] = defending['Stand. Tackle'] + defending['Unsucc Stand. Tackle']
    defending['Rec Total'] = defending['Progr Rec'] + defending['Unprogr Rec']
    defending['Inter Total'] = defending['Progr Inter'] + defending['Unprogr Inter']
    defending.fillna(0, inplace=True)
    defending = defending.loc[:, ['Stand. Tackle Total', 'Rec Total', 'Inter Total', 'Progr Regain ', 
                                'Stand. Tackle Success ']]

    ball_progression = merged_df[['Line Break', 'Dribble', 'Att 1v1',
                            'Loss of Poss']]
    ball_progression.fillna(0, inplace=True)

    final_pizza = pd.DataFrame(columns=['Pass %', 'Line Breaks', 'Progr Regain %', 
                                        'Tackle %', 'Player Name', 'Team Name', 'Minutes'])
    player_name = merged_df.at[0, 'Player Full Name']
    team_name = merged_df.at[0, 'Team Name']
    
    cb_df = pd.read_csv("Thresholds/CenterBackSeasonThresholds.csv")
    
    mean_values = cb_df.iloc[0, [5,6,7,8,9,15]]
    std_values = cb_df.iloc[1, [5,6,7,8,9,15]]
    # Calculate the z-score for each data point
    z_scores_df = passing.transform(lambda col: calculate_zscore(col, mean_values[col.name], std_values[col.name]))
    passing_percentile = z_scores_df.applymap(calculate_percentile)
    player_passing = passing_percentile

    mean_values = cb_df.iloc[0, [0,1,2,3,4,16]]
    std_values = cb_df.iloc[1, [0,1,2,3,4,16]]
    # Calculate the z-score for each data point
    z_scores_df = defending.transform(lambda col: calculate_zscore(col, mean_values[col.name], std_values[col.name]))
    defending_percentile = z_scores_df.applymap(calculate_percentile)
    player_defending = defending_percentile

    mean_values = cb_df.iloc[0, [10, 11, 12, 13, 14]]
    std_values = cb_df.iloc[1, [10, 11, 12, 13, 14]]
    # Calculate the z-score for each data point
    z_scores_df = ball_progression.transform(lambda col: calculate_zscore(col, mean_values[col.name], std_values[col.name]))
    ball_prog_percentile = z_scores_df.applymap(calculate_percentile)
    player_ball_prog = ball_prog_percentile
    
    minutes_total = merged_df.at[0, 'mins played']
    date = merged_df.at[0, 'Year']
    
    final_pizza.loc[0, 'Pass %'] = float(raw_df['Pass Completion '][0])
    final_pizza.loc[0, 'Progr Regain %'] = float(raw_df['Progr Regain '][0])
    final_pizza.loc[0, 'Tackle %'] = float(raw_df['Stand. Tackle Success '][0])
    final_pizza.loc[0, 'Line Breaks'] = float(raw_df['Line Break'][0])
    final_pizza.loc[0, 'Rec Total Percentile'] = float(player_defending['Rec Total'])
    final_pizza.loc[0, 'Progr Regain Percentile'] = float(player_defending['Progr Regain '])
    final_pizza.loc[0, 'Stand. Tackle Success'] = float(player_defending['Stand. Tackle Success '])
    final_pizza.loc[0, 'Forward Total Percentile'] = float(player_passing['Forward Total'])
    final_pizza.loc[0, 'Passing Total Percentile'] = float(player_passing['Total'])
    final_pizza.loc[0, 'Pass Completion Percentile'] = float(player_passing['Pass Completion '])
    final_pizza.loc[0, 'Forward Completion Percentile'] = float(player_passing['Forward Completion'])
    final_pizza.loc[0, 'Line Break Percentile'] = float(player_ball_prog['Line Break'])
    final_pizza.loc[0, 'Loss of Poss Percentile'] = float(100-player_ball_prog['Loss of Poss'])
    final_pizza.loc[0, 'Player Name'] = player_name
    final_pizza.loc[0, 'Team Name'] = team_name
    final_pizza.loc[0, 'Minutes'] = minutes_total
    final_pizza.loc[0, 'Date'] = date

    final_pizza.drop_duplicates(subset=['Player Name'], inplace=True)

    # Drop duplicates to keep only one pair of player and team names

    return final_pizza

def creatingRawCB(merged_df):

    raw_columns = ['Stand. Tackle Success ', 'Line Break', 'Pass Completion ', 'Progr Regain ']

    def calculate_percentile(value):
        return norm.cdf(value) * 100

        # Function to calculate z-score for each element in a column
    def calculate_zscore(column, mean, std):
        return (column - mean) / std

    per90 = ['Goal', 'Dribble',
        'Stand. Tackle', 'Unsucc Stand. Tackle', 'Tackle',
        'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter',
        'Att 1v1', 'Efforts on Goal',
        'Shot on Target', 'Forward', 'Unsucc Forward', 'Line Break',
        'Loss of Poss', 'Success', 'Unsuccess']

    merged_df['minutes per 90'] = merged_df['mins played']/90

    for column in per90:
        merged_df[column] = merged_df[column] / merged_df['minutes per 90']
        
    merged_df = merged_df.drop(columns=['minutes per 90'])
    merged_df.fillna(0, inplace=True)

    merged_df = merged_df.drop_duplicates()
    raw_df = merged_df[raw_columns]

    passing = merged_df[['Forward', 'Unsucc Forward', 'Success', 'Unsuccess', 'Pass Completion ']]
    passing['Forward Total'] = passing['Forward'] + passing['Unsucc Forward']
    passing['Forward Completion'] = (passing['Forward'] / passing['Forward Total']) * 100
    passing['Total'] = passing['Success'] + passing['Unsuccess']
    passing.fillna(0, inplace=True)
    passing = passing.loc[:,['Forward Total', 'Forward Completion', 'Total', 'Pass Completion ']]

    defending = merged_df[['Stand. Tackle', 'Unsucc Stand. Tackle', 'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter', 'Progr Regain ', 
                            'Stand. Tackle Success ']]
    defending['Stand. Tackle Total'] = defending['Stand. Tackle'] + defending['Unsucc Stand. Tackle']
    defending['Rec Total'] = defending['Progr Rec'] + defending['Unprogr Rec']
    defending['Inter Total'] = defending['Progr Inter'] + defending['Unprogr Inter']
    defending.fillna(0, inplace=True)
    defending = defending.loc[:, ['Stand. Tackle Total', 'Rec Total', 'Inter Total', 'Progr Regain ', 
                                'Stand. Tackle Success ']]

    ball_progression = merged_df[['Line Break', 'Dribble', 'Att 1v1',
                            'Loss of Poss']]
    ball_progression.fillna(0, inplace=True)

    combined_aspects = pd.concat([defending, ball_progression, passing], axis=1)
    combined_aspects['Player Name'] = merged_df['Player Full Name']
    combined_aspects['Team Name'] = merged_df['Team Name']
    combined_aspects['Year'] = merged_df['Year']

    front_columns = ['Player Name', 'Team Name', 'Year']
    combined_aspects = combined_aspects[front_columns + [col for col in combined_aspects.columns if col not in front_columns]]


    return combined_aspects
