import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import streamlit as st


def gettingPlayerDataPlot(player_df, other_player_df):

    positions = []

    if player_df.empty:
        fig = plt.figure(dpi=600)
        ax = fig.add_subplot(111)
        plt.scatter([], [])
        
        plt.xlabel('Avg Training Load Total Distance', size = 10.5)
        plt.ylabel('Avg Training Load High Intensity Distance', size = 10.5)
        plt.title('Distance and High Intensity Distance Training Load', size = 12)
    
        ax.annotate(
            "No data available",
            xy=(0.5, 0.5),
            xycoords="axes fraction",
            ha="center",
            va="center",
            fontsize=12,
            color="gray"
        )

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.set_facecolor('white')
    else:
        player_name = player_df['Player Full Name'].iloc[0]
        player_name = player_name.title()
        age_player_df = player_df['Team Category'].iloc[0]
        player_df.loc[player_df['Position Tag'] == 'AM', 'Position Tag'] = 'CM' 
        position = player_df['Position Tag'].iloc[0]
        positions.append(position)
    
        if position == 'ATT':
            positions.append('Wing')
        elif position == 'Wing':
            positions.append('ATT')
        elif position == 'CM':
            positions.append('DM')
        elif position == 'DM':
            positions.append('CM')
    
        if age_player_df == 'U13':
            dual_age_band = 'U14'
        elif age_player_df == 'U14':
            dual_age_band = 'U15'
        elif age_player_df == 'U15':
            dual_age_band = 'U16'
        elif age_player_df == 'U16':
            dual_age_band = 'U17'
        elif age_player_df == 'U17':
            dual_age_band = 'U19'
        if age_player_df == 'U19':
            dual_age_band = 'U17'
    
        teams_want = [age_player_df, dual_age_band]
    
        result_df = other_player_df[(other_player_df['Team Category'].isin(teams_want)) &
                        (other_player_df['Position Tag'].isin(positions))]
        
        colors = {age_player_df: '#429bf5', dual_age_band: 'black'}
        
        fig = plt.figure(dpi=600)
        ax = fig.add_subplot(111)
        plt.axhline(y=result_df['Avg_High_Intensity_Distance'].mean(), color='black', linestyle='--', label='Avg HID', alpha=0.6)
        plt.axvline(x=result_df['Avg_Total_Distance'].mean(), color='black', linestyle='--', label='Avg Dist per Min', alpha=0.6)
        for category, color in colors.items():
            plt.scatter(result_df[result_df['Team Category'] == category]['Avg_Total_Distance'], 
                    result_df[result_df['Team Category'] == category]['Avg_High_Intensity_Distance'], 
                    color=color, label=category)
        plt.scatter(player_df['Avg_Total_Distance'], player_df['Avg_High_Intensity_Distance'], color='orange', label=player_name, s=70)
        custom_legend = [Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label=player_name)]
    
        plt.xlabel('Avg Training Load Total Distance', size = 10.5)
        plt.ylabel('Avg Training Load High Intensity Distance', size = 10.5)
        plt.title(f'Distance and High Intensity Distance Training Load For {position}', size = 12)
    
    
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.set_facecolor('white')
        plt.gca().set_facecolor('white')
    
        # Place the legend in the upper left corner
        plt.legend(handles=custom_legend, loc='upper left')


    return fig

