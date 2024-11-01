import pandas as pd
import numpy as np
from scipy.stats import norm

def creatingPercentilesWing(merged_df):

    raw_columns = ['Stand. Tackle Success ', 'Line Break', 'Pass Completion ', 'Progr Regain ']

    def calculate_percentile(value):
        return norm.cdf(value) * 100

        # Function to calculate z-score for each element in a column
    def calculate_zscore(column, mean, std):
        return (column - mean) / std

    per90 = ['Goal', 'Dribble',
        'Stand. Tackle', 'Unsucc Stand. Tackle',
        'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter',
        'Att 1v1', 'Efforts on Goal',
        'Shot on Target', 'Pass into Oppo Box', 'Forward', 'Unsucc Forward', 'Line Break',
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
    passing = passing.loc[:, ['Forward Total', 'Forward Completion', 'Total', 'Pass Completion ']]


    dribbling = merged_df[['Dribble', 'Att 1v1', 'Loss of Poss']]
    dribbling.fillna(0, inplace=True)

    defending = merged_df[['Stand. Tackle', 'Unsucc Stand. Tackle', 'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter', 'Progr Regain ', 
                            'Stand. Tackle Success ']]
    defending['Stand. Tackle Total'] = defending['Stand. Tackle'] + defending['Unsucc Stand. Tackle']
    defending['Rec Total'] = defending['Progr Rec'] + defending['Unprogr Rec']
    defending['Inter Total'] = defending['Progr Inter'] + defending['Unprogr Inter']
    defending.fillna(0, inplace=True)
    defending = defending.loc[:, ['Stand. Tackle Total', 'Rec Total', 'Inter Total', 'Progr Regain ', 'Stand. Tackle Success ']]

    playmaking = merged_df[['Line Break', 'Pass into Oppo Box']]
    playmaking.fillna(0, inplace=True)

    shooting = merged_df[['Efforts on Goal', 'Shot on Target']]
    shooting.fillna(0, inplace=True)


    final_pizza = pd.DataFrame(columns=['Pass %', 'Line Breaks', 'Progr Regain %', 
                                        'Tackle %', 'Player Name', 'Team Name', 'Minutes'])
    
    player_name = merged_df.at[0, 'Player Full Name']
    team_name = merged_df.at[0, 'Team Name']
    
    wing_df = pd.read_csv("IDP_Plan/Thresholds/WingerSeasonThresholds.csv")

    mean_values = wing_df.iloc[0, [5, 6, 7, 8, 9]]
    std_values = wing_df.iloc[1, [5, 6, 7, 8, 9]]
    # Calculate the z-score for each data point
    z_scores_df = passing.transform(lambda col: calculate_zscore(col, mean_values[col.name], std_values[col.name]))
    passing_percentile = z_scores_df.applymap(calculate_percentile)
    will_passing = passing_percentile

    mean_values = wing_df.iloc[0, 14:17]
    std_values = wing_df.iloc[1, 14:17]
    # Calculate the z-score for each data point
    z_scores_df = dribbling.transform(lambda col: calculate_zscore(col, mean_values[col.name], std_values[col.name]))
    dribbling_percentile = z_scores_df.applymap(calculate_percentile)
    will_dribbling = dribbling_percentile


    mean_values = wing_df.iloc[0, 0:5]
    std_values = wing_df.iloc[1, 0:5]
    # Calculate the z-score for each data point
    z_scores_df = defending.transform(lambda col: calculate_zscore(col, mean_values[col.name], std_values[col.name]))
    defending_percentile = z_scores_df.applymap(calculate_percentile)
    will_defending = defending_percentile


    mean_values = wing_df.iloc[0, 10:14]
    std_values = wing_df.iloc[0, 10:14]
    # Calculate the z-score for each data point
    z_scores_df = playmaking.transform(lambda col: calculate_zscore(col, mean_values[col.name], std_values[col.name]))
    playmaking_percentile = z_scores_df.applymap(calculate_percentile)
    will_playmaking = playmaking_percentile
    
    mean_values = wing_df.iloc[0, 17:20]
    std_values = wing_df.iloc[0, 17:20]
    z_scores_df = shooting.transform(lambda col: calculate_zscore(col, mean_values[col.name], std_values[col.name]))
    shooting_percentile = z_scores_df.applymap(calculate_percentile)
    player_shooting = shooting_percentile

    minutes_total = merged_df.at[0, 'mins played']
    date = merged_df.at[0, 'Year']
    
    final_pizza.loc[0, 'Pass %'] = float(raw_df['Pass Completion '][0])
    final_pizza.loc[0, 'Progr Regain %'] = float(raw_df['Progr Regain '][0])
    final_pizza.loc[0, 'Tackle %'] = float(raw_df['Stand. Tackle Success '][0])
    final_pizza.loc[0, 'Line Breaks'] = float(raw_df['Line Break'][0])
    final_pizza.loc[0, 'Stand. Tackle Total Percentile'] = float(will_defending['Stand. Tackle Total'])
    final_pizza.loc[0, 'Rec Total Percentile'] = float(will_defending['Rec Total'])
    final_pizza.loc[0, 'Total Passes Percentile'] = float(will_passing['Total'])
    final_pizza.loc[0, 'Pass Completion Percentile'] = float(will_passing['Pass Completion '])
    final_pizza.loc[0, 'Pass into Oppo Box Percentile'] = float(will_playmaking['Pass into Oppo Box'])
    final_pizza.loc[0, 'Forward Completion Percentile'] = float(will_passing['Forward Completion'])
    final_pizza.loc[0, 'Dribble Percentile'] = float(will_dribbling['Dribble'])
    final_pizza.loc[0, 'Att 1v1 Percentile'] = float(will_dribbling['Att 1v1'])
    final_pizza.loc[0, 'Loss of Poss Percentile'] = float(100-will_dribbling['Loss of Poss'])
    final_pizza.loc[0, 'Efforts on Goal Percentile'] = float(player_shooting['Efforts on Goal'])
    final_pizza.loc[0, 'Shot on Target Percentile'] = float(player_shooting['Shot on Target'])
    final_pizza.loc[0, 'Player Name'] = player_name
    final_pizza.loc[0, 'Team Name'] = team_name
    final_pizza.loc[0, 'Minutes'] = minutes_total
    final_pizza.loc[0, 'Date'] = date

    final_pizza.drop_duplicates(subset=['Player Name'], inplace=True)

    return final_pizza