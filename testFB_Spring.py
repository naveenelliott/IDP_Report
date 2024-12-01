import pandas as pd
import numpy as np
from scipy.stats import norm

def creatingPercentilesFB(merged_df):

    raw_columns = ['Stand. Tackle Success ', 'Line Break', 'Pass Completion ', 'Progr Regain ']

    def calculate_percentile(value):
        return norm.cdf(value) * 100

        # Function to calculate z-score for each element in a column
    def calculate_zscore(column, mean, std):
        return (column - mean) / std

    per90 = ['Goal', 'Dribble',
        'Stand. Tackle', 'Unsucc Stand. Tackle', 'Tackle',
        'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter', 'Att 1v1', 'Efforts on Goal',
        'Shot on Target', 'Forward', 'Unsucc Forward', 'Line Break', 'Pass into Oppo Box',
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

    defending = merged_df[['Stand. Tackle', 'Unsucc Stand. Tackle', 'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter', 'Progr Regain ', 
                            'Stand. Tackle Success ']]
    defending['Stand. Tackle Total'] = defending['Stand. Tackle'] + defending['Unsucc Stand. Tackle']
    defending['Rec Total'] = defending['Progr Rec'] + defending['Unprogr Rec']
    defending['Inter Total'] = defending['Progr Inter'] + defending['Unprogr Inter']
    defending.fillna(0, inplace=True)
    defending = defending.loc[:, ['Stand. Tackle Total', 'Rec Total', 'Inter Total', 'Stand. Tackle Success ', 'Progr Regain ']]

    attacking = merged_df[['Line Break', 'Pass into Oppo Box', 'Dribble', 'Att 1v1',
                            'Loss of Poss']]
    attacking.fillna(0, inplace=True)


    final_pizza = pd.DataFrame(columns=['Pass %', 'Line Breaks', 'Progr Regain %', 
                                        'Tackle %', 'Player Name', 'Team Name', 'Minutes'])
    player_name = merged_df.at[0, 'Player Full Name']
    team_name = merged_df.at[0, 'Team Name']
    # DENIS
    age_group = merged_df.at[0, 'Team Category']

    u13_u14 = ['U13', 'U14']
    u15_u16 = ['U15', 'U16']
    u17_u19 = ['U17', 'U19']

    if age_group in u13_u14:
        fb_df = pd.read_csv("UpdateThresholds_IDP/FullBackThresholds1314.csv")
    if age_group in u15_u16:
        fb_df = pd.read_csv("UpdateThresholds_IDP/FullBackThresholds1516.csv")
    if age_group in u17_u19:
        fb_df = pd.read_csv("UpdateThresholds_IDP/FullBackThresholds1719.csv")
    
    mean_values = fb_df.iloc[0, [5,6,7,8,9,11,15]]
    std_values = fb_df.iloc[1, [5,6,7,8,9,11,15]]
    # Calculate the z-score for each data point
    z_scores_df = passing.transform(lambda col: calculate_zscore(col, mean_values[col.name], std_values[col.name]))
    passing_percentile = z_scores_df.applymap(calculate_percentile)
    player_passing = passing_percentile

    mean_values = fb_df.iloc[0, [0,1,2,3,4]]
    std_values = fb_df.iloc[1, [0,1,2,3,4]]
    # Calculate the z-score for each data point
    z_scores_df = defending.transform(lambda col: calculate_zscore(col, mean_values[col.name], std_values[col.name]))
    defending_percentile = z_scores_df.applymap(calculate_percentile)
    player_defending = defending_percentile

    mean_values = fb_df.iloc[0, [10, 12, 13, 14, 16]]
    std_values = fb_df.iloc[1, [10, 12, 13, 14, 16]]
    # Calculate the z-score for each data point
    z_scores_df = attacking.transform(lambda col: calculate_zscore(col, mean_values[col.name], std_values[col.name]))
    attacking_percentile = z_scores_df.applymap(calculate_percentile)
    player_attacking = attacking_percentile
    
    minutes_total = merged_df.at[0, 'mins played']
    date = merged_df.at[0, 'Year']
    
    final_pizza.loc[0, 'Pass %'] = float(raw_df['Pass Completion '][0])
    final_pizza.loc[0, 'Progr Regain %'] = float(raw_df['Progr Regain '][0])
    final_pizza.loc[0, 'Tackle %'] = float(raw_df['Stand. Tackle Success '][0])
    final_pizza.loc[0, 'Line Breaks'] = float(raw_df['Line Break'][0])
    final_pizza.loc[0, 'Stand. Tackle Total Percentile'] = float(player_defending['Stand. Tackle Total'])
    final_pizza.loc[0, 'Rec Total Percentile'] = float(player_defending['Rec Total'])
    final_pizza.loc[0, 'Progr Regain Percentile'] = float(player_defending['Progr Regain '])
    final_pizza.loc[0, 'Stand. Tackle Success Percentile'] = float(player_defending['Stand. Tackle Success '])
    final_pizza.loc[0, 'Forward Total Percentile'] = float(player_passing['Forward Total'])
    final_pizza.loc[0, 'Total Passes Percentile'] = float(player_passing['Total'])
    final_pizza.loc[0, 'Pass Completion Percentile'] = float(player_passing['Pass Completion '])
    final_pizza.loc[0, 'Forward Completion Percentile'] = float(player_passing['Forward Completion'])
    final_pizza.loc[0, 'Dribble Percentile'] = float(player_attacking['Dribble'])
    final_pizza.loc[0, 'Line Break Percentile'] = float(player_attacking['Line Break'])
    final_pizza.loc[0, 'Pass into Oppo Box Percentile'] = float(player_attacking['Pass into Oppo Box'])
    final_pizza.loc[0, 'Loss of Poss Percentile'] = float(100-player_attacking['Loss of Poss'])
    final_pizza.loc[0, 'Player Name'] = player_name
    final_pizza.loc[0, 'Team Name'] = team_name
    final_pizza.loc[0, 'Minutes'] = minutes_total
    final_pizza.loc[0, 'Date'] = date

    final_pizza.drop_duplicates(subset=['Player Name'], inplace=True)

    return final_pizza

def creatingRawFB(merged_df):
    
    raw_columns = ['Stand. Tackle Success ', 'Line Break', 'Pass Completion ', 'Progr Regain ']

    def calculate_percentile(value):
        return norm.cdf(value) * 100

    def calculate_zscore(column, mean, std):
        return (column - mean) / std

    per90 = ['Goal', 'Dribble', 'Stand. Tackle', 'Unsucc Stand. Tackle', 'Tackle',
             'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter', 'Att 1v1', 'Efforts on Goal',
             'Shot on Target', 'Forward', 'Unsucc Forward', 'Line Break', 'Pass into Oppo Box',
             'Loss of Poss', 'Success', 'Unsuccess']

    age_group = merged_df.at[0, 'Team Category']

    per_70 = ['U13']
    per_80 = ['U14', 'U15']

    if age_group in per_70:
        minutes_divide = 70
    elif age_group in per_80:
        minutes_divide = 80
    else:
        minutes_divide = 90

    merged_df['minutes per 90'] = merged_df['mins played'] / minutes_divide

    for column in per90:
        merged_df[column] = merged_df[column] / merged_df['minutes per 90']
        
    merged_df = merged_df.drop(columns=['minutes per 90'])
    merged_df.fillna(0, inplace=True)
    merged_df = merged_df.drop_duplicates()
    raw_df = merged_df[raw_columns]

    # Rename 'Player Full Name' to 'Player Name'
    merged_df.rename(columns={'Player Full Name': 'Player Name'}, inplace=True)

    # Passing DataFrame
    passing = merged_df[['Player Name', 'Year', 'Forward', 'Unsucc Forward', 'Success', 'Unsuccess', 'Pass Completion ']]
    passing['Forward Total'] = passing['Forward'] + passing['Unsucc Forward']
    passing['Forward Completion'] = (passing['Forward'] / passing['Forward Total']) * 100
    passing['Total'] = passing['Success'] + passing['Unsuccess']
    passing.fillna(0, inplace=True)
    passing = passing[['Player Name', 'Year', 'Forward Total', 'Forward Completion', 'Total', 'Pass Completion ']]

    # Defending DataFrame
    defending = merged_df[['Player Name', 'Year', 'Stand. Tackle', 'Unsucc Stand. Tackle', 'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter', 'Progr Regain ', 'Stand. Tackle Success ']]
    defending['Stand. Tackle Total'] = defending['Stand. Tackle'] + defending['Unsucc Stand. Tackle']
    defending['Rec Total'] = defending['Progr Rec'] + defending['Unprogr Rec']
    defending['Inter Total'] = defending['Progr Inter'] + defending['Unprogr Inter']
    defending.fillna(0, inplace=True)
    defending = defending[['Player Name', 'Year', 'Stand. Tackle Total', 'Rec Total', 'Inter Total', 'Stand. Tackle Success ', 'Progr Regain ']]

    # Attacking DataFrame
    attacking = merged_df[['Player Name', 'Year', 'Line Break', 'Pass into Oppo Box', 'Dribble', 'Att 1v1', 'Loss of Poss']]
    attacking.fillna(0, inplace=True)

    return passing, attacking, defending
