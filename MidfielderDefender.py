import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import streamlit as st

def midfielder_function(dataframe, age_group, pname, position):
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
    plt.axhline(y=dataframe['Line Break'].mean(), color='black', linestyle='--', label='Avg Line Breaks', alpha=0.6)
    plt.axvline(x=dataframe['Pass %'].mean(), color='black', linestyle='--', label='Avg Pass %', alpha=0.6)
    for key, value in colors.items():
        if key == 'U13':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Pass %'], 
                        dataframe[dataframe['Team Category'] == key]['Line Break'], 
                        color=value, 
                        label=key)  # Lower the opacity for gray points
        elif key == 'U14':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Pass %'], 
                        dataframe[dataframe['Team Category'] == key]['Line Break'], 
                        color=value, 
                        label=key)
        elif key == 'U15':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Pass %'], 
                        dataframe[dataframe['Team Category'] == key]['Line Break'], 
                        color=value, 
                        label=key)
        elif key == 'U16':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Pass %'], 
                        dataframe[dataframe['Team Category'] == key]['Line Break'], 
                        color=value, 
                        label=key)
        elif key == 'U17':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Pass %'], 
                        dataframe[dataframe['Team Category'] == key]['Line Break'], 
                        color=value, 
                        label=key)
        elif key == 'U19':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Pass %'], 
                        dataframe[dataframe['Team Category'] == key]['Line Break'], 
                        color=value, 
                        label=key)
        player_row = dataframe[dataframe['Player Name'] == pname]
        primary_player = player_row[player_row['Year'] == '2024'].reset_index(drop=True)
        if len(player_row) > 1:
            compare_player = player_row[player_row['Year'] == '2023'].reset_index(drop=True)
            recent_pass = primary_player['Pass %'].iloc[0]
            recent_lb = primary_player['Line Break'].iloc[0]
            compare_pass = compare_player['Pass %'].iloc[0]
            compare_lb = compare_player['Line Break'].iloc[0]
            if (recent_pass > compare_pass) and (recent_lb > compare_lb):
                update_color = 'green'
                plt.scatter(primary_player['Pass %'], primary_player['Line Break'], color=update_color, label=pname, s=70)
            elif (recent_pass < compare_pass) and (recent_lb < compare_lb):
                update_color = 'red'
                plt.scatter(primary_player['Pass %'], primary_player['Line Break'], color=update_color, label=pname, s=70)
            else:
                update_color = 'orange'
                plt.scatter(primary_player['Pass %'], primary_player['Line Break'], color=update_color, label=pname, s=70)
            update_pname = pname + ' This Season'
            later_pname = pname + ' Last Seaosn'
            plt.scatter(compare_player['Pass %'], compare_player['Line Break'], color='pink', label=later_pname, s=70)
            custom_legend = [Line2D([0], [0], marker='o', color='w', markerfacecolor=update_color, markersize=10, label=update_pname),
                                 Line2D([0], [0], marker='o', color='w', markerfacecolor='pink', markersize=10, label=later_pname)]
        else:
            update_pname = pname + ' This Season'
            plt.scatter(player_row['Pass %'], player_row['Line Break'], color='orange', label=pname, s=70)
            custom_legend = [Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label=update_pname)]
        plt.xlabel('Pass Percentage', size = 11.5)
        plt.ylabel('Line Breaks per 90', size = 11.5)
        plt.title('Pass Percentage and Line Breaks For Midfielders', size = 14)


    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.set_facecolor('white')
    plt.gca().set_facecolor('white')
    

    # Place the legend in the upper left corner
    plt.legend(handles=custom_legend, loc='upper left', bbox_to_anchor=(.05, 0.95))
    
    return fig

def defender_function(dataframe, age_group, pname, position):
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
    plt.axhline(y=dataframe['Tackle %'].mean(), color='black', linestyle='--', label='Avg Tackle %', alpha=0.6)
    plt.axvline(x=dataframe['Progr Regain %'].mean(), color='black', linestyle='--', label='Avg Progr Regain %', alpha=0.6)
    for key, value in colors.items():
        if key == 'U13':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Progr Regain %'], 
                        dataframe[dataframe['Team Category'] == key]['Tackle %'], 
                        color=value, 
                        label=key)
        elif key == 'U14':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Progr Regain %'], 
                        dataframe[dataframe['Team Category'] == key]['Tackle %'], 
                        color=value, 
                        label=key)
        elif key == 'U15':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Progr Regain %'], 
                        dataframe[dataframe['Team Category'] == key]['Tackle %'], 
                        color=value, 
                        label=key)
        elif key == 'U16':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Progr Regain %'], 
                        dataframe[dataframe['Team Category'] == key]['Tackle %'], 
                        color=value, 
                        label=key)
        elif key == 'U17':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Progr Regain %'], 
                        dataframe[dataframe['Team Category'] == key]['Tackle %'], 
                        color=value, 
                        label=key)
        elif key == 'U19':
            plt.scatter(dataframe[dataframe['Team Category'] == key]['Progr Regain %'], 
                        dataframe[dataframe['Team Category'] == key]['Tackle %'], 
                        color=value, 
                        label=key)
        player_row = dataframe[dataframe['Player Name'] == pname]
        primary_player = player_row[player_row['Year'] == '2024'].reset_index(drop=True)
        if len(player_row) > 1:
            compare_player = player_row[player_row['Year'] == '2023'].reset_index(drop=True)
            recent_regain = primary_player['Progr Regain %'].iloc[0]
            recent_tack = primary_player['Tackle %'].iloc[0]
            compare_regain = compare_player['Progr Regain %'].iloc[0]
            compare_tack = compare_player['Tackle %'].iloc[0]
            if (recent_regain > compare_regain) and (recent_tack > compare_tack):
                update_color = 'green'
                plt.scatter(player_row['Progr Regain %'], player_row['Tackle %'], color=update_color, label=pname, s=70)
            elif (recent_regain < compare_regain) and (recent_tack < compare_tack):
                update_color = 'red'
                plt.scatter(player_row['Progr Regain %'], player_row['Tackle %'], color=update_color, label=pname, s=70)
            else:
                update_color = 'orange'
                plt.scatter(player_row['Progr Regain %'], player_row['Tackle %'], color=update_color, label=pname, s=70)
            update_pname = pname + ' This Season'
            later_pname = pname + ' Last Seaosn'
            plt.scatter(compare_player['Progr Regain %'], compare_player['Tackle %'], color='pink', label=later_pname, s=70)
            custom_legend = [Line2D([0], [0], marker='o', color='w', markerfacecolor=update_color, markersize=10, label=update_pname),
                                 Line2D([0], [0], marker='o', color='w', markerfacecolor='pink', markersize=10, label=later_pname)]
        else:
            update_pname = pname + ' This Season'
            plt.scatter(player_row['Progr Regain %'], player_row['Line Breaks'], color='orange', label=pname, s=70)
            custom_legend = [Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label=update_pname)]
        plt.xlabel('Progressive Regain %', size = 11.5)
        plt.ylabel('Tackle %', size = 11.5)
        plt.title('Tackle and Progressive Regain Percentages For Defenders', size = 14)


    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.set_facecolor('white')
    plt.gca().set_facecolor('white')

    # Place the legend in the upper left corner
    plt.legend(handles=custom_legend, loc='upper left')

    return fig

