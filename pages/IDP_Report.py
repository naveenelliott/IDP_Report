import pandas as pd
import os
import glob
import streamlit as st
from PIL import Image, ImageOps
from GettingPSDLineupData import getting_PSD_min_data, getting_weeklyReport, getting_WeeklyReportRank
import matplotlib.pyplot as plt
from GettingPercentOfMins import plottingMinsPlayed, plottingStarts
from GetPlayerGrade import gettingFinalGradeForEachTeam, getPrimaryPosition, getPlayerStatistics, getStandardizedValues, getRadarChart, getRadarChartAdvanced, getPrimaryPositionAll
from xGModel import xGModel
import plotly.graph_objs as go
from plottingTimeSeries import plottingStatistics
from scipy.stats import norm
from SpringSTATSportsPDP import gettingPlayerDataPlot
from GettingScatterData import gettingPostSpringGames
from MidfielderDefender import midfielder_function, defender_function
from Attacker import attacker_function
from testCF_Spring import creatingPercentilesAtt, creatingRawAtt
from testCB_Spring import creatingPercentilesCB, creatingRawCB
from testCDM_Spring import creatingPercentilesDM, creatingRawDM 
from testCM_Spring import creatingPercentilesCM, creatingRawCM
from testFB_Spring import creatingPercentilesFB, creatingRawFB
from testWinger_Spring import creatingPercentilesWing, creatingRawWing
from PizzaPlotPDP_Spring import createPizzaChart
from streamlit_gsheets import GSheetsConnection

player_name = st.session_state['selected_player']
team_name = st.session_state['selected_team']

st.set_page_config(layout="wide")

# Add the logo
logo_path = 'BostonBoltsLogo.png'

# Align the logo to the top-right corner
header_container = st.container()
with header_container:
    col1, col2 = st.columns([9, 1])  # Adjust column widths to control logo placement
    with col1:
        st.write("")  # Placeholder for aligning
    with col2:
        st.image(logo_path, use_column_width=False, width=200)

wr_rank = getting_WeeklyReportRank()
wr_rank = wr_rank.loc[wr_rank['Team Name'] == team_name]
wr_rank = wr_rank.loc[wr_rank['Player Full Name'] == player_name].reset_index(drop=True)
del wr_rank['Player Full Name'], wr_rank['Team Name']
wr_rank = wr_rank.T
wr_rank.columns = ['Rank']

directory_path = 'Player_Photos'
    
# Search for files that match the variable name
matching_files = glob.glob(os.path.join(directory_path, f"{player_name}.*")) + \
                 glob.glob(os.path.join(directory_path, f"{player_name} .*"))

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

goals_assists = getting_PSD_min_data()
goals_assists = goals_assists.loc[(goals_assists['Team Name'] == team_name) & (goals_assists['Player Full Name'] == player_name)]
goals = goals_assists['Goal'].sum()
goals = int(goals)
assists = goals_assists['Assist'].sum()
assists = int(assists)


# Calculate the percentage of available minutes played
percentage_played = (player_mins / available_minutes) * 100

fig = plottingMinsPlayed(percentage_played=percentage_played, player_name=player_name)

first_start_df = starts_df[starts_df['Starts'] == 1]
available_starts = first_start_df.groupby(['Match Date', 'Opposition', 'Team Name'])['Starts'].first().sum()

player_starts = starts_df[starts_df['Player Full Name'] == player_name]
player_starts = player_starts.groupby(['Match Date', 'Opposition', 'Team Name'])['Starts'].first().sum()

percentage_started = (player_starts / available_starts) * 100

fig2 = plottingStarts(percentage_played=percentage_started, player_name=player_name)

conn = st.connection('gsheets', type=GSheetsConnection)
comp_level = conn.read(worksheet='IDP_Plan', ttl=0)
comp_level = comp_level.loc[comp_level['Player Name'] == player_name]
comp_level.reset_index(drop=True, inplace=True)
coach = comp_level.at[0, "Coach's Summary"]
spring_focus = comp_level.at[0, "Focus for Spring"]

primary_position = getPrimaryPosition(player_name)
primary_position = primary_position['Position Tag'].values[0]

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
                    <span style='font-family: Arial; font-size: 10pt; color: black;'>Team Name: {team_name}</span>
                </div>
                """.format(team_name=team_name),
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
            st.markdown(
                """
                <div style='display: block; text-align: left;'>
                    <span style='font-family: Arial; font-size: 10pt; color: black;'>Coach's Summary: {coach}</span>
                </div>
                """.format(coach=coach),
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <div style='display: block; text-align: left;'>
                    <span style='font-family: Arial; font-size: 10pt; color: black;'>Focus for Spring: {spring_focus}</span>
                </div>
                """.format(spring_focus=spring_focus),
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <div style='display: block; text-align: left;'>
                    <span style='font-family: Arial; font-size: 10pt; color: black;'>Goals: {goals}</span>
                </div>
                """.format(goals=goals),
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <div style='display: block; text-align: left;'>
                    <span style='font-family: Arial; font-size: 10pt; color: black;'>Assists: {assists}</span>
                </div>
                """.format(assists=assists),
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <div style='display: block; text-align: left;'>
                    <span style='font-family: Arial; font-size: 10pt; color: black;'>Primary Position: {primary_position}</span>
                </div>
                """.format(primary_position=primary_position),
                unsafe_allow_html=True
            )



weekly_report = getting_weeklyReport()
weekly_report = weekly_report.loc[weekly_report['Player Full Name'] == player_name]
weekly_report['mins played'] = weekly_report['mins played'].astype(float)
weekly_report = weekly_report.loc[weekly_report['mins played'].idxmax()].to_frame()
weekly_report = pd.DataFrame(weekly_report)

if primary_position == 'LW' or primary_position == 'RW':
    primary_position = 'Wing'
elif primary_position == 'LB' or primary_position == 'RB' or primary_position == 'RWB' or primary_position == 'LWB':
    primary_position = 'FB'
elif primary_position == 'LCB' or primary_position == 'RCB':
    primary_position = 'CB'
elif primary_position == 'AM':
    primary_position = 'CM'

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

if not xg_us.empty:
    player_metrics['xG'] = xg_us.at[0, 'xG']
else:
    player_metrics['xG'] = 0


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
if primary_position in xg_positions:
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

all_primary_position = getPrimaryPositionAll()

temp_all_primary_position = all_primary_position.copy()

file_path = 'Last_Year'
last_season = gettingPostSpringGames(file_path)
last_season['Year'] = '2023'
last_season.loc[last_season['Player Full Name'] == 'Kaio Morias', 'Player Full Name'] = 'Kaio Morais'
last_season = pd.merge(last_season, temp_all_primary_position[['Player Full Name', 'Position Tag']], on='Player Full Name', how='inner')

file_path = 'This_Year'
this_season = gettingPostSpringGames(file_path)
this_season['Year'] = '2024'
this_season = pd.merge(this_season, temp_all_primary_position[['Player Full Name', 'Position Tag']], on='Player Full Name', how='inner')

combined_seasons = pd.concat([this_season, last_season], ignore_index=True)

player_season = combined_seasons.loc[combined_seasons['Player Full Name'] == player_name]
player_season_raw = player_season.copy()
player_season_later = player_season.loc[player_season['Year'] == '2023'].reset_index()
player_season = player_season.loc[player_season['Year'] == '2024'].reset_index()
player_season_later_raw = player_season_raw.loc[player_season_raw['Year'] == '2023'].reset_index()
player_season_raw = player_season_raw.loc[player_season_raw['Year'] == '2024'].reset_index()

age_groups = player_season.at[0, 'Team Category']

if not player_season_later.empty:
    player_season_later.at[0, 'Team Category'] = age_groups

combined_seasons.rename(columns={'Pass Completion ': 'Pass %',
                                 'Player Full Name': 'Player Name', 
                                 'Stand. Tackle Success ': 'Tackle %', 
                                 'Progr Regain ': 'Progr Regain %'}, inplace=True)

our_fig = plt.figure()


this_season = pd.merge(this_season, xg_us_copy, on='Player Full Name', how='inner')
this_season['Goal'] = (this_season['Goal']/this_season['mins played']) * 90
this_season['xG Value'] = (this_season['xG']/this_season['mins played']) * 90
this_season.rename(columns={'Player Full Name': 'Player Name'}, inplace=True)

def apply_color_change(value, base_value, index):
    try:
        # Skip formatting for 'Player Name' and 'Year' rows
        if index in ['Player Name', 'Year']:
            return ''
        
        # Calculate the percent change from '2023' to '2024'
        percent_change = ((value - base_value) / base_value) * 100 if base_value != 0 else None
        
        # Apply conditional coloring based on percent change
        if percent_change is not None:
            if percent_change >= 5:
                if index == 'Loss of Poss':
                    return 'background-color: #ffcccc'
                else:
                    return 'background-color: #b3ffb3'
            elif percent_change <= -5:
                if index == 'Loss of Poss':
                    return 'background-color: #b3ffb3'
                else:
                    return 'background-color: #ffcccc'
    except:
        return ''  # No styling if value is not numeric or calculation fails

current_names = ['Forward Total', 'Pass Completion ', 'Total', 'Forward Completion', 'Stand. Tackle Total', 'Rec Total', 'Inter Total', 'Progr Regain ', 'Stand. Tackle Success ', 'Efforts on Goal', 'Pass into Oppo Box']

new_names = ['Forward Passes', 'Pass %', 'Total Passes', 'Forward Pass %', 'Total Tackles', 'Total Recoveries', 'Total Interceptions', 'Regain %', 'Tackle %', 'Shots', 'Passes into 18']

if primary_position == 'ATT':
    overall_player = creatingPercentilesAtt(player_season)
    passing, dribbling, defending, shooting = creatingRawAtt(player_season_raw)
    if not player_season_later.empty:
        ls_passing, ls_dribbling, ls_defending, ls_shooting = creatingRawAtt(player_season_later_raw)
        last_season_player = creatingPercentilesAtt(player_season_later)
        overall_player = pd.concat([overall_player, last_season_player], ignore_index=True)
        passing = pd.concat([passing, ls_passing])
        dribbling = pd.concat([dribbling, ls_dribbling])
        defending = pd.concat([defending, ls_defending])
        shooting = pd.concat([shooting, ls_shooting])
    passing = passing.T
    dribbling = dribbling.T
    defending = defending.T
    shooting = shooting.T
    inn_columns = st.columns(4)
    with inn_columns[0]:
        new_columns = list(passing.loc['Year'])
        passing = passing.drop(['Player Name', 'Year'])
        passing.columns = new_columns
        if passing.shape[1] >= 2:
            passing = pd.concat([passing, wr_rank], axis=1)
            passing = passing.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in passing.index}
            passing = passing.rename(index=rename_mapping)
            passing_styled = passing.style.apply(
                lambda col: [
                    apply_color_change(value, passing.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            passing = passing.apply(pd.to_numeric, errors='coerce')
            passing_styled = passing.style.format(precision=2)
            passing_styled = pd.concat([passing_styled, wr_rank], axis=1)
            passing_styled = passing_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in passing_styled.index}
            passing_styled = passing_styled.rename(index=rename_mapping)
        st.write(passing_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[1]:
        new_columns = list(dribbling.loc['Year'])
        dribbling = dribbling.drop(['Player Name', 'Year'])
        dribbling.columns = new_columns
        if dribbling.shape[1] >= 2:
            dribbling = pd.concat([dribbling, wr_rank], axis=1)
            dribbling = dribbling.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in dribbling.index}
            dribbling = dribbling.rename(index=rename_mapping)
            dribbling_styled = dribbling.style.apply(
                lambda col: [
                    apply_color_change(value, dribbling.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            dribbling = dribbling.apply(pd.to_numeric, errors='coerce')
            dribbling_styled = dribbling.style.format(precision=2)
            dribbling_styled = pd.concat([dribbling_styled, wr_rank], axis=1)
            dribbling_styled = dribbling_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in dribbling_styled.index}
            dribbling_styled = dribbling_styled.rename(index=rename_mapping)
        st.write(dribbling_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[2]:
        new_columns = list(defending.loc['Year'])
        defending = defending.drop(['Player Name', 'Year'])
        defending.columns = new_columns
        if defending.shape[1] >= 2:
            defending = pd.concat([defending, wr_rank], axis=1)
            defending = defending.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in defending.index}
            defending = defending.rename(index=rename_mapping)
            defending_styled = defending.style.apply(
                lambda col: [
                    apply_color_change(value, defending.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            defending = defending.apply(pd.to_numeric, errors='coerce')
            defending_styled = defending.style.format(precision=2)
            defending_styled = pd.concat([defending_styled, wr_rank], axis=1)
            defending_styled = defending_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in defending_styled.index}
            defending_styled = defending_styled.rename(index=rename_mapping)
        st.write(defending_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[3]:
        new_columns = list(shooting.loc['Year'])
        shooting = shooting.drop(['Player Name', 'Year'])
        shooting.columns = new_columns
        if shooting.shape[1] >= 2:
            shooting = pd.concat([shooting, wr_rank], axis=1)
            shooting = shooting.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in shooting.index}
            shooting = shooting.rename(index=rename_mapping)
            shooting_styled = shooting.style.apply(
                lambda col: [
                    apply_color_change(value, shooting.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            shooting = shooting.apply(pd.to_numeric, errors='coerce')
            shooting_styled = shooting.style.format(precision=2)
            shooting_styled = pd.concat([shooting_styled, wr_rank], axis=1)
            shooting_styled = shooting_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in shooting_styled.index}
            shooting_styled = shooting_styled.rename(index=rename_mapping)
        st.write(shooting_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    overall_player['Position'] = 'ATT'
elif primary_position == 'Wing':
    overall_player = creatingPercentilesWing(player_season)
    passing, dribbling, defending, playmaking, shooting = creatingRawWing(player_season_raw)
    if not player_season_later.empty:
        ls_passing, ls_dribbling, ls_defending, ls_playmaking, ls_shooting = creatingRawWing(player_season_later_raw)
        last_season_player = creatingPercentilesWing(player_season_later)
        overall_player = pd.concat([overall_player, last_season_player], ignore_index=True)
        passing = pd.concat([passing, ls_passing])
        dribbling = pd.concat([dribbling, ls_dribbling])
        defending = pd.concat([defending, ls_defending])
        playmaking = pd.concat([playmaking, ls_playmaking])
        shooting = pd.concat([shooting, ls_shooting])
    passing = passing.T
    dribbling = dribbling.T
    defending = defending.T
    playmaking = playmaking.T
    shooting = shooting.T
    inn_columns = st.columns(5)
    with inn_columns[0]:
        new_columns = list(passing.loc['Year'])
        passing = passing.drop(['Player Name', 'Year'])
        passing.columns = new_columns
        if passing.shape[1] >= 2:
            passing = pd.concat([passing, wr_rank], axis=1)
            passing = passing.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in passing.index}
            passing = passing.rename(index=rename_mapping)
            passing_styled = passing.style.apply(
                lambda col: [
                    apply_color_change(value, passing.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            passing = passing.apply(pd.to_numeric, errors='coerce')
            passing_styled = passing.style.format(precision=2)
            passing_styled = pd.concat([passing_styled, wr_rank], axis=1)
            passing_styled = passing_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in passing_styled.index}
            passing_styled = passing_styled.rename(index=rename_mapping)
        st.write(passing_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[1]:
        new_columns = list(dribbling.loc['Year'])
        dribbling = dribbling.drop(['Player Name', 'Year'])
        dribbling.columns = new_columns
        if dribbling.shape[1] >= 2:
            dribbling = pd.concat([dribbling, wr_rank], axis=1)
            dribbling = dribbling.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in dribbling.index}
            dribbling = dribbling.rename(index=rename_mapping)
            dribbling_styled = dribbling.style.apply(
                lambda col: [
                    apply_color_change(value, dribbling.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            dribbling = dribbling.apply(pd.to_numeric, errors='coerce')
            dribbling_styled = dribbling.style.format(precision=2)
            dribbling_styled = pd.concat([dribbling_styled, wr_rank], axis=1)
            dribbling_styled = dribbling_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in dribbling_styled.index}
            dribbling_styled = dribbling_styled.rename(index=rename_mapping)
        st.write(dribbling_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[2]:
        new_columns = list(defending.loc['Year'])
        defending = defending.drop(['Player Name', 'Year'])
        defending.columns = new_columns
        if defending.shape[1] >= 2:
            defending = pd.concat([defending, wr_rank], axis=1)
            defending = defending.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in defending.index}
            defending = defending.rename(index=rename_mapping)
            defending_styled = defending.style.apply(
                lambda col: [
                    apply_color_change(value, defending.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            defending = defending.apply(pd.to_numeric, errors='coerce')
            defending_styled = defending.style.format(precision=2)
            defending_styled = pd.concat([defending_styled, wr_rank], axis=1)
            defending_styled = defending_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in defending_styled.index}
            defending_styled = defending_styled.rename(index=rename_mapping)
        st.write(defending_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[3]:
        new_columns = list(playmaking.loc['Year'])
        playmaking = playmaking.drop(['Player Name', 'Year'])
        playmaking.columns = new_columns
        if playmaking.shape[1] >= 2:
            playmaking = pd.concat([playmaking, wr_rank], axis=1)
            playmaking = playmaking.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in playmaking.index}
            playmaking = playmaking.rename(index=rename_mapping)
            playmaking_styled = playmaking.style.apply(
                lambda col: [
                    apply_color_change(value, playmaking.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            playmaking = playmaking.apply(pd.to_numeric, errors='coerce')
            playmaking_styled = playmaking.style.format(precision=2)
            playmaking_styled = pd.concat([playmaking_styled, wr_rank], axis=1)
            playmaking_styled = playmaking_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in playmaking_styled.index}
            playmaking_styled = playmaking_styled.rename(index=rename_mapping)
        st.write(playmaking_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[4]:
        new_columns = list(shooting.loc['Year'])
        shooting = shooting.drop(['Player Name', 'Year'])
        shooting.columns = new_columns
        if shooting.shape[1] >= 2:
            shooting = pd.concat([shooting, wr_rank], axis=1)
            shooting = shooting.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in shooting.index}
            shooting = shooting.rename(index=rename_mapping)
            shooting_styled = shooting.style.apply(
                lambda col: [
                    apply_color_change(value, shooting.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            shooting = shooting.apply(pd.to_numeric, errors='coerce')
            shooting_styled = shooting.style.format(precision=2)
            shooting_styled = pd.concat([shooting_styled, wr_rank], axis=1)
            shooting_styled = shooting_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in shooting_styled.index}
            shooting_styled = shooting_styled.rename(index=rename_mapping)
        st.write(shooting_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    overall_player['Position'] = 'Wing'
elif primary_position == 'CB':
    overall_player = creatingPercentilesCB(player_season)
    passing, ball_prog, defending = creatingRawCB(player_season_raw)
    if not player_season_later.empty:
        ls_passing, ls_ball_prog, ls_defending = creatingRawCB(player_season_later_raw)
        last_season_player = creatingPercentilesCB(player_season_later)
        overall_player = pd.concat([overall_player, last_season_player], ignore_index=True)
        passing = pd.concat([passing, ls_passing])
        ball_prog = pd.concat([ball_prog, ls_ball_prog])
        defending = pd.concat([defending, ls_defending])
    passing = passing.T
    ball_prog = ball_prog.T
    defending = defending.T
    inn_columns = st.columns(3)
    with inn_columns[0]:
        new_columns = list(passing.loc['Year'])
        passing = passing.drop(['Player Name', 'Year'])
        passing.columns = new_columns
        if passing.shape[1] >= 2:
            passing = pd.concat([passing, wr_rank], axis=1)
            passing = passing.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in passing.index}
            passing = passing.rename(index=rename_mapping)
            passing_styled = passing.style.apply(
                lambda col: [
                    apply_color_change(value, passing.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            passing = passing.apply(pd.to_numeric, errors='coerce')
            passing_styled = passing.style.format(precision=2)
            passing_styled = pd.concat([passing_styled, wr_rank], axis=1)
            passing_styled = passing_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in passing.index}
            passing = passing.rename(index=rename_mapping)
        st.write(passing_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[1]:
        new_columns = list(ball_prog.loc['Year'])
        ball_prog = ball_prog.drop(['Player Name', 'Year'])
        ball_prog.columns = new_columns
        if ball_prog.shape[1] >= 2:
            ball_prog = pd.concat([ball_prog, wr_rank], axis=1)
            ball_prog = ball_prog.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in ball_prog.index}
            ball_prog = ball_prog.rename(index=rename_mapping)
            ball_prog_styled = ball_prog.style.apply(
                lambda col: [
                    apply_color_change(value, ball_prog.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            ball_prog = ball_prog.apply(pd.to_numeric, errors='coerce')
            ball_prog_styled = ball_prog.style.format(precision=2)
            ball_prog_styled = pd.concat([ball_prog_styled, wr_rank], axis=1)
            ball_prog_styled = ball_prog_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in ball_prog_styled.index}
            ball_prog_styled = ball_prog_styled.rename(index=rename_mapping)
        st.write(ball_prog_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[2]:
        new_columns = list(defending.loc['Year'])
        defending = defending.drop(['Player Name', 'Year'])
        defending.columns = new_columns
        if defending.shape[1] >= 2:
            defending = pd.concat([defending, wr_rank], axis=1)
            defending = defending.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in defending.index}
            defending = defending.rename(index=rename_mapping)
            defending_styled = defending.style.apply(
                lambda col: [
                    apply_color_change(value, defending.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            defending = defending.apply(pd.to_numeric, errors='coerce')
            defending_styled = defending.style.format(precision=2)
            defending_styled = pd.concat([defending_styled, wr_rank], axis=1)
            defending_styled = defending_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in defending_styled.index}
            defending_styled = defending_styled.rename(index=rename_mapping)
        st.write(defending_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    overall_player['Position'] = 'CB'
elif primary_position == 'DM':
    overall_player = creatingPercentilesDM(player_season)
    passing, dribbling, defending, playmaking = creatingRawDM(player_season_raw)
    if not player_season_later.empty:
        ls_passing, ls_dribbling, ls_defending, ls_playmaking = creatingRawDM(player_season_later_raw)
        last_season_player = creatingPercentilesDM(player_season_later)
        overall_player = pd.concat([overall_player, last_season_player], ignore_index=True)
        passing = pd.concat([passing, ls_passing])
        dribbling = pd.concat([dribbling, ls_dribbling])
        defending = pd.concat([defending, ls_defending])
        playmaking = pd.concat([playmaking, ls_playmaking])
    passing = passing.T
    dribbling = dribbling.T
    defending = defending.T
    playmaking = playmaking.T
    inn_columns = st.columns(4)
    with inn_columns[0]:
        new_columns = list(passing.loc['Year'])
        passing = passing.drop(['Player Name', 'Year'])
        passing.columns = new_columns
        if passing.shape[1] >= 2:
            passing = pd.concat([passing, wr_rank], axis=1)
            passing = passing.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in passing.index}
            passing = passing.rename(index=rename_mapping)
            passing_styled = passing.style.apply(
                lambda col: [
                    apply_color_change(value, passing.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            passing = passing.apply(pd.to_numeric, errors='coerce')
            passing_styled = passing.style.format(precision=2)
            passing_styled = pd.concat([passing_styled, wr_rank], axis=1)
            passing_styled = passing_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in passing_styled.index}
            passing_styled = passing_styled.rename(index=rename_mapping)
        st.write(passing_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[1]:
        new_columns = list(dribbling.loc['Year'])
        dribbling = dribbling.drop(['Player Name', 'Year'])
        dribbling.columns = new_columns
        if dribbling.shape[1] >= 2:
            dribbling = pd.concat([dribbling, wr_rank], axis=1)
            dribbling = dribbling.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in dribbling.index}
            dribbling = dribbling.rename(index=rename_mapping)
            dribbling_styled = dribbling.style.apply(
                lambda col: [
                    apply_color_change(value, dribbling.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            dribbling = dribbling.apply(pd.to_numeric, errors='coerce')
            dribbling_styled = dribbling.style.format(precision=2)
            dribbling_styled = pd.concat([dribbling_styled, wr_rank], axis=1)
            dribbling_styled = dribbling_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in dribbling_styled.index}
            dribbling_styled = dribbling_styled.rename(index=rename_mapping)
        st.write(dribbling_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[2]:
        new_columns = list(defending.loc['Year'])
        defending = defending.drop(['Player Name', 'Year'])
        defending.columns = new_columns
        if defending.shape[1] >= 2:
            defending = pd.concat([defending, wr_rank], axis=1)
            defending = defending.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in defending.index}
            defending = defending.rename(index=rename_mapping)
            defending_styled = defending.style.apply(
                lambda col: [
                    apply_color_change(value, defending.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            defending = defending.apply(pd.to_numeric, errors='coerce')
            defending_styled = defending.style.format(precision=2)
            defending_styled = pd.concat([defending_styled, wr_rank], axis=1)
            defending_styled = defending_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in defending_styled.index}
            defending_styled = defending_styled.rename(index=rename_mapping)
        st.write(defending_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[3]:
        new_columns = list(playmaking.loc['Year'])
        playmaking = playmaking.drop(['Player Name', 'Year'])
        playmaking.columns = new_columns
        if playmaking.shape[1] >= 2:
            playmaking = pd.concat([playmaking, wr_rank], axis=1)
            playmaking = playmaking.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in playmaking.index}
            playmaking = playmaking.rename(index=rename_mapping)
            playmaking_styled = playmaking.style.apply(
                lambda col: [
                    apply_color_change(value, playmaking.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            playmaking = playmaking.apply(pd.to_numeric, errors='coerce')
            playmaking_styled = playmaking.style.format(precision=2)
            playmaking_styled = pd.concat([playmaking_styled, wr_rank], axis=1)
            playmaking_styled = playmaking_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in playmaking_styled.index}
            playmaking_styled = playmaking_styled.rename(index=rename_mapping)
        st.write(playmaking_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    overall_player['Position'] = 'DM'
elif primary_position == 'CM':
    overall_player = creatingPercentilesCM(player_season)
    passing, dribbling, defending, playmaking = creatingRawCM(player_season_raw)
    if not player_season_later.empty:
        ls_passing, ls_dribbling, ls_defending, ls_playmaking = creatingRawCM(player_season_later_raw)
        last_season_player = creatingPercentilesCM(player_season_later)
        overall_player = pd.concat([overall_player, last_season_player], ignore_index=True)
        passing = pd.concat([passing, ls_passing], ignore_index=True)
        dribbling = pd.concat([dribbling, ls_dribbling])
        defending = pd.concat([defending, ls_defending])
        playmaking = pd.concat([playmaking, ls_playmaking])
    passing = passing.T
    dribbling = dribbling.T
    defending = defending.T
    playmaking = playmaking.T
    inn_columns = st.columns(4)
    with inn_columns[0]:
        new_columns = list(passing.loc['Year'])
        passing = passing.drop(['Player Name', 'Year'])
        passing.columns = new_columns
        if passing.shape[1] >= 2:
            passing = pd.concat([passing, wr_rank], axis=1)
            passing = passing.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in passing.index}
            passing = passing.rename(index=rename_mapping)
            passing_styled = passing.style.apply(
                lambda col: [
                    apply_color_change(value, passing.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else: 
            passing = passing.apply(pd.to_numeric, errors='coerce')
            passing_styled = passing.style.format(precision=2)
            passing_styled = pd.concat([passing_styled, wr_rank], axis=1)
            passing_styled = passing_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in passing_styled.index}
            passing_styled = passing_styled.rename(index=rename_mapping)
        st.write(passing_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[1]:
        new_columns = list(dribbling.loc['Year'])
        dribbling = dribbling.drop(['Player Name', 'Year'])
        dribbling.columns = new_columns
        if dribbling.shape[1] >= 2:
            dribbling = pd.concat([dribbling, wr_rank], axis=1)
            dribbling = dribbling.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in dribbling.index}
            dribbling = dribbling.rename(index=rename_mapping)
            dribbling_styled = dribbling.style.apply(
                lambda col: [
                    apply_color_change(value, dribbling.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else: 
            dribbling = dribbling.apply(pd.to_numeric, errors='coerce')
            dribbling_styled = dribbling.style.format(precision=2)
            dribbling_styled = pd.concat([dribbling_styled, wr_rank], axis=1)
            dribbling_styled = dribbling_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in dribbling_styled.index}
            dribbling_styled = dribbling_styled.rename(index=rename_mapping)
        st.write(dribbling_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[2]:
        new_columns = list(defending.loc['Year'])
        defending = defending.drop(['Player Name', 'Year'])
        defending.columns = new_columns
        if defending.shape[1] >= 2:
            defending = pd.concat([defending, wr_rank], axis=1)
            defending = defending.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in defending.index}
            defending = defending.rename(index=rename_mapping)
            defending_styled = defending.style.apply(
                lambda col: [
                    apply_color_change(value, defending.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            defending = defending.apply(pd.to_numeric, errors='coerce')
            defending_styled = defending.style.format(precision=2)
            defending_styled = pd.concat([defending_styled, wr_rank], axis=1)
            defending_styled = defending_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in defending_styled.index}
            defending_styled = defending_styled.rename(index=rename_mapping)
        st.write(defending_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    with inn_columns[3]:
        nnew_columns = list(playmaking.loc['Year'])
        playmaking = playmaking.drop(['Player Name', 'Year'])
        playmaking.columns = new_columns
        if playmaking.shape[1] >= 2:
            playmaking = pd.concat([playmaking, wr_rank], axis=1)
            playmaking = playmaking.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in playmaking.index}
            playmaking = playmaking.rename(index=rename_mapping)
            playmaking_styled = playmaking.style.apply(
                lambda col: [
                    apply_color_change(value, playmaking.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            playmaking = playmaking.apply(pd.to_numeric, errors='coerce')
            playmaking_styled = playmaking.style.format(precision=2)
            playmaking_styled = pd.concat([playmaking_styled, wr_rank], axis=1)
            playmaking_styled = playmaking_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in playmaking_styled.index}
            playmaking_styled = playmaking_styled.rename(index=rename_mapping)
        st.write(playmaking_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
    overall_player['Position'] = 'CM'
elif primary_position == 'FB':
    overall_player = creatingPercentilesFB(player_season)
    passing, attacking, defending = creatingRawFB(player_season_raw)
    if not player_season_later.empty:
        ls_passing, ls_attacking, ls_defending = creatingRawFB(player_season_later_raw)
        last_season_player = creatingPercentilesFB(player_season_later)
        overall_player = pd.concat([overall_player, last_season_player], ignore_index=True)
        passing = pd.concat([passing, ls_passing])
        attacking = pd.concat([attacking, ls_attacking])
        defending = pd.concat([defending, ls_defending])
    passing = passing.T
    attacking = attacking.T
    defending = defending.T
    inn_columns = st.columns(3)
    with inn_columns[0]:
        new_columns = list(passing.loc['Year'])
        passing = passing.drop(['Player Name', 'Year'])
        passing.columns = new_columns
        if passing.shape[1] >= 2:
            passing = pd.concat([passing, wr_rank], axis=1)
            passing = passing.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in passing.index}
            passing = passing.rename(index=rename_mapping)
            passing_styled = passing.style.apply(
                lambda col: [
                    apply_color_change(value, passing.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            passing = passing.apply(pd.to_numeric, errors='coerce')
            passing_styled = passing.style.format(precision=2)
            passing_styled = pd.concat([passing_styled, wr_rank], axis=1)
            passing_styled = passing_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in passing_styled.index}
            passing_styled = passing_styled.rename(index=rename_mapping)
        st.write(passing_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
        #st.dataframe(passing_styled, use_container_width=True)
    with inn_columns[1]:
        new_columns = list(attacking.loc['Year'])
        attacking = attacking.drop(['Player Name', 'Year'])
        attacking.columns = new_columns
        if attacking.shape[1] >= 2:
            attacking = pd.concat([attacking, wr_rank], axis=1)
            attacking = attacking.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in attacking.index}
            attacking = attacking.rename(index=rename_mapping)
            attacking_styled = attacking.style.apply(
                lambda col: [
                    apply_color_change(value, attacking.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            attacking = attacking.apply(pd.to_numeric, errors='coerce')
            attacking_styled = attacking.style.format(precision=2)
            attacking_styled = pd.concat([attacking_styled, wr_rank], axis=1)
            attacking_styled = attacking_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in attacking_styled.index}
            attacking_styled = attacking_styled.rename(index=rename_mapping)
        st.write(attacking_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
        #st.dataframe(attacking_styled, use_container_width=True)
    with inn_columns[2]:
        new_columns = list(defending.loc['Year'])
        defending = defending.drop(['Player Name', 'Year'])
        defending.columns = new_columns
        if defending.shape[1] >= 2:
            defending = pd.concat([defending, wr_rank], axis=1)
            defending = defending.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in defending.index}
            defending = defending.rename(index=rename_mapping)
            defending_styled = defending.style.apply(
                lambda col: [
                    apply_color_change(value, defending.at[idx, '2023'], idx) for idx, value in col.items()
                ],
                subset=['2024']
            ).format(precision=2)
        else:
            defending = defending.apply(pd.to_numeric, errors='coerce')
            defending_styled = defending.style.format(precision=2)
            defending_styled = pd.concat([defending_styled, wr_rank], axis=1)
            defending_styled = defending_styled.dropna(how='all', subset=['2024'])
            rename_mapping = {current: new for current, new in zip(current_names, new_names) if current in defending_styled.index}
            defending_styled = defending_styled.rename(index=rename_mapping)
        st.write(defending_styled.to_html(table_attributes='style="width:100%"'), unsafe_allow_html=True)
        #st.dataframe(defending_styled, use_container_width=True)
    overall_player['Position'] = 'FB'


if primary_position == 'ATT' or primary_position == 'Wing':
    our_fig = attacker_function(this_season, age_groups, player_name, primary_position)
elif primary_position == 'CM' or primary_position == 'DM':
    our_fig = midfielder_function(combined_seasons, age_groups, player_name, primary_position)
elif primary_position == 'FB' or primary_position == 'CB': 
    our_fig = defender_function(combined_seasons, age_groups, player_name, primary_position)
else:
    our_fig = plt.figure()

col1, col2, col3 = st.columns(3)

with col1:
    st.pyplot(our_fig)

# Path to the folder containing CSV files
folder_path = 'Detailed_Training_Sessions'

csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

dataframes = []
# Filter filenames that contain both player_name and opp_name
for f in csv_files:
    file_path = os.path.join(folder_path, f)
    
    # Read the CSV file into a DataFrame
    pd_df = pd.read_csv(file_path)
    
    pd_df['athlete_name'] = pd_df['athlete_name'].str.lower()
    
    # Append the DataFrame to the list
    dataframes.append(pd_df)
    
playerdata_df = pd.concat(dataframes, ignore_index=True)

# Convert start_time from string to datetime in UTC
playerdata_df['start_time'] = pd.to_datetime(playerdata_df['start_time'])

# Set the timezone to UTC, then convert to EST
playerdata_df['start_time'] = playerdata_df['start_time'].dt.tz_convert('America/New_York')

playerdata_df['Day of Week'] = pd.to_datetime(playerdata_df['start_time']).dt.day_name()

u19 = playerdata_df.loc[playerdata_df['bolts team'] == 'Boston Bolts MLS Next U19']

playerdata_df.drop(columns={'session_type'}, inplace=True)


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
playerdata_df['bolts team'] = playerdata_df['bolts team'].apply(rearrange_team_name)

# Getting rid of outliers
playerdata_df = playerdata_df[playerdata_df['total_distance_m'] > 2000]

distance_metrics = ['total_distance_m', 'total_high_intensity_distance_m']

playerdata_df['start_time'] = pd.to_datetime(playerdata_df['start_time']).dt.strftime('%m/%d/%Y')


days_of_week = ['Tuesday', 'Wednesday', 'Thursday']

playerdata_df = playerdata_df.loc[playerdata_df['Day of Week'].isin(days_of_week)]

averages = playerdata_df.groupby(['athlete_name', 'Day of Week']).agg(
    Avg_Total_Distance=('total_distance_m', 'mean'),
    Avg_High_Intensity_Distance=('total_high_intensity_distance_m', 'mean')
).reset_index()

final_averages_pd = averages.groupby(['athlete_name']).agg(
    Avg_Total_Distance=('Avg_Total_Distance', 'mean'), 
    Avg_High_Intensity_Distance=('Avg_High_Intensity_Distance', 'mean')
).reset_index()

final_averages_pd['athlete_name'] = final_averages_pd['athlete_name'].str.lower()


all_primary_position['Player Full Name'] = all_primary_position['Player Full Name'].str.lower()

final_averages_pd = pd.merge(final_averages_pd, all_primary_position, left_on='athlete_name', right_on='Player Full Name', how='inner')
final_averages_pd['Team Category'] = final_averages_pd['Team Name'].str.extract(r'(U\d+)')


player_name_lower = player_name.lower()

our_player_avg = final_averages_pd.loc[final_averages_pd['athlete_name'] == player_name_lower]

final_averages_pd = final_averages_pd.loc[final_averages_pd['athlete_name'] != player_name_lower]

fig_pd = gettingPlayerDataPlot(our_player_avg, final_averages_pd)

with col2:
    st.pyplot(fig_pd)



fig_pizza = createPizzaChart(overall_player)

with col3:
    st.pyplot(fig_pizza)

st.plotly_chart(fig)
