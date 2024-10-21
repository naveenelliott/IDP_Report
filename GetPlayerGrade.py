from FBGradeStreamlit import FBFunction
from CBGradeStreamlit import CBFunction
from CDMGradeStreamlit import CDMFunction
from CMGradeStreamlit import CMFunction
from WingerGradeStreamlit import WingerFunction
from StrikerGradeStreamlit import StrikerFunction
from GettingEventDataGrades import StrikerEventFunction, WingerEventFunction, CMEventFunction
import glob
import os
import pandas as pd
from xGModel import xGModel
import numpy as np
import streamlit as st
from mplsoccer import Radar
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.stats import norm

def gettingFinalGradeForEachTeam(selected_team, selected_opp, selected_date, player_data, actions, fc_python, full_actions, xg):

    player_data['mins played'] = player_data['mins played'].astype(float)
    player_data_copy = player_data.copy()
    grouped = player_data_copy.groupby(['Player Full Name', 'Position Tag'])['mins played'].sum().reset_index()
    
    # Find the position with the most minutes played for each player
    idx = grouped.groupby('Player Full Name')['mins played'].idxmax()
    prime_pos = grouped.loc[idx].reset_index(drop=True)
    prime_pos.rename(columns={'Position Tag': 'Primary Position'}, inplace=True)

    # getting the primary position
    player_data_copy = pd.merge(player_data_copy, prime_pos[['Player Full Name', 'Primary Position']], on='Player Full Name', how='inner')
    del player_data_copy['Position Tag']
    player_data_copy = player_data_copy.groupby(['Player Full Name', 'Opposition', 'Match Date', 'Team Name', 'Primary Position'])[['mins played']].sum()
    player_data_copy.reset_index(inplace=True)
    player_data_copy['Match Identifier'] = player_data_copy['Team Name'] + ' vs ' + player_data_copy['Opposition'] + ' on ' + player_data_copy['Match Date'].astype(str)
    match_identifiers = st.session_state['match_identifiers']
    player_data_copy = player_data_copy[player_data_copy['Match Identifier'].isin(match_identifiers)]

    full_actions = full_actions.loc[(full_actions['Team'] == selected_team) & (full_actions['Opposition'] == selected_opp) & (full_actions['Match Date'] == selected_date)].reset_index(drop=True)

    # Getting the chances created, is this something that PSD will consistently have in actions tab??
    chances_created = full_actions.loc[full_actions['Action'] == 'Chance Created']

    # converting everything to seconds
    def time_to_seconds(time_str):
            minutes, seconds = map(int, time_str.split(':'))
            return minutes + (seconds/60)
        
    # Apply the function to the 'Time' column
    chances_created['Time'] = chances_created['Time'].apply(time_to_seconds)

    # creating a copy for later
    if not xg.empty:
        xg_copy = xg.copy()


        xg = xg.loc[(xg['Bolts Team'] == selected_team) & (xg['Opposition'] == selected_opp) & (xg['Match Date'] == selected_date)]


        # getting Bolts info
        our_wanted_actions = ['Att Shot Blockd',  'Goal', 'Header on Target', 
                        'Header off Target', 'Shot off Target', 'Shot on Target']
        xg_us = xg_copy.loc[xg_copy['Action'].isin(our_wanted_actions)]

        # combining chances created rows and shots rows and sorting by time
        chances_created = pd.concat([chances_created, xg_us], ignore_index=True)
        chances_created = chances_created.sort_values('Time', ascending=True).reset_index(drop=True)

        # Initialize columns for pairing
        chances_created['xA'] = None

        # Keep track of the last "Chance Created" event
        last_chance_idx = None

        # this will check if there is an associated chances created with each shot
        for idx, row in chances_created.iterrows():
            if row['Action'] == 'Chance Created':
                last_chance_idx = idx
            elif row['Action'] in our_wanted_actions and last_chance_idx is not None:
                chances_created.at[last_chance_idx, 'xA'] = row['xG']
                last_chance_idx = None


        # final formatting of chances created
        chances_created = chances_created[['Player Full Name', 'Team', 'Opposition', 'Match Date', 'xG', 'xA']]
        # summing the xA and xG for each player
        chances_created = chances_created.groupby(['Player Full Name', 'Team', 'Opposition', 'Match Date'])[['xG', 'xA']].sum()
        chances_created.reset_index(inplace=True)


        player_data_copy.rename(columns={'Team Name': 'Team'}, inplace=True)
        chances_created = pd.merge(chances_created, player_data_copy[['Player Full Name', 'Team', 'Opposition', 'Match Date', 'mins played', 'Primary Position']], 
                                on=['Player Full Name', 'Team', 'Opposition', 'Match Date'], how='outer')

        chances_created['xG + xA'] = chances_created['xG'] + chances_created['xA']

        # converting this to p90
        chances_created['xG + xA'] = (chances_created['xG + xA']/chances_created['mins played']) * 90

        select_event_df = chances_created.loc[(chances_created['Team'] == selected_team) & (chances_created['Opposition'] == selected_opp) & (chances_created['Match Date'] == selected_date)]




    our_columns = ['Final Grade', 'Player Name', 'Position', 'Adjustments']
    final_grade_df = pd.DataFrame(columns=our_columns)

    # would ideally like to combine this into one dataframe with the event data
    # CAN WE CONCACATENATE THE EVENT DATA TO PLAYER_DATA
    # will be tough because the structure is limited to the time limits for each position

    for index, row in player_data.iterrows():
        if row['Position Tag'] == 'ATT': 
            temp_df = player_data.loc[[index]]
            end_att = StrikerFunction(temp_df)
            final_grade_df = pd.concat([final_grade_df, end_att], ignore_index=True)
        elif (row['Position Tag'] == 'RW') or (row['Position Tag'] == 'LW'):
            temp_df = player_data.loc[[index]]
            end_att = WingerFunction(temp_df)
            final_grade_df = pd.concat([final_grade_df, end_att], ignore_index=True)
        elif (row['Position Tag'] == 'CM') or (row['Position Tag'] == 'RM') or (row['Position Tag'] == 'LM') or (row['Position Tag'] == 'AM'):
            temp_df = player_data.loc[[index]]
            end_att = CMFunction(temp_df)
            final_grade_df = pd.concat([final_grade_df, end_att], ignore_index=True)
        elif (row['Position Tag'] == 'DM'):
            temp_df = player_data.loc[[index]]
            end_att = CDMFunction(temp_df)
            final_grade_df = pd.concat([final_grade_df, end_att], ignore_index=True)
        elif (row['Position Tag'] == 'RCB') or (row['Position Tag'] == 'LCB') or (row['Position Tag'] == 'CB'):
            temp_df = player_data.loc[[index]]
            end_att = CBFunction(temp_df)
            final_grade_df = pd.concat([final_grade_df, end_att], ignore_index=True)
        elif 'RB' in row['Position Tag'] or 'LB' in row['Position Tag'] or 'RWB' in row['Position Tag'] or 'LWB' in row['Position Tag'] or 'WingB' in row['Position Tag']:
            temp_df = player_data.loc[[index]]
            end_att = FBFunction(temp_df)
            final_grade_df = pd.concat([final_grade_df, end_att], ignore_index=True)

    temp_group = final_grade_df.groupby('Player Name')



    # adding the adjustments and getting the primary position
    temp_df = pd.DataFrame(columns=['Player Name', 'Position', 'Final Grade', 'Adjustments'])
    for player_name, group in temp_group:
        group.reset_index(drop=True, inplace=True)
        if (len(group) > 1):
            total_adj = group['Adjustments'].sum()
            max_minutes_row = group.loc[group['Minutes'].idxmax()]
            position = max_minutes_row['Position']
            if len(group) == 3:
                first_weight = group.loc[0, 'Minutes']/(group.loc[0, 'Minutes'] + group.loc[1, 'Minutes'] + group.loc[2, 'Minutes'])
                second_weight = group.loc[1, 'Minutes']/(group.loc[0, 'Minutes'] + group.loc[1, 'Minutes'] + group.loc[2, 'Minutes'])
                third_weight = group.loc[2, 'Minutes']/(group.loc[0, 'Minutes'] + group.loc[1, 'Minutes'] + group.loc[2, 'Minutes'])
                final_grade = (first_weight * group.loc[0, 'Final Grade']) + (second_weight * group.loc[1, 'Final Grade']) + (third_weight * group.loc[2, 'Final Grade'])
            elif len(group) == 2:
                first_weight = group.loc[0, 'Minutes']/(group.loc[0, 'Minutes'] + group.loc[1, 'Minutes'])
                second_weight = group.loc[1, 'Minutes']/(group.loc[0, 'Minutes'] + group.loc[1, 'Minutes'])
                final_grade = (first_weight * group.loc[0, 'Final Grade']) + (second_weight * group.loc[1, 'Final Grade'])
            update_row = {
                'Player Name': player_name,
                'Position': position,
                'Final Grade': final_grade,
                'Adjustments': total_adj
                }
            update_row = pd.DataFrame([update_row])
            temp_df = pd.concat([temp_df, update_row], ignore_index=True)
        else:
            update_row2 = group[['Player Name', 'Position', 'Final Grade', 'Adjustments']]
            temp_df = pd.concat([temp_df, update_row2], ignore_index=True)
        

    final_grade_df = temp_df.copy()

    for index, row in final_grade_df.iterrows():
        if row['Position'] == 'ATT':
            temp_event_df = chances_created.loc[(chances_created['Primary Position'] == 'ATT')]
            wanted = ['xG + xA', 'Team']
            temp_event_df = temp_event_df[wanted]
            select_temp_df = select_event_df.loc[select_event_df['Player Full Name'] == row['Player Name']]
            select_temp_df = select_temp_df[wanted]
            select_temp_df = StrikerEventFunction(temp_event_df, select_temp_df)
            final_grade_df.at[index, 'Final Grade'] = row['Final Grade'] + ((select_temp_df.at[0, 'Finishing'])*.2)
        elif (row['Position'] == 'RW') or (row['Position'] == 'LW'):
            temp_event_df = chances_created.loc[(chances_created['Primary Position'] == 'LW') | (chances_created['Primary Position'] == 'RW')]
            wanted = ['xG + xA', 'Team']
            temp_event_df = temp_event_df[wanted]
            select_temp_df = select_event_df.loc[select_event_df['Player Full Name'] == row['Player Name']]
            select_temp_df = select_temp_df[wanted]
            select_temp_df = WingerEventFunction(temp_event_df, select_temp_df)
            final_grade_df.at[index, 'Final Grade'] = row['Final Grade'] + ((select_temp_df.at[0, 'Finishing'])*.2)
        elif (row['Position'] == 'CM') or (row['Position'] == 'RM') or (row['Position'] == 'LM') or (row['Position'] == 'AM'):
            temp_event_df = chances_created.loc[(chances_created['Primary Position'] == 'RM') | (chances_created['Primary Position'] == 'LM')
                                            | (chances_created['Primary Position'] == 'AM') | (chances_created['Primary Position'] == 'CM')]
            wanted = ['xG + xA', 'Team']
            temp_event_df = temp_event_df[wanted]
            select_temp_df = select_event_df.loc[select_event_df['Player Full Name'] == row['Player Name']]
            select_temp_df = select_temp_df[wanted]
            select_temp_df = CMEventFunction(temp_event_df, select_temp_df)
            final_grade_df.at[index, 'Final Grade'] = row['Final Grade'] + ((select_temp_df.at[0, 'Playmaking'])*.2)



    final_grade_df['Final Grade'] = final_grade_df['Final Grade'] + final_grade_df['Adjustments']

    final_grade_df = final_grade_df[['Player Name', 'Position', 'Final Grade']]
    final_grade_df.rename(columns={'Player Name': 'Player Full Name', 'Position': 'Position Tag'}, inplace=True)
    final_grade_df['Final Grade'] = round(final_grade_df['Final Grade'], 1)

    final_grade_df.loc[final_grade_df['Player Full Name'] == 'Sy Perkins', 'Position Tag'] = 'GK'

    final_grade_df['Final Grade'] = np.clip(final_grade_df['Final Grade'], 5.00, 9.70)
    final_grade_df['Final Grade'] = final_grade_df['Final Grade'].astype(float)
    final_grade_df['Final Grade'] = final_grade_df['Final Grade'].round(1)
    return final_grade_df

def getPrimaryPosition(player_full_name):
    def read_all_csvs_from_folder(folder_path):
        # List all files in the folder
        files = os.listdir(folder_path)
        
        # Filter the list to include only CSV files
        csv_files = [file for file in files if file.endswith('.csv')]
        
        # Read each CSV file and store it in a list of DataFrames
        data_frames = []
        for file in csv_files:
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)
            # formatting the files
            df.columns = df.iloc[3]
            df = df.iloc[4:]
            df = df.reset_index(drop=True)
            # this is getting us the player data
            start_index = df.index[df["Period Name"] == "Running By Position Player"][0]

            # Find the index where "period name" is equal to "running by position player"
            end_index = df.index[df["Period Name"] == "Running By Team"][0]

            df = df.iloc[start_index:end_index]

            # Reset the index (optional if you want a clean integer index)
            df = df.reset_index(drop=True)
            remove_first = ['Period Name', 'Squad Number', 'Match Name', 'Round Name']
            df = df.drop(columns=remove_first, errors='ignore')
            df = df.dropna(axis=1, how='all')
            df = df.iloc[1:]
            data_frames.append(df)
            
        
        # Optionally, combine all DataFrames into a single DataFrame
        combined_df = pd.concat(data_frames, ignore_index=True)
        
        return combined_df

    # Example usage
    # THIS COULD NEED CHANGED WITH 18 NEW TEAMS
    folder_path = 'WeeklyReport PSD/'  # Replace with your folder path
    end = read_all_csvs_from_folder(folder_path)
        
    end = end.drop_duplicates()
    end['mins played'] = end['mins played'].astype(float)
    end['As At Date'] = pd.to_datetime(end['As At Date'])
    end = end.loc[end['Player Full Name'] == player_full_name]

    # Sort by Player Full Name and Match Date in descending order
    end = end.sort_values(by=['Player Full Name', 'As At Date'], ascending=[True, False])

    as_at_date = end['As At Date'].max()

    end = end.loc[end['As At Date'] == as_at_date]
    end_grouped = end.groupby(['Player Full Name', 'Position Tag'])['mins played'].sum().reset_index()
    end_grouped = end_grouped.sort_values(by=['Player Full Name', 'mins played'], ascending=[True, False])

    # Drop duplicates to keep the position with the most minutes for each player
    most_played_position = end_grouped.drop_duplicates(subset=['Player Full Name'], keep='first')
    
    


    return most_played_position


def getPlayerStatistics(player_full_name, position):
    def read_all_csvs_from_folder(folder_path):
        # List all files in the folder
        files = os.listdir(folder_path)
        
        # Filter the list to include only CSV files
        csv_files = [file for file in files if file.endswith('.csv')]
        
        # Read each CSV file and store it in a list of DataFrames
        data_frames = []
        for file in csv_files:
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)
            # formatting the files
            df.columns = df.iloc[3]
            df = df.iloc[4:]
            df = df.reset_index(drop=True)
            # this is getting us the player data
            start_index = df.index[df["Period Name"] == "Running By Player"][0]

            # Find the index where "period name" is equal to "running by position player"
            end_index = df.index[df["Period Name"] == "Running By Position Player"][0]

            df = df.iloc[start_index:end_index]

            # Reset the index (optional if you want a clean integer index)
            df = df.reset_index(drop=True)
            remove_first = ['Period Name', 'Squad Number', 'Match Name', 'Round Name']
            df = df.drop(columns=remove_first, errors='ignore')
            df = df.dropna(axis=1, how='all')
            df = df.iloc[1:]
            data_frames.append(df)
            
        
        # Optionally, combine all DataFrames into a single DataFrame
        combined_df = pd.concat(data_frames, ignore_index=True)
        
        return combined_df

    # Example usage
    # THIS COULD NEED CHANGED WITH 18 NEW TEAMS
    folder_path = 'WeeklyReport PSD/'  # Replace with your folder path
    end = read_all_csvs_from_folder(folder_path)
        
    end = end.drop_duplicates()
    end['mins played'] = end['mins played'].astype(float)
    end['As At Date'] = pd.to_datetime(end['As At Date'])
    end = end.loc[end['Player Full Name'] == player_full_name]

    # Sort by Player Full Name and Match Date in descending order
    end = end.sort_values(by=['Player Full Name', 'As At Date'], ascending=[True, False])

    as_at_date = end['As At Date'].max()

    end = end.loc[end['As At Date'] == as_at_date]

    number_columns = ['mins played', 'Yellow Card', 'Red Card', 'Goal', 'Assist', 'Dribble',
           'Goal Against', 'Stand. Tackle', 'Unsucc Stand. Tackle', 'Def Aerial', 'Unsucc Def Aerial',
           'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter', 'Att 1v1', 'Efforts on Goal', 'Att Aerial',
           'Shot on Target', 'Pass into Oppo Box', 'Tackle', 'Clear', 'Unsucc Tackle', 'Own Box Clear', 'Blocked Shot', 'Blocked Cross',
           'Forward', 'Unsucc Forward', 'Line Break', 'Header on Target', 'Cross', 'Unsucc Cross', 'Att Shot Blockd', 'Long', 'Unsucc Long',
           'Loss of Poss', 'Success', 'Unsuccess', 'Foul Won', 'Progr Regain ', 'Stand. Tackle Success ', 'Def Aerial Success ',
           'Pass Completion ', 'Progr Pass Attempt ', 'Progr Pass Completion ', 'Efficiency ', 'PK Missed', 'PK Scored', 'Foul Conceded']
    
    end = end[number_columns].astype(float)

    per90 = ['Yellow Card', 'Red Card', 'Goal', 'Assist', 'Dribble',
           'Stand. Tackle', 'Unsucc Stand. Tackle', 'Tackle', 'Def Aerial', 'Unsucc Def Aerial',
           'Own Box Clear', 'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter', 'Blocked Shot',
           'Blocked Cross', 'Att 1v1', 'Efforts on Goal', 'Clear', 'Unsucc Tackle',
           'Shot on Target', 'Att Shot Blockd',
           'Long', 'Unsucc Long', 'Forward', 'Unsucc Forward', 'Line Break', 
           'Loss of Poss', 'Success', 'Unsuccess', 'Foul Conceded', 'PK Missed', 'PK Scored']

    end['minutes per 90'] = end['mins played']/90

    for column in per90:
        if column not in ['Goal', 'Assist', 'Shot on Target', 'Yellow Card', 'Red Card', 'PK Missed', 'PK Scored']:
            end[column] = end[column] / end['minutes per 90']

    end = end.drop(columns=['minutes per 90'])
    end.reset_index(drop=True, inplace=True)
    end.fillna(0, inplace=True)

    if position == 'ATT':
        total_att_actions_columns = ['Goal', 'Assist', 'Att 1v1', 'Att Aerial', 'Efforts on Goal', 'Header on Target', 
                             'Shot on Target', 'Cross', 'Unsucc Cross', 'Pass into Oppo Box', 'Foul Won']
        end['Total Att Actions'] = end[total_att_actions_columns].sum(axis=1)

        total_def_actions_columns = ['Tackle', 'Clear', 'Progr Inter', 'Unprogr Inter', 'Progr Rec', 
                             'Unprogr Rec', 'Stand. Tackle', 'Unsucc Stand. Tackle', 
                             'Unsucc Tackle']
        end['Total Def Actions'] = end[total_def_actions_columns].sum(axis=1)
        end = end[['Total Def Actions', 'Efforts on Goal', 'Dribble', 'Total Att Actions', 'mins played']]
    elif position == 'Wing':
        total_def_actions_columns = ['Tackle', 'Clear', 'Progr Inter', 'Unprogr Inter', 'Progr Rec', 
                             'Unprogr Rec', 'Stand. Tackle', 'Unsucc Stand. Tackle', 
                             'Unsucc Tackle']
        end['Total Def Actions'] = end[total_def_actions_columns].sum(axis=1)

        total_att_actions_columns = ['Goal', 'Assist', 'Att 1v1', 'Att Aerial', 'Efforts on Goal', 'Header on Target', 
                                'Shot on Target', 'Cross', 'Unsucc Cross', 'Pass into Oppo Box', 'Foul Won']
        end['Total Att Actions'] = end[total_att_actions_columns].sum(axis=1)
        end = end[['Total Def Actions', 'Pass into Oppo Box', 'Dribble', 'Total Att Actions', 'mins played']]
    elif position == 'CM':
        success_total_actions_columns = ['Tackle', 'Progr Rec', 'Progr Inter', 'Blocked Shot', 'Stand. Tackle', 
                                 'Blocked Cross', 'Success', 'Efforts on Goal', 
                                 'Dribble', 'Foul Won']
        end['Total Successful Actions'] = end[success_total_actions_columns].sum(axis=1)

        end['Retention %'] = 100 - (((end['Loss of Poss'] + end['Unsuccess'])/(end['Success'] + end['Unsuccess'] + end['Dribble'] + end['Loss of Poss']))*100)

        total_def_actions_columns = ['Tackle', 'Clear', 'Progr Inter', 'Unprogr Inter', 'Progr Rec', 
                                'Unprogr Rec', 'Stand. Tackle', 'Unsucc Stand. Tackle', 
                                'Unsucc Tackle']
        end['Total Def Actions'] = end[total_def_actions_columns].sum(axis=1)

        end['Forward Passes'] = end['Forward'] + end['Unsucc Forward']
        end = end[['Total Successful Actions', 'Retention %', 'Total Def Actions', 'Forward Passes', 'Progr Pass Completion ', 'mins played']]
    elif position == 'DM':
        success_total_actions_columns = ['Tackle', 'Progr Rec', 'Progr Inter', 'Blocked Shot', 'Stand. Tackle', 
                                    'Blocked Cross', 'Success', 'Efforts on Goal', 
                                    'Dribble', 'Foul Won']
        end['Total Successful Actions'] = end[success_total_actions_columns].sum(axis=1)

        end['Retention %'] = 100 - (((end['Loss of Poss'] + end['Unsuccess'])/(end['Success'] + end['Unsuccess'] + end['Dribble'] + end['Loss of Poss']))*100)

        total_def_actions_columns = ['Tackle', 'Clear', 'Progr Inter', 'Unprogr Inter', 'Progr Rec', 
                                'Unprogr Rec', 'Stand. Tackle', 'Unsucc Stand. Tackle', 
                                'Unsucc Tackle']
        end['Total Def Actions'] = end[total_def_actions_columns].sum(axis=1)

        end['Forward Passes'] = end['Forward'] + end['Unsucc Forward']
        end = end[['Total Successful Actions', 'Total Def Actions', 'Retention %', 'Forward Passes', 'Progr Pass Completion ', 'mins played']]
    elif position == 'CB':
        total_def_actions_columns = ['Tackle', 'Clear', 'Progr Inter', 'Unprogr Inter', 'Progr Rec', 
                             'Unprogr Rec', 'Stand. Tackle', 'Unsucc Stand. Tackle', 
                             'Unsucc Tackle']
        end['Total Def Actions'] = end[total_def_actions_columns].sum(axis=1)

        end['Def Aerial %'] = (end['Def Aerial']/(end['Def Aerial'] + end['Unsucc Def Aerial'])) * 100

        end['Forward Passes'] = end['Forward'] + end['Unsucc Forward']
        end = end[['Total Def Actions', 'Def Aerial %', 'Forward Passes', 'Progr Pass Completion ', 'Progr Regain ', 'Pass Completion ', 'mins played']]
    elif position == 'FB': 
        total_def_actions_columns = ['Tackle', 'Clear', 'Progr Inter', 'Unprogr Inter', 'Progr Rec', 
                             'Unprogr Rec', 'Stand. Tackle', 'Unsucc Stand. Tackle', 
                             'Unsucc Tackle']
        end['Total Def Actions'] = end[total_def_actions_columns].sum(axis=1)

        end['Forward Passes'] = end['Forward'] + end['Unsucc Forward']

        end = end[['Total Def Actions', 'Progr Regain ', 'Forward Passes', 'Pass Completion ', 'Pass into Oppo Box', 'Progr Pass Completion ', 'mins played']]
    
    return end


def getStandardizedValues(metrics, team_name, position):
    
    def calculate_percentile(value):
        return norm.cdf(value) * 100

    # Function to calculate z-score for each element in a column
    def calculate_zscore(column, mean, std):
        return (column - mean) / std
    
    if position == 'ATT':
        if ('U13' in team_name) or ('U14' in team_name):
            cf_df = pd.read_csv("Thresholds/StrikerThresholds1314.csv")
        elif ('U15' in team_name) or ('U16' in team_name):
            cf_df = pd.read_csv("Thresholds/StrikerThresholds1516.csv")
        elif ('U17' in team_name) or ('U19' in team_name):
            cf_df = pd.read_csv("Thresholds/StrikerThresholds1719.csv")

        mean_values = cf_df.iloc[0, 0:].values
        std_values = cf_df.iloc[1, 0:].values
        # Calculate the z-score for each data point
        z_scores_df = metrics.apply(lambda col: calculate_zscore(col, mean_values, std_values), axis=1)
        percentiles = z_scores_df.map(calculate_percentile)
    elif position == 'Wing':
        if ('U13' in team_name) or ('U14' in team_name):
            wing_df = pd.read_csv("Thresholds/WingerThresholds1314.csv")
        elif ('U15' in team_name) or ('U16' in team_name):
            wing_df = pd.read_csv("Thresholds/WingerThresholds1516.csv")
        elif ('U17' in team_name) or ('U19' in team_name):
            wing_df = pd.read_csv("Thresholds/WingerThresholds1719.csv")

        mean_values = wing_df.iloc[0, 0:].values
        std_values = wing_df.iloc[1, 0:].values
        # Calculate the z-score for each data point
        z_scores_df = metrics.apply(lambda col: calculate_zscore(col, mean_values, std_values), axis=1)
        percentiles = z_scores_df.map(calculate_percentile)
    elif position == 'CM':
        if ('U13' in team_name) or ('U14' in team_name):
            cm_df = pd.read_csv("Thresholds/CenterMidfieldThresholds1314.csv")
        elif ('U15' in team_name) or ('U16' in team_name):
            cm_df = pd.read_csv("Thresholds/CenterMidfieldThresholds1516.csv")
        elif ('U17' in team_name) or ('U19' in team_name):
            cm_df = pd.read_csv("Thresholds/CenterMidfieldThresholds1719.csv")

        mean_values = cm_df.iloc[0, 0:].values
        std_values = cm_df.iloc[1, 0:].values
        # Calculate the z-score for each data point
        z_scores_df = metrics.apply(lambda col: calculate_zscore(col, mean_values, std_values), axis=1)
        percentiles = z_scores_df.map(calculate_percentile)
    elif position == 'DM':
        if ('U13' in team_name) or ('U14' in team_name):
            dm_df = pd.read_csv("Thresholds/DefensiveMidfieldThresholds1314.csv")
        elif ('U15' in team_name) or ('U16' in team_name):
            dm_df = pd.read_csv("Thresholds/DefensiveMidfieldThresholds1516.csv")
        elif ('U17' in team_name) or ('U19' in team_name):
            dm_df = pd.read_csv("Thresholds/DefensiveMidfieldThresholds1719.csv")

        mean_values = dm_df.iloc[0, 0:].values
        std_values = dm_df.iloc[1, 0:].values
        # Calculate the z-score for each data point
        z_scores_df = metrics.apply(lambda col: calculate_zscore(col, mean_values, std_values), axis=1)
        percentiles = z_scores_df.map(calculate_percentile)
    elif position == 'CB':
        if ('U13' in team_name) or ('U14' in team_name):
            cb_df = pd.read_csv("Thresholds/CenterBackThresholds1314.csv")
        elif ('U15' in team_name) or ('U16' in team_name):
            cb_df = pd.read_csv("Thresholds/CenterBackThresholds1516.csv")
        elif ('U17' in team_name) or ('U19' in team_name):
            cb_df = pd.read_csv("Thresholds/CenterBackThresholds1719.csv")

        mean_values = cb_df.iloc[0, 0:].values
        std_values = cb_df.iloc[1, 0:].values
        # Calculate the z-score for each data point
        z_scores_df = metrics.apply(lambda col: calculate_zscore(col, mean_values, std_values), axis=1)
        percentiles = z_scores_df.map(calculate_percentile)
    elif position == 'FB':
        if ('U13' in team_name) or ('U14' in team_name):
            fb_df = pd.read_csv("Thresholds/FullBackThresholds1314.csv")
        elif ('U15' in team_name) or ('U16' in team_name):
            fb_df = pd.read_csv("Thresholds/FullBackThresholds1516.csv")
        elif ('U17' in team_name) or ('U19' in team_name):
            fb_df = pd.read_csv("Thresholds/FullBackThresholds1719.csv")
        mean_values = fb_df.iloc[0, 0:].values
        std_values = fb_df.iloc[1, 0:].values
        # Calculate the z-score for each data point
        z_scores_df = metrics.apply(lambda col: calculate_zscore(col, mean_values, std_values), axis=1)
        percentiles = z_scores_df.map(calculate_percentile)

    return percentiles



def getRadarChart(metric_names, metric_values):
    params = metric_names


    font_path = 'Roboto-Bold.ttf'
    font_bold = FontProperties(fname=font_path)


    low = [0] * len(params)
    high = [100] * len(params)


    radar = Radar(params, low, high,
                # whether to round any of the labels to integers instead of decimal places
                round_int=[True]*len(params),
                num_rings=4,  # the number of concentric circles (excluding center circle)
                # if the ring_width is more than the center_circle_radius then
                # the center circle radius will be wider than the width of the concentric circles
                ring_width=1, center_circle_radius=1)

    fig, ax = radar.setup_axis()
    rings_inner = radar.draw_circles(ax=ax, facecolor='lightgray', edgecolor='black')

    radar1, vertices1 = radar.draw_radar_solid(metric_values.values.flatten(), ax=ax,
                                            kwargs={'facecolor': 'lightblue',
                                                    'alpha': 0.6,
                                                    'edgecolor': 'lightblue',
                                                    'lw': 2})

    ax.scatter(vertices1[:, 0], vertices1[:, 1],
            c='lightblue', edgecolors='lightblue', marker='o', s=100, zorder=2)

    range_labels = radar.draw_range_labels(ax=ax, fontsize=15)
    param_labels = radar.draw_param_labels(ax=ax, fontsize=17)

    fig.set_dpi(600)

    return fig

def getRadarChartAdvanced(metric_names, metric_values_1, metric_values_2):
    params = metric_names


    font_path = 'Roboto-Bold.ttf'
    font_bold = FontProperties(fname=font_path)


    low = [0] * len(params)
    high = [100] * len(params)


    radar = Radar(params, low, high,
                # whether to round any of the labels to integers instead of decimal places
                round_int=[True]*len(params),
                num_rings=4,  # the number of concentric circles (excluding center circle)
                # if the ring_width is more than the center_circle_radius then
                # the center circle radius will be wider than the width of the concentric circles
                ring_width=1, center_circle_radius=1)

    fig, ax = radar.setup_axis()
    rings_inner = radar.draw_circles(ax=ax, facecolor='lightgray', edgecolor='black')

    radar1, vertices1 = radar.draw_radar_solid(metric_values_2.values.flatten(), ax=ax,
                                            kwargs={'facecolor': 'black',
                                                    'alpha': 0.6,
                                                    'edgecolor': 'black',
                                                    'lw': 2})

    ax.scatter(vertices1[:, 0], vertices1[:, 1],
            c='black', edgecolors='black', marker='o', s=100, zorder=2)

    radar1, vertices2 = radar.draw_radar_solid(metric_values_1.values.flatten(), ax=ax,
                                            kwargs={'facecolor': 'lightblue',
                                                    'alpha': 0.6,
                                                    'edgecolor': 'lightblue',
                                                    'lw': 2})

    ax.scatter(vertices2[:, 0], vertices2[:, 1],
            c='lightblue', edgecolors='lightblue', marker='o', s=100, zorder=2)

    range_labels = radar.draw_range_labels(ax=ax, fontsize=15)
    param_labels = radar.draw_param_labels(ax=ax, fontsize=17)

    fig.set_dpi(600)

    return fig
