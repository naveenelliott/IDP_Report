import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def plottingMinsPlayed(player_name, percentage_played):
    # Create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(8, 2))
    plt.barh([player_name], [percentage_played], color='lightblue')

    plt.title(f'Percent of Mins Played', fontsize=40)

    plt.xlim(0, 100)

    # Show the percentage value on the bar
    for index, value in enumerate([percentage_played]):
        plt.text(value + 1, index, f'{value:.2f}%', va='center', fontsize=40)

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

    # Show the percentage value on the bar
    for index, value in enumerate([percentage_played]):
        plt.text(value + 1, index, f'{value:.2f}%', va='center', fontsize=40)

    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])

    plt.tight_layout()

    return fig
