import pandas as pd
import os
import streamlit as st

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
            details = df.loc[:, ['Player Full Name', 'Team Name', 'mins played', 'Match Date', 'Opposition', 'Starts']]
            details[['mins played', 'Starts']] = details[['mins played', 'Starts']].astype(float)
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
    folder_path = 'IDP_Plan/WeeklyReport PSD/'  # Replace with your folder path
    end = read_all_csvs_from_folder(folder_path)
        
    end = end.drop_duplicates()



    return end