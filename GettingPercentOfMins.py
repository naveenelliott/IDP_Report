import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def plottingMinsPlayed(player_name, percentage_played):
    # Create a horizontal bar chart with consistent settings
    fig, ax = plt.subplots(figsize=(10, 2))  # Consistent figure size
    plt.barh([player_name], [percentage_played], color='lightblue')

    plt.title('% of Mins Played', fontsize=30)  # Consistent font size
    plt.xlim(0, 100)  # Same x-axis range for consistency

    # Place the text consistently outside the bar
    fixed_position = 105  # Fixed offset outside the chart area
    for index, value in enumerate([percentage_played]):
        plt.text(fixed_position, index, f'{value:.2f}%', va='center', fontsize=25)  # Consistent text size

    ax.xaxis.set_ticks([])  # Hide x-axis ticks
    ax.yaxis.set_ticks([])  # Hide y-axis ticks

    plt.tight_layout()

    return fig

def plottingStarts(player_name, percentage_played):
    # Create a horizontal bar chart with consistent settings
    fig, ax = plt.subplots(figsize=(10, 2))  # Consistent figure size
    plt.barh([player_name], [percentage_played], color='lightblue')

    plt.title('% of Starts', fontsize=30)  # Consistent font size
    plt.xlim(0, 100)  # Same x-axis range for consistency

    # Place the text consistently outside the bar
    fixed_position = 105  # Fixed offset outside the chart area
    for index, value in enumerate([percentage_played]):
        plt.text(fixed_position, index, f'{value:.2f}%', va='center', fontsize=25)  # Consistent text size

    ax.xaxis.set_ticks([])  # Hide x-axis ticks
    ax.yaxis.set_ticks([])  # Hide y-axis ticks

    plt.tight_layout()

    return fig
