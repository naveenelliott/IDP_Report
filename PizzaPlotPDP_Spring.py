from PIL import Image
from mplsoccer import PyPizza, add_image, FontManager
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.font_manager import FontProperties
import streamlit as st

from PIL import Image
from mplsoccer import PyPizza
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pandas as pd

def createPizzaChart(bolts):
    # Load fonts
    font_path = 'Roboto-Regular.ttf'
    font_normal = FontProperties(fname=font_path)
    font_bold_path = 'Roboto-Bold.ttf'
    font_bold = FontProperties(fname=font_bold_path)

    # Group data by player name
    grouped = bolts.groupby('Player Name')

    # Iterate over each player group
    for player_name, group in grouped:
        position = group['Position'].iloc[0]

        # Define parameters for each position
        if position == 'ATT':
            columns = ['Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Total Passes Percentile',
                       'Pass Completion Percentile', 'Att 1v1 Percentile', 'Loss of Poss Percentile',
                       'Efforts on Goal Percentile', 'Shot on Target Percentile', 'Efficiency Percentile']
        elif position == 'Wing':
            columns = ['Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Total Passes Percentile',
                       'Pass Completion Percentile', 'Pass into Oppo Box Percentile', 'Forward Completion Percentile',
                       'Dribble Percentile', 'Att 1v1 Percentile', 'Loss of Poss Percentile',
                       'Efforts on Goal Percentile', 'Shot on Target Percentile']
        elif position == 'CM':
            columns = ['Dribble Percentile', 'Loss of Poss Percentile', 'Stand. Tackle Total Percentile',
                       'Rec Total Percentile', 'Progr Regain Percentile', 'Total Passes Percentile',
                       'Pass Completion Percentile', 'Forward Total Percentile', 'Forward Completion Percentile',
                       'Line Break Percentile', 'Pass into Oppo Box Percentile', 'Efforts on Goal Percentile']
        elif position == 'DM':
            columns = ['Total Passes Percentile', 'Forward Total Percentile', 'Pass Completion Percentile',
                       'Forward Completion Percentile', 'Stand. Tackle Total Percentile', 'Rec Total Percentile',
                       'Progr Regain Percentile', 'Stand. Tackle Success Percentile', 'Dribble Percentile',
                       'Loss of Poss Percentile', 'Line Break Percentile']
        elif position == 'CB':
            columns = ['Rec Total Percentile', 'Progr Regain Percentile', 'Stand. Tackle Success',
                       'Forward Total Percentile', 'Passing Total Percentile', 'Pass Completion Percentile',
                       'Forward Completion Percentile', 'Line Break Percentile', 'Loss of Poss Percentile']
        elif position == 'FB':
            columns = ['Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Progr Regain Percentile',
                       'Stand. Tackle Success Percentile', 'Forward Total Percentile', 'Total Passes Percentile',
                       'Pass Completion Percentile', 'Forward Completion Percentile', 'Dribble Percentile',
                       'Loss of Poss Percentile', 'Line Break Percentile', 'Pass into Oppo Box Percentile']
        else:
            continue  # Skip positions not covered

        # Replace " Percentile" for display in the pizza chart
        params = [col.replace(' Percentile', '') for col in columns]
        group = group.fillna(0)

        # Check for 2024 and 2023 data
        row_2024 = group[group['Date'] == '2024']
        row_2023 = group[group['Date'] == '2023']

        if not row_2024.empty:  # Ensure 2024 data exists
            values = [int(row_2024[col].iloc[0]) for col in columns]

            if not row_2023.empty:  # If 2023 data also exists, compare
                other_vals = [int(row_2023[col].iloc[0]) for col in columns]

                # Define slice and comparison colors
                slice_colors = ["#6bb2e2"] * len(params)
                compare_colors = []
                for spring_val, dec_val in zip(values, other_vals):
                    if dec_val > spring_val:
                        compare_colors.append('red')
                    elif dec_val == spring_val:
                        compare_colors.append('orange')
                    else:
                        compare_colors.append('green')

                # Create comparison pizza chart
                baker = PyPizza(
                    params=params,
                    background_color="white",
                    straight_line_color="#EBEBE9",
                    straight_line_lw=1,
                    last_circle_lw=0,
                    other_circle_lw=0,
                    inner_circle_size=9
                )
                fig, ax = baker.make_pizza(
                    other_vals,
                    compare_values=values,
                    figsize=(8, 8.5),
                    color_blank_space="same",
                    slice_colors=slice_colors,
                    compare_colors=compare_colors,
                    kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=1),
                    kwargs_compare=dict(edgecolor="#F2F2F2", zorder=3, linewidth=2),
                    kwargs_params=dict(color="#000000", fontsize=13, fontproperties=font_normal, va="center"),
                    kwargs_values=dict(
                        color="#000000", fontsize=13, fontproperties=font_normal, zorder=3,
                        bbox=dict(
                            edgecolor="#000000", facecolor="cornflowerblue",
                            boxstyle="round,pad=0.3", lw=1
                        )
                    ),
                    kwargs_compare_values=dict(
                        color="#000000", fontsize=13, fontproperties=font_normal, zorder=3,
                        bbox=dict(
                            edgecolor="#000000", facecolor="cornflowerblue",
                            boxstyle="round,pad=0.3", lw=1
                        )
                    )
                )

            else:  # If only 2024 data exists
                slice_colors = ["#6bb2e2"] * len(params)

                # Create single-year pizza chart
                baker = PyPizza(
                    params=params,
                    background_color="white",
                    straight_line_color="#EBEBE9",
                    straight_line_lw=1,
                    last_circle_lw=0,
                    other_circle_lw=0,
                    inner_circle_size=9
                )
                fig, ax = baker.make_pizza(
                    values,
                    figsize=(8, 8.5),
                    color_blank_space="same",
                    slice_colors=slice_colors,
                    kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=1),
                    kwargs_params=dict(color="#000000", fontsize=13, fontproperties=font_normal, va="center"),
                    kwargs_values=dict(
                        color="#000000", fontsize=13, fontproperties=font_normal, zorder=3,
                        bbox=dict(
                            edgecolor="#000000", facecolor="cornflowerblue",
                            boxstyle="round,pad=0.3", lw=1
                        )
                    )
                )

            # Save or display the figure
            fig.set_dpi(600)
            fig.set_facecolor('white')
            plt.gca().set_facecolor('white')

    return fig
