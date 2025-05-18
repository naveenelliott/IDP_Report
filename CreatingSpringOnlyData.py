import pandas as pd
import os
import glob

def read_all_csvs_from_folder(folder_path):

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
            remove_first = ['Period Name', 'Squad Number', 'Match Name', 'As At Date', 'Round Name']
            df = df.drop(columns=remove_first, errors='ignore')
            df = df.dropna(axis=1, how='all')
            df = df.iloc[1:]
            data_frames.append(df)
    
        # Optionally, combine all DataFrames into a single DataFrame
        combined_df = pd.concat(data_frames, ignore_index=True)
        combined_df = combined_df.loc[:, combined_df.columns.notna()]
        non_int = ['Player Full Name', 'Team Name', 'Position Tag']
        for col in combined_df.columns:
                if col not in non_int:
                    combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
        cols_we_need = ['Player Full Name', 'Team Name', 'Position Tag', 'mins played', 'Goal', 'Success', 'Unsuccess', 'Line Break', 'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter',
                        'Stand. Tackle', 'Unsucc Stand. Tackle', 'Tackle', 'Unsucc Tackle', 'Att 1v1', 'Loss of Poss', 
                        'Efforts on Goal', 'Shot on Target', 'Pass into Oppo Box', 'Efficiency ',
                        'Dribble', 'Forward', 'Unsucc Forward', 'Clear', 'Blocked Shot', 'Blocked Cross', 
                        'Foul Won', 'Def Aerial', 'Unsucc Def Aerial', 'Opp Effort on Goal',
                        'Save Held', 'Save Parried', 'Goal Against']
        
        combined_df = combined_df.loc[:,cols_we_need]
        
        return combined_df

file_path_fall = 'Last_Year'
fall_szn = read_all_csvs_from_folder(file_path_fall)
fall_szn['Position Tag'] = fall_szn['Position Tag'].str.replace('LW', 'Wing').str.replace('RW', 'Wing').str.replace('LB', 'FB').str.replace('RB', 'FB').str.replace('LCB', 'CB').str.replace('RCB', 'CB').str.replace('AM', 'CM')
fall_szn['Position Tag'] = fall_szn['Position Tag'].str.replace('WingB', 'FB').str.replace('LM', 'Wing').str.replace('RM', 'Wing')

# Concatenate all DataFrames into one
file_path_full_season = 'FullSeason'
total = read_all_csvs_from_folder(file_path_full_season)
total['Position Tag'] = total['Position Tag'].str.replace('LW', 'Wing').str.replace('RW', 'Wing').str.replace('LB', 'FB').str.replace('RB', 'FB').str.replace('LCB', 'CB').str.replace('RCB', 'CB').str.replace('AM', 'CM')
total['Position Tag'] = total['Position Tag'].str.replace('WingB', 'FB').str.replace('LM', 'Wing').str.replace('RM', 'Wing')

#total = total.loc[(total['Position Tag'] != 'GK') & (total['Position Tag'] != 'UNK')]

grouped = total.groupby(['Player Full Name', 'Position Tag'])['mins played'].sum().reset_index()

# Select the position with the most minutes played for each Player Full Name
primary_position = grouped.loc[grouped.groupby('Player Full Name')['mins played'].idxmax()]
primary_position.rename(columns={'Position Tag': 'Primary Position'}, inplace=True)
primary_position = primary_position[['Player Full Name', 'Primary Position']]

total = total.merge(primary_position, on='Player Full Name', how='left')
total = total.sort_values(by=['Player Full Name', 'mins played'], ascending=[True, False])

most_minutes = total.drop_duplicates(subset=['Player Full Name'], keep='first')

end = total.groupby(['Player Full Name'])[['mins played', 'Goal', 'Success', 'Unsuccess', 'Progr Rec', 'Unprogr Rec', 
                                                        'Progr Inter', 'Unprogr Inter', 'Stand. Tackle', 
                                                        'Unsucc Stand. Tackle', 'Line Break', 'Tackle', 'Unsucc Tackle', 
                                                        'Att 1v1', 'Loss of Poss', 'Efforts on Goal', 'Shot on Target', 
                                                        'Pass into Oppo Box', 'Dribble', 'Forward', 
                                                        'Unsucc Forward', 'Clear', 'Blocked Shot', 
                                                        'Blocked Cross', 'Foul Won', 
                                                        'Def Aerial', 'Unsucc Def Aerial', 'Opp Effort on Goal',
                                                        'Save Held', 'Save Parried', 'Goal Against']].sum().reset_index()

fall_end = fall_szn.groupby(['Player Full Name'])[['mins played', 'Goal', 'Success', 'Unsuccess', 'Progr Rec', 'Unprogr Rec', 
                                                        'Progr Inter', 'Unprogr Inter', 'Stand. Tackle', 
                                                        'Unsucc Stand. Tackle', 'Line Break', 'Tackle', 'Unsucc Tackle', 
                                                        'Att 1v1', 'Loss of Poss', 'Efforts on Goal', 'Shot on Target', 
                                                        'Pass into Oppo Box', 'Dribble', 'Forward', 
                                                        'Unsucc Forward', 'Clear', 'Blocked Shot', 
                                                        'Blocked Cross', 'Foul Won', 
                                                        'Def Aerial', 'Unsucc Def Aerial', 'Opp Effort on Goal',
                                                        'Save Held', 'Save Parried', 'Goal Against']].sum().reset_index()

# Step 1: Ensure 'Player Full Name' is the key for merging
merged = end.merge(fall_end, on='Player Full Name', how='left', suffixes=('', '_fall'))

# Step 2: Define all numeric columns to subtract
numeric_cols = ['mins played', 'Goal', 'Success', 'Unsuccess', 'Progr Rec', 'Unprogr Rec', 
                'Progr Inter', 'Unprogr Inter', 'Stand. Tackle', 'Unsucc Stand. Tackle', 
                'Line Break', 'Tackle', 'Unsucc Tackle', 'Att 1v1', 'Loss of Poss', 
                'Efforts on Goal', 'Shot on Target', 'Pass into Oppo Box', 'Dribble', 
                'Forward', 'Unsucc Forward', 'Clear', 'Blocked Shot', 'Blocked Cross', 
                'Foul Won', 'Def Aerial', 'Unsucc Def Aerial', 'Opp Effort on Goal',
                'Save Held', 'Save Parried', 'Goal Against']

for col in numeric_cols:
    merged[col] = merged[col].fillna(0)
    merged[f'{col}_fall'] = merged[f'{col}_fall'].fillna(0)

# Step 3: Subtract fall values from total values
for col in numeric_cols:
    merged[col] = merged[col] - merged[f'{col}_fall']

# Step 4: Drop the fall columns (optional)
merged = merged[['Player Full Name'] + numeric_cols]

final = merged.copy()


# WAIT UNTIL LATER
final['Pass Completion '] = (final['Success']/(final['Success']+final['Unsuccess']))*100
final['Progr Regain '] = ((final['Progr Rec']+final['Progr Inter'])/(final['Progr Rec']+final['Unprogr Rec']+final['Progr Inter']+final['Unprogr Inter']))*100
final['Stand. Tackle Success '] = (final['Stand. Tackle']/(final['Stand. Tackle']+final['Unsucc Stand. Tackle']))*100

final = final.merge(most_minutes[['Player Full Name', 'Team Name']], on='Player Full Name', how='left')

#end = end[['Player Full Name', 'Team Name', 'mins played', 'Pass Completion ', 'Progr Regain ', 'Stand. Tackle Success ', 'Line Break', 'Goal']]
final['Team Category'] = final['Team Name'].apply(lambda x: 'U19' if '19' in x else 'U17' if '17' in x else 'U13' if '13' in x else 'U14' if '14' in x else 'U15' if '15' in x else 'U16')

#final.to_csv('spring2025_data.csv', index=False)
