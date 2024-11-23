from PIL import Image
from mplsoccer import PyPizza, add_image, FontManager
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.font_manager import FontProperties
import streamlit as st

from PIL import Image
from mplsoccer import PyPizza, add_image, FontManager
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
import streamlit as st

def createPizzaChart(bolts):
    # Load fonts
    font_path = 'Roboto-Regular.ttf'
    font_normal = FontProperties(fname=font_path)
    font_path_bold = 'Roboto-Bold.ttf'
    font_bold = FontProperties(fname=font_path_bold)

    # Load logo
    image_path = 'BostonBoltsLogo.png'  # Replace with the actual path to your image
    image = plt.imread(image_path)

    grouped = bolts.groupby('Player Name')

    # Define columns for each position
    position_columns = {
        'ATT': [
            'Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Total Passes Percentile',
            'Pass Completion Percentile', 'Att 1v1 Percentile', 'Loss of Poss Percentile',
            'Efforts on Goal Percentile', 'Shot on Target Percentile', 'Efficiency Percentile'
        ],
        'Wing': [
            'Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Total Passes Percentile',
            'Pass Completion Percentile', 'Pass into Oppo Box Percentile', 'Forward Completion Percentile',
            'Dribble Percentile', 'Att 1v1 Percentile', 'Loss of Poss Percentile',
            'Efforts on Goal Percentile', 'Shot on Target Percentile'
        ],
        'CM': [
            'Dribble Percentile', 'Loss of Poss Percentile', 'Stand. Tackle Total Percentile',
            'Rec Total Percentile', 'Progr Regain Percentile', 'Total Passes Percentile',
            'Pass Completion Percentile', 'Forward Total Percentile', 'Forward Completion Percentile',
            'Line Break Percentile', 'Pass into Oppo Box Percentile', 'Efforts on Goal Percentile'
        ],
        'DM': [
            'Total Passes Percentile', 'Forward Total Percentile', 'Pass Completion Percentile',
            'Forward Completion Percentile', 'Stand. Tackle Total Percentile', 'Rec Total Percentile',
            'Progr Regain Percentile', 'Stand. Tackle Success Percentile', 'Dribble Percentile',
            'Loss of Poss Percentile', 'Line Break Percentile'
        ],
        'CB': [
            'Rec Total Percentile', 'Progr Regain Percentile', 'Stand. Tackle Success',
            'Forward Total Percentile', 'Passing Total Percentile', 'Pass Completion Percentile',
            'Forward Completion Percentile', 'Line Break Percentile', 'Loss of Poss Percentile'
        ],
        'FB': [
            'Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Progr Regain Percentile',
            'Stand. Tackle Success Percentile', 'Forward Total Percentile', 'Total Passes Percentile',
            'Pass Completion Percentile', 'Forward Completion Percentile', 'Dribble Percentile',
            'Loss of Poss Percentile', 'Line Break Percentile', 'Pass into Oppo Box Percentile'
        ]
    }

    # Iterate over grouped players
    for player_name, group in grouped:
        position = group['Position'].iloc[0]
        if position not in position_columns:
            continue  # Skip unknown positions

        player_named = group['Player Name'].iloc[0]
        position_columns_list = position_columns[position]
        position_columns_wout = [col.replace(' Percentile', '') for col in position_columns_list]
        group = group.fillna(0)
        params = list(position_columns_wout)

        # Filter data by year
        row_2024 = group[group['Date'] == '2024']
        row_2023 = group[group['Date'] == '2023']

        if not row_2024.empty:  # Ensure 2024 data exists
            values = [int(row_2024[col].iloc[0]) for col in position_columns_list]

            if not row_2023.empty:  # If both 2024 and 2023 data exist
                other_vals = [int(row_2023[col].iloc[0]) for col in position_columns_list]

                # Colors for comparison
                slice_colors = []
                slice_colors_bck = ["#6bb2e2"] * len(params)  # Light blue for slices
                compare_colors = []
                for spring_val, dec_val in zip(values, other_vals):
                    if dec_val > spring_val:
                        compare_colors.append('red')
                        slice_colors.append("#6bb2e2")
                    elif dec_val == spring_val:
                        compare_colors.append('orange')
                        slice_colors.append("#6bb2e2")
                    else:
                        compare_colors.append('green')
                        slice_colors.append("#6bb2e2")

                # Instantiate PyPizza for comparison
                baker = PyPizza(
                    params=params,
                    background_color="white",
                    straight_line_color="#EBEBE9",
                    straight_line_lw=1,
                    last_circle_lw=0,
                    other_circle_lw=0,
                    inner_circle_size=9
                )

                # Plot comparison pizza chart
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
                    kwargs_values=dict(color="#000000", fontsize=13, fontproperties=font_normal),
                    kwargs_compare_values=dict(color="#000000", fontsize=13, fontproperties=font_normal)
                )

            else:  # If only 2024 data exists
                slice_colors = ["#6bb2e2"] * len(params)  # Default color
                value_colors = ["#000000"] * len(params)  # Default text color

                # Instantiate PyPizza for single-year data
                baker = PyPizza(
                    params=params,
                    background_color="white",
                    straight_line_color="#EBEBE9",
                    straight_line_lw=1,
                    last_circle_lw=0,
                    other_circle_lw=0,
                    inner_circle_size=9
                )

                # Plot single-year pizza chart
                fig, ax = baker.make_pizza(
                    values,
                    figsize=(8, 8.5),
                    color_blank_space="same",
                    slice_colors=slice_colors,
                    value_colors=value_colors,
                    kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=1),
                    kwargs_params=dict(color="#000000", fontsize=13, fontproperties=font_normal, va="center"),
                    kwargs_values=dict(color="#000000", fontsize=13, fontproperties=font_normal)
                )

            fig.set_dpi(600)
            fig.set_facecolor('white')
            plt.gca().set_facecolor('white')

    return fig
