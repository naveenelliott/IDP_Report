import pandas as pd
import os
import glob
import streamlit as st
from PIL import Image, ImageOps
from GettingPSDLineupData import getting_PSD_min_data, getting_weeklyReport
import matplotlib.pyplot as plt
from GettingPercentOfMins import plottingMinsPlayed, plottingStarts
from GetPlayerGrade import gettingFinalGradeForEachTeam, getPrimaryPosition, getPlayerStatistics, getStandardizedValues, getRadarChart, getRadarChartAdvanced
from xGModel import xGModel
import plotly.graph_objs as go
from plottingTimeSeries import plottingStatistics
from scipy.stats import norm

player_name = st.session_state['selected_player']
team_name = st.session_state['selected_team']



directory_path = 'Player_Photos'
    
# Search for files that match the variable name
matching_files = glob.glob(os.path.join(directory_path, f"{player_name}.*"))

# Check if a matching file is found
if matching_files:
    image_file = matching_files[0]
    
    # Open the image
    player_pic = Image.open(image_file)
else:
    player_pic = Image.open('Player_Photos/other_person.jpg')

col1, col2 = st.columns(2)

folder_path = 'Height_Weight'      
# List all files in the folder
files = os.listdir(folder_path)

# Filter the list to include only CSV files
csv_files = [file for file in files if file.endswith('.csv')]

data_frames = []
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    data_frames.append(df)

height_weight = pd.concat(data_frames, ignore_index=True)


height_weight = height_weight.loc[height_weight['Athlete Name'] == player_name].reset_index(drop=True)

height = height_weight['Height (cm)'][0]
weight = height_weight['Weight (lbs)'][0]

mins_df = getting_PSD_min_data()
mins_df = mins_df.loc[mins_df['Team Name'] == team_name]

starts_df = mins_df.copy()



# Define a function to assign Max Minutes based on team_name
def assign_max_minutes(team_name):
    if 'U13' in team_name:
        return 70
    elif 'U14' in team_name or 'U15' in team_name:
        return 80
    elif 'U16' in team_name or 'U17' in team_name or 'U19' in team_name:
        return 90

# Step 1: Apply the function to the idp_report
mins_df['Max Minutes'] = mins_df['Team Name'].apply(assign_max_minutes)

available_minutes = mins_df.groupby(['Match Date', 'Opposition', 'Team Name'])['Max Minutes'].first().sum()


player_mins = mins_df[mins_df['Player Full Name'] == player_name]
player_mins = player_mins['mins played'].sum()


# Calculate the percentage of available minutes played
percentage_played = (player_mins / available_minutes) * 100

fig = plottingMinsPlayed(percentage_played=percentage_played, player_name=player_name)

first_start_df = starts_df[starts_df['Starts'] == 1]
available_starts = first_start_df.groupby(['Match Date', 'Opposition', 'Team Name'])['Starts'].first().sum()

player_starts = starts_df[starts_df['Player Full Name'] == player_name]
player_starts = player_starts.groupby(['Match Date', 'Opposition', 'Team Name'])['Starts'].first().sum()

percentage_started = (player_starts / available_starts) * 100

fig2 = plottingStarts(percentage_played=percentage_started, player_name=player_name)

with col1:
        inner_columns = st.columns(2)

        with inner_columns[0]:
            st.image(player_pic)
            st.markdown(
            """
            <div style='display: block; text-align: left;'>
                <span style='font-family: Arial; font-size: 10pt; color: black;'>Player Name: {gk_name}</span>
            </div>
            """.format(gk_name=player_name),
            unsafe_allow_html=True
        )
            st.markdown(
                """
                <div style='display: block; text-align: left;'>
                    <span style='font-family: Arial; font-size: 10pt; color: black;'>Height: {height} cm</span>
                </div>
                """.format(height=height),
                unsafe_allow_html=True
            )
            st.markdown(
            """
            <div style='display: block; text-align: left;'>
                <span style='font-family: Arial; font-size: 10pt; color: black;'>Weight: {weight} lbs</span>
            </div>
            """.format(weight=weight),
            unsafe_allow_html=True
        )
        with inner_columns[1]:
            st.pyplot(fig)
            st.pyplot(fig2)

weekly_report = getting_weeklyReport()
weekly_report = weekly_report.loc[weekly_report['Player Full Name'] == player_name]
weekly_report['mins played'] = weekly_report['mins played'].astype(float)
weekly_report = weekly_report.loc[weekly_report['mins played'].idxmax()].to_frame()
weekly_report = pd.DataFrame(weekly_report)

primary_position = getPrimaryPosition(player_name)
primary_position = primary_position['Position Tag'].values[0]

if primary_position == 'LW' or primary_position == 'RW':
    primary_position = 'Wing'
elif primary_position == 'LB' or primary_position == 'RB' or primary_position == 'RWB' or primary_position == 'LWB':
    primary_position = 'FB'
elif primary_position == 'LCB' or primary_position == 'RCB':
    primary_position = 'CB'

player_metrics = getPlayerStatistics(player_full_name=player_name, position=primary_position)

temp_player_metrics = player_metrics.drop(columns={'mins played'})
temp_player_metrics = getStandardizedValues(temp_player_metrics, team_name, primary_position)

temp_player_metrics['mins played'] = player_metrics['mins played']
player_metrics = temp_player_metrics

weekly_report['Primary Position'] = primary_position

folder_path = 'xG Input Files'

# Find all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# List to hold individual idp_reports
df_list = []

# Loop through the CSV files and read them into idp_reports
for file in csv_files:
    df = pd.read_csv(file)
    df_list.append(df)

# Concatenate all idp_reports into a single idp_report
fc_python = pd.concat(df_list, ignore_index=True)

# Making sure everything is aligned on one side
def flip_coordinates(x, y):
    # Flip x and y coordinates horizontally
    flipped_x = field_dim - x
    flipped_y = field_dim - y  # y remains unchanged in this transformation
    
    return flipped_x, flipped_y

field_dim = 100
# Iterating through coordinates and making them on one side
flipped_points = []
for index, row in fc_python.iterrows():
    if row['X'] < 50:
        flipped_x, flipped_y = flip_coordinates(row['X'], row['Y'])
        fc_python.at[index, 'X'] = flipped_x
        fc_python.at[index, 'Y'] = flipped_y

# Path to the folder containing CSV files
folder_path = 'Actions PSD'

# Find all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# List to hold individual idp_reports
df_list = []

# Loop through the CSV files and read them into idp_reports
for file in csv_files:
    df = pd.read_csv(file)
    df.columns = df.loc[4]
    df = df.loc[5:].reset_index(drop=True)
    df_list.append(df)

# Concatenate all idp_reports into a single idp_report
actions = pd.concat(df_list, ignore_index=True)
actions['Match Date'] = pd.to_datetime(actions['Match Date']).dt.strftime('%m/%d/%Y')
actions.loc[actions['Opposition'] == 'St Louis', 'Match Date'] = '12/09/2023'

# creating copies to work on
full_actions = actions.copy()

xg_positions = ['CM', 'Wing', 'ATT']

if primary_position in xg_positions:

    # these are the ideal columns
    cols = ['Player Full Name', 'Team', 'Match Date', 'Opposition', 'Action', 'Time', 'Video Link']
    xg_actions = actions[cols]

    # these are the shots we want
    wanted_actions = ['Att Shot Blockd', 'Blocked Shot', 'Goal', 'Goal Against', 'Header on Target', 
                    'Header off Target', 'Opp Effort on Goal', 'Save Held', 'Save Parried', 'Shot off Target', 
                    'Shot on Target']
    xg_actions = xg_actions.loc[xg_actions['Action'].isin(wanted_actions)].reset_index(drop=True)
    # renaming for the join
    xg_actions.rename(columns={'Team': 'Bolts Team'}, inplace=True)

    # this is handeling duplicated PlayerStatData shots 
    temp_df = pd.DataFrame(columns=xg_actions.columns)
    prime_actions = ['Opp Effort on Goal', 'Shot on Target']
    remove_indexes = []
    for index in range(len(xg_actions) - 1):
        if xg_actions.loc[index, 'Time'] == xg_actions.loc[index+1, 'Time']:
            temp_df = pd.concat([temp_df, xg_actions.loc[[index]], xg_actions.loc[[index + 1]]], ignore_index=False)
            bye1 = temp_df.loc[temp_df['Action'].isin(prime_actions)]
            # these are the indexes we want to remove
            remove_indexes.extend(bye1.index)
            
        temp_df = pd.DataFrame(columns=xg_actions.columns)     

    # this is a copy with the removed duplicated PSD shots
    actions_new = xg_actions.copy()
    actions_new = actions_new.drop(remove_indexes).reset_index(drop=True) 

    fc_python['Match Date'] = pd.to_datetime(fc_python['Match Date']).dt.strftime('%m/%d/%Y')

    # combining into xG idp_report we want
    combined_xg = pd.merge(fc_python, actions_new, on=['Bolts Team', 'Match Date', 'Time'], how='inner')

    # running the model on our idp_report
    xg = xGModel(combined_xg)

    # creating a copy for later
    xg_copy = xg.copy()

    our_wanted_actions = ['Att Shot Blockd',  'Goal', 'Header on Target', 
                    'Header off Target', 'Shot off Target', 'Shot on Target']
    xg_us = xg_copy.loc[xg_copy['Action'].isin(our_wanted_actions)]

    xg_us = xg_us.groupby(['Player Full Name'])['xG'].sum().reset_index()
    xg_us_copy = xg_us.copy()

    xg_us = xg_us.loc[xg_us['Player Full Name'] == player_name].reset_index()


    player_metrics['xG'] = xg_us.at[0, 'xG']


    player_metrics['xG per 90'] = (player_metrics['xG']/player_metrics['mins played']) * 90
    xg_per_90 = player_metrics.loc[0, 'xG per 90']


    team_series = pd.Series(team_name)
    age_group = team_series.str.extract(r'(U\d{2})')
    age_group = age_group.at[0,0]
    age_group_mapping = {
        'U13': 'U13-U14',
        'U14': 'U13-U14',
        'U15': 'U15-U16',
        'U16': 'U15-U16',
        'U17': 'U17-U19',
        'U19': 'U17-U19'
    }

    # Replace Age Group with the grouped values
    age_group = age_group_mapping.get(age_group, age_group)

    thresholds = pd.read_csv('xGPositionAgeGroupAvgs.csv')
    thresholds = thresholds.loc[thresholds['Age Group'] == age_group]
    thresholds = thresholds.loc[thresholds['Position Tag'] == primary_position].reset_index(drop=True)



    mean_values = thresholds.loc[0, 'mean']
    std_values = thresholds.loc[0, 'std']

    def calculate_percentile(value):
        return norm.cdf(value) * 100

    # Function to calculate z-score for each element in a column
    def calculate_zscore(column, mean, std):
        return (column - mean) / std
    
    z_scores = calculate_zscore(xg_per_90, mean_values, std_values)
    xg_percentile = calculate_percentile(z_scores)
    player_metrics['xG per 90'] = xg_percentile

    player_metrics.drop(columns={'xG', 'mins played'}, inplace=True)
else:
    player_metrics.drop(columns={'mins played'}, inplace=True)


metric_columns = player_metrics.columns

def read_all_csvs_from_folder(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)
    
    # Filter the list to include only CSV files
    csv_files = [file for file in files if file.endswith('.csv')]
    
    # Read each CSV file and store it in a list of idp_reports
    data_frames = []
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df.columns = df.iloc[3]
        df = df.iloc[4:]
        df = df.reset_index(drop=True)

        start_index = df.index[df["Period Name"] == "Round By Position Player"][0]

        # Find the index where "period name" is equal to "running by position player"
        end_index = df.index[df["Period Name"] == "Round By Team"][0]

        # Select the rows between the two indices
        selected_rows = df.iloc[start_index:end_index]

        # Reset the index (optional if you want a clean integer index)
        selected = selected_rows.reset_index(drop=True)

        remove_first = ['Period Name', 'Squad Number', 'Match Name', 'As At Date', 'Round Name']
        selected = selected.drop(columns=remove_first, errors='ignore')
        selected = selected.dropna(axis=1, how='all')
        player_df = selected.iloc[1:]
        player_df.reset_index(drop=True, inplace=True)
        player_df['Match Date'] = pd.to_datetime(player_df['Match Date']).dt.strftime('%m/%d/%Y')
        team = player_df.at[1, 'Team Name']
        opp = player_df.at[1, 'Opposition']
        match_date = player_df.at[1, 'Match Date']
        player_df['Match Identifier'] = player_df['Team Name'] + ' vs ' + player_df['Opposition'] + ' on ' + player_df['Match Date'].astype(str)
        unique_match_identifiers = player_df['Match Identifier'].drop_duplicates().reset_index(drop=True)
        st.session_state['match_identifiers'] = unique_match_identifiers
        if player_name in player_df['Player Full Name'].values:
            player_df = player_df.loc[player_df['Player Full Name'] == player_name]
            temp_grade_df = gettingFinalGradeForEachTeam(team, opp, match_date, player_df, actions, fc_python, full_actions, xg)
            temp_grade_df['Match Date'] = match_date
            temp_grade_df['Opposition'] = opp
            data_frames.append(temp_grade_df)

    combined_df = pd.concat(data_frames, ignore_index=True)

    return combined_df


temp_folder_path = 'WeeklyReport PSD'
idp_report = read_all_csvs_from_folder(temp_folder_path)

idp_report = idp_report.sort_values('Match Date').reset_index(drop=True)

# Create the plot
fig = go.Figure()

idp_report['More Opposition'] = 'vs ' + idp_report['Opposition']
idp_report['Match Date'] = pd.to_datetime(idp_report['Match Date']).dt.strftime('%m/%d/%Y')

statistic = 'Final Grade'

player_average = idp_report[statistic].mean()

# Add the trendline to the plot
fig.add_trace(go.Scatter(
    x=idp_report['Match Date'],
    y=idp_report[statistic],
    mode='lines',
    name='Trendline',
    line=dict(color='black', dash='dash'),
    showlegend=True  # Show the legend for the trendline
))

current_game_shown = False
# Line plot for the specified statistic over time
for index, row in idp_report.iterrows(): 
    fig.add_trace(go.Scatter(
        x=[row['Match Date']],
        y=[row[statistic]],
        mode='lines+markers',
        name='Previous Games',
        line=dict(color='black'),
        marker=dict(color='black', size=6),
        showlegend=not current_game_shown,  # Remove legend
        text=row['More Opposition'] + ' (' + str(round(row[statistic], 4)) + ' )',  # Set hover text to Opposition
        hoverinfo='text'  # Display only the text (Opposition) in the hover tooltip
    ))
    current_game_shown = True

fig.add_trace(go.Scatter(
    x=idp_report['Match Date'],
    y=[player_average] * len(idp_report),  # Create a horizontal line by repeating the average
    mode='lines',
    name=f"{player_name}'s Average",
    line=dict(color='lightblue', width=2),  # Light blue color for the line
    showlegend=True,
    text='Average: ' + str(round(player_average, 2)),
    hoverinfo='text' # Show legend for the average line
))

# Customize the layout
fig.update_layout(
    title=dict(
        text=f'{statistic} Over Time',
        x=0.5,  # Center the title
        xanchor='center',
        yanchor='top',
        font=dict(size=12)  # Smaller title font
    ),
    xaxis_title=dict(
        text='Match Date',
        font=dict(size=10)  # Smaller x-axis label font
    ),
    yaxis_title=dict(
        text=statistic,
        font=dict(size=10)  # Smaller y-axis label font
    ),
    xaxis=dict(
        showline=True, 
        showgrid=False, 
        showticklabels=True, 
        linecolor='gray',
        tickangle=45,  # Angle the x-axis ticks for better readability
        ticks='outside',  # Show ticks outside the plot
        tickcolor='black',
        tickfont=dict(
            size=9
        )
    ),
    yaxis=dict(
        showline=True, 
        showgrid=False, 
        showticklabels=True, 
        linecolor='gray',
        ticks='outside',
        tickcolor='black'
    ),
    font=dict(size=9)
)

st.plotly_chart(fig)


# Path to the folder containing CSV files
folder_path = 'PlayerData Files'

# Find all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# List to hold individual DataFrames
df_list = []

# Loop through the CSV files and read them into DataFrames
for file in csv_files:
    df = pd.read_csv(file)
    df_list.append(df)

# Concatenate all DataFrames into a single DataFrame
pd_df = pd.concat(df_list, ignore_index=True)
pd_df['start_time'] = pd.to_datetime(pd_df['start_time']).dt.strftime('%m/%d/%Y')
pd_df['Total Distance'] = pd_df['total_distance_m'] * 0.001
pd_df['Max Speed'] = pd_df['max_speed_kph'] * 0.621371
pd_df['High Intensity Distance'] = pd_df['total_high_intensity_distance_m']

def rearrange_team_name(team_name):
    # Define age groups and leagues
    age_groups = ['U15', 'U16', 'U17', 'U19', 'U13', 'U14']
    leagues = ['MLS Next', 'NAL Boston', 'NAL South Shore']
    
    # Find age group in the team name
    for age in age_groups:
        if age in team_name:
            # Find the league part
            league_part = next((league for league in leagues if league in team_name), '')
            if league_part == 'NAL Boston':
                league_part = 'NALB'
            
            # Extract the rest of the team name
            rest_of_name = team_name.replace(age, '').replace('NAL Boston', '').replace(league_part, '').strip()
            
            
            # Construct the new team name
            return f"{rest_of_name} {age} {league_part}"
    
    # Return the original team name if no age group is found
    return team_name

# Apply the function to the 'team_name' column
pd_df['bolts team'] = pd_df['bolts team'].apply(rearrange_team_name)

col1, col2 = st.columns(2)

pd_df['athlete_name'] = pd_df['athlete_name'].str.lower()
idp_report['Player Full Name'] = idp_report['Player Full Name'].str.lower()

merged_df = idp_report.merge(pd_df, left_on=['Player Full Name', 'Match Date'], right_on=['athlete_name', 'start_time'], how='left')
merged_df = merged_df[['Player Full Name', 'Opposition', 'Match Date', 'Total Distance', 'High Intensity Distance', 'Max Speed']]


fig1 = plottingStatistics(merged_df, 'Total Distance')

fig2 = plottingStatistics(merged_df, 'High Intensity Distance')

with col1:
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

all_available_players = st.session_state['all_players']

positions = []
player_names = []
for available_player_name in all_available_players:
    temp_primary_position = getPrimaryPosition(available_player_name)
    position_tag = temp_primary_position['Position Tag'].values[0]
    if position_tag == 'LW' or position_tag == 'RW':
        position_tag = 'Wing'
    elif position_tag == 'LB' or position_tag == 'RB' or position_tag == 'RWB' or position_tag == 'LWB':
        position_tag = 'FB'
    elif position_tag == 'LCB' or position_tag == 'RCB':
        position_tag = 'CB'
    positions.append(position_tag)
    temp_player_name = temp_primary_position['Player Full Name'].values[0]
    player_names.append(temp_player_name)

players_df = pd.DataFrame()
players_df['Player Full Name'] = player_names
players_df['Position Tag'] = positions

players_df = players_df[players_df['Position Tag'] == primary_position]
players_df = players_df[players_df['Player Full Name'] != player_name].reset_index(drop=True)


available_players = players_df['Player Full Name']
none_series = pd.Series(['None'])
available_players = pd.concat([none_series, available_players], ignore_index=True)


with col2:
    compare_player = st.selectbox('Choose a Comparison Player:', available_players, index=0)

    if compare_player == 'None':
        fig3 = getRadarChart(metric_names=metric_columns, metric_values=player_metrics)

    else:
        player_metrics_2 = getPlayerStatistics(player_full_name=compare_player, position=primary_position)

        temp_player_metrics = player_metrics_2.drop(columns={'mins played'})
        temp_player_metrics = getStandardizedValues(temp_player_metrics, team_name, primary_position)

        temp_player_metrics['mins played'] = player_metrics_2['mins played']
        player_metrics_2 = temp_player_metrics

        if primary_position in xg_positions:

            xg_us = xg_us_copy.loc[xg_us_copy['Player Full Name'] == compare_player].reset_index()


            player_metrics_2['xG'] = xg_us.at[0, 'xG']


            player_metrics_2['xG per 90'] = (player_metrics_2['xG']/player_metrics_2['mins played']) * 90
            xg_per_90 = player_metrics_2.loc[0, 'xG per 90']


            team_series = pd.Series(team_name)
            age_group = team_series.str.extract(r'(U\d{2})')
            age_group = age_group.at[0,0]
            age_group_mapping = {
                'U13': 'U13-U14',
                'U14': 'U13-U14',
                'U15': 'U15-U16',
                'U16': 'U15-U16',
                'U17': 'U17-U19',
                'U19': 'U17-U19'
            }

            # Replace Age Group with the grouped values
            age_group = age_group_mapping.get(age_group, age_group)

            thresholds = pd.read_csv('xGPositionAgeGroupAvgs.csv')
            thresholds = thresholds.loc[thresholds['Age Group'] == age_group]
            thresholds = thresholds.loc[thresholds['Position Tag'] == primary_position].reset_index(drop=True)



            mean_values = thresholds.loc[0, 'mean']
            std_values = thresholds.loc[0, 'std']
            
            z_scores = calculate_zscore(xg_per_90, mean_values, std_values)
            xg_percentile = calculate_percentile(z_scores)
            player_metrics_2['xG per 90'] = xg_percentile

            player_metrics_2.drop(columns={'xG', 'mins played'}, inplace=True)
        else:
            player_metrics_2.drop(columns={'mins played'}, inplace=True)

        fig3 = getRadarChartAdvanced(metric_names=metric_columns, metric_values_1=player_metrics, metric_values_2=player_metrics_2)
    st.pyplot(fig3)
