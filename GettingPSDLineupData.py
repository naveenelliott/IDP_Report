import pandas as pd
import os
import streamlit as st

def getting_available_played(teamName, playerName):
    
    if teamName == 'Boston Bolts U13 MLS Next':
        folder_path = 'Team_Thresholds/BoltsThirteenGames/'
        maxMins = 70
    elif teamName == 'Boston Bolts U14 MLS Next':
        folder_path = 'Team_Thresholds/BoltsFourteenGames/'
        maxMins = 80
    elif teamName == 'Boston Bolts U15 MLS Next':
        folder_path = 'Team_Thresholds/BoltsFifteenGames/'
        maxMins = 80
    elif teamName == 'Boston Bolts U16 MLS Next':
        folder_path = 'Team_Thresholds/BoltsSixteenGames/'
        maxMins = 90
    elif teamName == 'Boston Bolts U17 MLS Next':
        folder_path = 'Team_Thresholds/BoltsSeventeenGames/'
        maxMins = 90
    elif teamName == 'Boston Bolts U19 MLS Next':
        folder_path = 'Team_Thresholds/BoltsNineteenGames/'
        maxMins = 90
    
    
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
            start_index = df.index[df["Period Name"] == "Round By Player"][0]

            # Find the index where "period name" is equal to "running by position player"
            end_index = df.index[df["Period Name"] == "Round By Position Player"][0]

            df = df.iloc[start_index:end_index]

            # Reset the index (optional if you want a clean integer index)
            df = df.reset_index(drop=True)
            remove_first = ['Period Name', 'Squad Number', 'Match Name', 'As At Date', 'Round Name']
            df = df.drop(columns=remove_first, errors='ignore')
            df = df.dropna(axis=1, how='all')
            df = df.iloc[1:]

            temp_match_date = pd.to_datetime(df['Match Date'][1])

            date_wanted = pd.Timestamp('2024-08-01')
            
            if temp_match_date >= date_wanted:
                # selecting match date information, because that's what actions have
                details = df.loc[:, ['Player Full Name', 'Team Name', 'mins played', 'Match Date', 'Opposition', 'Starts', 'Goal', 'Assist']]
                details[['mins played', 'Starts', 'Goal', 'Assist']] = details[['mins played', 'Starts', 'Goal', 'Assist']].astype(float)
                details['Max Minutes'] = maxMins
                data_frames.append(details)
        
        # Optionally, combine all DataFrames into a single DataFrame
        combined_df = pd.concat(data_frames, ignore_index=True)
        
        return combined_df
    
    end = read_all_csvs_from_folder(folder_path)

    end['Match Date'] = pd.to_datetime(end['Match Date'])
    
    # Filter rows where 'Match Date' is after 08/01/2024
    end = end[end['Match Date'] > pd.Timestamp('2024-08-01')]
    
    
    end = end.loc[end['Player Full Name'] == playerName].reset_index(drop=True)
        
    end = end.drop_duplicates()

    return end

def getting_PSD_data():
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
            remove_first = ['Period Name', 'Squad Number', 'Match Name', 'As At Date', 'Round Name']
            df = df.drop(columns=remove_first, errors='ignore')
            df = df.dropna(axis=1, how='all')
            df = df.iloc[1:]
            # if we have starts included, then we extract starts, otherwise we don't and don't add the dataframe
            if 'Starts' in df.columns:
                # selecting match date information, because that's what actions have
                details = df.loc[:, ['Player Full Name', 'Team Name']]
                data_frames.append(details)
        
        # Optionally, combine all DataFrames into a single DataFrame
        combined_df = pd.concat(data_frames, ignore_index=True)
        
        return combined_df

    # Example usage
    # THIS COULD NEED CHANGED WITH 18 NEW TEAMS
    folder_path = 'WeeklyReport PSD/'  # Replace with your folder path
    end = read_all_csvs_from_folder(folder_path)
        
    end = end.drop_duplicates()



    return end

def getting_PSD_min_data():
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
            start_index = df.index[df["Period Name"] == "Round By Player"][0]

            # Find the index where "period name" is equal to "running by position player"
            end_index = df.index[df["Period Name"] == "Round By Position Player"][0]

            df = df.iloc[start_index:end_index]

            # Reset the index (optional if you want a clean integer index)
            df = df.reset_index(drop=True)
            remove_first = ['Period Name', 'Squad Number', 'Match Name', 'As At Date', 'Round Name']
            df = df.drop(columns=remove_first, errors='ignore')
            df = df.dropna(axis=1, how='all')
            df = df.iloc[1:]
            # selecting match date information, because that's what actions have
            details = df.loc[:, ['Player Full Name', 'Team Name', 'mins played', 'Match Date', 'Opposition', 'Starts', 'Goal', 'Assist']]
            details[['mins played', 'Starts', 'Goal', 'Assist']] = details[['mins played', 'Starts', 'Goal', 'Assist']].astype(float)
            data_frames.append(details)
        
        # Optionally, combine all DataFrames into a single DataFrame
        combined_df = pd.concat(data_frames, ignore_index=True)
        
        return combined_df

    # Example usage
    # THIS COULD NEED CHANGED WITH 18 NEW TEAMS
    folder_path = 'WeeklyReport PSD/'  # Replace with your folder path
    end = read_all_csvs_from_folder(folder_path)
        
    end = end.drop_duplicates()



    return end


def getting_weeklyReport():
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
            remove_first = ['Period Name', 'Squad Number', 'Match Name', 'As At Date', 'Round Name']
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



    return end

def getting_WeeklyReportRank():
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
            remove_first = ['Period Name', 'Squad Number', 'Match Name', 'As At Date', 'Round Name']
            df = df.drop(columns=remove_first, errors='ignore')
            df = df.dropna(axis=1, how='all')
            df = df.iloc[1:]
            data_frames.append(df)
        
        # Optionally, combine all DataFrames into a single DataFrame
        combined_df = pd.concat(data_frames, ignore_index=True)
        
        return combined_df

    # Example usage
    # THIS COULD NEED CHANGED WITH 18 NEW TEAMS
    folder_path = 'This_Year/'  # Replace with your folder path
    end = read_all_csvs_from_folder(folder_path)
        
    end = end.drop_duplicates()

    per90 = ['Goal', 'Dribble',
        'Stand. Tackle', 'Unsucc Stand. Tackle', 'Tackle',
        'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter', 'Att 1v1', 'Efforts on Goal',
        'Shot on Target', 'Pass into Oppo Box',
        'Forward', 'Unsucc Forward', 'Line Break',
        'Loss of Poss', 'Success', 'Unsuccess']
    
    float_columns = ['Goal', 'Dribble',
        'Stand. Tackle', 'Unsucc Stand. Tackle', 'Tackle',
        'Progr Rec', 'Unprogr Rec', 'Progr Inter', 'Unprogr Inter', 'Att 1v1', 'Efforts on Goal',
        'Shot on Target', 'Pass into Oppo Box',
        'Forward', 'Unsucc Forward', 'Line Break',
        'Loss of Poss', 'Success', 'Unsuccess', 'mins played', 'Pass Completion ', 'Stand. Tackle Success ', 'Progr Regain ']

    end[float_columns] = end[float_columns].astype(float)


    end['minutes per 90'] = end['mins played']/90

    for column in per90:
        end[column] = end[column] / end['minutes per 90']
        
    end = end.drop(columns=['minutes per 90'])
    end['Forward Total'] = end['Forward'] + end['Unsucc Forward']
    end['Forward Completion'] = (end['Forward'] / end['Forward Total']) * 100
    end['Total'] = end['Success'] + end['Unsuccess']
    end['Stand. Tackle Total'] = end['Stand. Tackle'] + end['Unsucc Stand. Tackle']
    end['Rec Total'] = end['Progr Rec'] + end['Unprogr Rec']
    end['Inter Total'] = end['Progr Inter'] + end['Unprogr Inter']

    metrics_to_rank = ['Forward Total', 'Forward Completion', 'Total', 'Pass Completion ', 'Dribble', 
                      'Att 1v1', 'Stand. Tackle Total', 'Rec Total', 'Inter Total', 'Progr Regain ',
                      'Stand. Tackle Success ', 'Line Break', 'Pass into Oppo Box', 'Efforts on Goal']  # Replace with actual metric column names
    weird_metrics_to_rank = ['Loss of Poss']


    # Rank each metric within each team and create separate rank columns
    for metric in metrics_to_rank:
        end[metric] = end.groupby("Team Name")[metric].rank(ascending=False)
    for metric in weird_metrics_to_rank:
        end[metric] = end.groupby("Team Name")[metric].rank(ascending=True)
    
    end = end[['Player Full Name', 'Team Name'] + metrics_to_rank + weird_metrics_to_rank]

    return end
