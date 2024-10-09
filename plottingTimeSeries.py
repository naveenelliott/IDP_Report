import plotly.graph_objs as go
import pandas as pd
import streamlit as st
from scipy.stats import norm
import numpy as np
from numpy.polynomial.polynomial import Polynomial
import glob
import os

def plottingStatistics(dataframe, statistic):
    # Create the plot
    fig = go.Figure()

    dataframe['More Opposition'] = 'vs ' + dataframe['Opposition']
    dataframe['Match Date'] = pd.to_datetime(dataframe['Match Date']).dt.strftime('%m/%d/%Y')

    # Add the trendline to the plot
    fig.add_trace(go.Scatter(
        x=dataframe['Match Date'],
        y=dataframe[statistic],
        mode='lines',
        name='Trendline',
        line=dict(color='black', dash='dash'),
        showlegend=True  # Show the legend for the trendline
    ))

    current_game_shown = False
    # Line plot for the specified statistic over time
    for index, row in dataframe.iterrows():
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

    # Display the plot in Streamlit
    return fig