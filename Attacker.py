import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import streamlit as st

def attacker_function(dataframe, age_group, pname, position):

    def distance_to_line(x, y):
        # Calculate the slope of the line x=y
        slope = 1
        # Calculate the y-intercept of the line x=y
        intercept = 0
        # Calculate the perpendicular distance from the point to the line
        distance = (slope * x - y + intercept) / (slope ** 2 + 1) ** 0.5
        return distance

    positions = []
    positions.append(position)


    if position == 'ATT':
        positions.append('Wing')
    elif position == 'Wing':
        positions.append('ATT')
    elif position == 'CM':
        positions.append('DM')
    elif position == 'DM':
        positions.append('CM')
    elif position == 'CB':
        positions.append('FB')
    elif position == 'FB':
        positions.append('CB')

    dataframe = dataframe.loc[dataframe['Position Tag'].isin(positions)]
    
    if age_group == 'U13':
        dual_age_band = 'U14'
        other = ['U15', 'U16', 'U17', 'U19']
    elif age_group == 'U14':
        dual_age_band = 'U15'
        other = ['U13', 'U16', 'U17', 'U19']
    elif age_group == 'U15':
        dual_age_band = 'U16'
        other = ['U13', 'U14', 'U17', 'U19']
    elif age_group == 'U16':
        dual_age_band = 'U17'
        other = ['U13', 'U14', 'U15', 'U19']
    elif age_group == 'U17':
        dual_age_band = 'U19'
        other = ['U13', 'U14', 'U15', 'U16']
    if age_group == 'U19':
        dual_age_band = 'U17'
        other = ['U13', 'U14', 'U15', 'U16']

    colors = {age_group: '#429bf5', dual_age_band: 'black'}
    for element in other:
        colors[element] = 'gray'
    
    # Set DPI (dots per inch)
    fig = plt.figure(dpi=600)
    ax = fig.add_subplot(111)
    x_values = [0, 1.4]  # Adjust the range as needed
    y_values = [0, 1.4]  # Adjust the range as needed

    # Plot the diagonal line with a dotted black line
    plt.plot(x_values, y_values, color='black', linestyle='--', label='x=y', alpha=0.7)
    for key, value in colors.items():
        if key == 'U13':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['xG Value'], 
                        dataframe[dataframe['Team Category'] == key]['Goal'], 
                        color=value, 
                        label=key)  # Lower the opacity for gray points
        elif key == 'U14':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['xG Value'], 
                        dataframe[dataframe['Team Category'] == key]['Goal'], 
                        color=value, 
                        label=key)
        elif key == 'U15':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['xG Value'], 
                        dataframe[dataframe['Team Category'] == key]['Goal'], 
                        color=value, 
                        label=key)
        elif key == 'U16':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['xG Value'], 
                        dataframe[dataframe['Team Category'] == key]['Goal'], 
                        color=value, 
                        label=key)
        elif key == 'U17':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['xG Value'], 
                        dataframe[dataframe['Team Category'] == key]['Goal'], 
                        color=value, 
                        label=key)
        elif key == 'U19':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['xG Value'], 
                        dataframe[dataframe['Team Category'] == key]['Goal'], 
                        color=value, 
                        label=key)
        player_row = dataframe[dataframe['Player Name'] == pname]
        update_pname = pname + ' Fall 2024'
        plt.scatter(player_row['xG Value'], player_row['Goal'], color='orange', label=pname, s=70)
        custom_legend = [Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label=update_pname)]
        plt.xlabel('xG per 90', size = 11.5)
        plt.ylabel('Goal per 90', size = 11.5)
        plt.title('Goals and xG For Attackers', size = 14)


    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.set_facecolor('white')
    plt.gca().set_facecolor('white')


    # Place the legend in the upper left corner
    plt.legend(handles=custom_legend, loc='upper left')

    return fig

def attacker_function2(dataframe, age_group, pname, position):
    positions = []
    positions.append(position)


    if position == 'ATT':
        positions.append('Wing')
    elif position == 'Wing':
        positions.append('ATT')
    elif position == 'CM':
        positions.append('DM')
    elif position == 'DM':
        positions.append('CM')
    elif position == 'CB':
        positions.append('FB')
    elif position == 'FB':
        positions.append('CB')

    dataframe = dataframe.loc[dataframe['Position Tag'].isin(positions)]
    
    if age_group == 'U13':
        dual_age_band = 'U14'
        other = ['U15', 'U16', 'U17', 'U19']
    elif age_group == 'U14':
        dual_age_band = 'U15'
        other = ['U13', 'U16', 'U17', 'U19']
    elif age_group == 'U15':
        dual_age_band = 'U16'
        other = ['U13', 'U14', 'U17', 'U19']
    elif age_group == 'U16':
        dual_age_band = 'U17'
        other = ['U13', 'U14', 'U15', 'U19']
    elif age_group == 'U17':
        dual_age_band = 'U19'
        other = ['U13', 'U14', 'U15', 'U16']
    if age_group == 'U19':
        dual_age_band = 'U17'
        other = ['U13', 'U14', 'U15', 'U16']

    colors = {age_group: '#429bf5', dual_age_band: 'black'}
    for element in other:
        colors[element] = 'gray'
    
    dataframe.rename(columns={'Efforts on Goal': 'Shots',
                              'Goal': 'Goals'}, inplace=True)

    dataframe['Shots'] = (dataframe['Shots']/dataframe['mins played']) * 90
    dataframe['Goals'] = (dataframe['Goals']/dataframe['mins played']) * 90
    # Set DPI (dots per inch)
    fig = plt.figure(dpi=600)
    ax = fig.add_subplot(111)
    plt.axhline(y=dataframe['Shots'].mean(), color='black', linestyle='--', label='Avg Shots', alpha=0.6)
    plt.axvline(x=dataframe['Goals'].mean(), color='black', linestyle='--', label='Avg Goals', alpha=0.6)
    for key, value in colors.items():
        if key == 'U13':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Goals'], 
                        dataframe[dataframe['Team Category'] == key]['Shots'], 
                        color=value, 
                        label=key)  # Lower the opacity for gray points
        elif key == 'U14':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Goals'], 
                        dataframe[dataframe['Team Category'] == key]['Shots'], 
                        color=value, 
                        label=key)
        elif key == 'U15':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Goals'], 
                        dataframe[dataframe['Team Category'] == key]['Shots'], 
                        color=value, 
                        label=key)
        elif key == 'U16':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Goals'], 
                        dataframe[dataframe['Team Category'] == key]['Shots'], 
                        color=value, 
                        label=key)
        elif key == 'U17':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Goals'], 
                        dataframe[dataframe['Team Category'] == key]['Shots'], 
                        color=value, 
                        label=key)
        elif key == 'U19':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Goals'], 
                        dataframe[dataframe['Team Category'] == key]['Shots'], 
                        color=value, 
                        label=key)
        player_row = dataframe[dataframe['Player Name'] == pname]
        primary_player = player_row[player_row['Year'] == 'Spring'].reset_index(drop=True)
        if len(player_row) > 1:
            compare_player = player_row[player_row['Year'] == 'Fall'].reset_index(drop=True)
            recent_pass = primary_player['Goals'].iloc[0]
            recent_lb = primary_player['Shots'].iloc[0]
            compare_pass = compare_player['Goals'].iloc[0]
            compare_lb = compare_player['Shots'].iloc[0]
            if (recent_pass > compare_pass) and (recent_lb > compare_lb):
                update_color = 'green'
                plt.scatter(primary_player['Goals'], primary_player['Shots'], color=update_color, label=pname, s=70)
            elif (recent_pass < compare_pass) and (recent_lb < compare_lb):
                update_color = 'red'
                plt.scatter(primary_player['Goals'], primary_player['Shots'], color=update_color, label=pname, s=70)
            else:
                update_color = 'orange'
                plt.scatter(primary_player['Goals'], primary_player['Shots'], color=update_color, label=pname, s=70)
            update_pname = pname + ' Spring'
            later_pname = pname + ' Fall'
            plt.scatter(compare_player['Goals'], compare_player['Shots'], color='pink', label=later_pname, s=70)
            custom_legend = [Line2D([0], [0], marker='o', color='w', markerfacecolor=update_color, markersize=10, label=update_pname),
                                 Line2D([0], [0], marker='o', color='w', markerfacecolor='pink', markersize=10, label=later_pname)]
        else:
            update_pname = pname + ' Spring'
            plt.scatter(player_row['Goals'], player_row['Shots'], color='orange', label=pname, s=70)
            custom_legend = [Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label=update_pname)]
        plt.xlabel('Goals per 90', size = 11.5)
        plt.ylabel('Shots per 90', size = 11.5)
        plt.title('Goals and Shots per 90 For Attackers', size = 14)


    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.set_facecolor('white')
    plt.gca().set_facecolor('white')
    

    # Place the legend in the upper left corner
    plt.legend(handles=custom_legend, loc='upper left', bbox_to_anchor=(.05, 0.95))
    
    return fig