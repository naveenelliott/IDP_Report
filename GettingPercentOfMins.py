import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def plottingMinsPlayed(player_name, percentage_played):
    # Create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(8, 2))
    plt.barh([player_name], [percentage_played], color='lightblue')

    plt.title('% of Mins Played', fontsize=40)

    plt.xlim(0, 100)

    # Define a fixed position for the text, regardless of percentage value
    fixed_position = 105  # This places all text consistently to the right of the chart area
    for index, value in enumerate([percentage_played]):
        plt.text(fixed_position, index, f'{value:.2f}%', va='center', fontsize=40)  # Consistent position

    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])

    plt.tight_layout()

    return fig

def plottingStarts(player_name, percentage_played):
    # Create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(8, 2))
    plt.barh([player_name], [percentage_played], color='lightblue')

    plt.title('Percent of Starts', fontsize=40)

    plt.xlim(0, 100)

    # Define a fixed position for the text, regardless of percentage value
    fixed_position = 105  # This places all text consistently to the right of the chart area
    for index, value in enumerate([percentage_played]):
        plt.text(fixed_position, index, f'{value:.2f}%', va='center', fontsize=40)  # Consistent position

    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])

    plt.tight_layout()

    return fig
