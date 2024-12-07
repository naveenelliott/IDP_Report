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

def createNewPizzaChart(bolts):
    # Load fonts
    font_path = 'Roboto-Regular.ttf'
    font_normal = FontProperties(fname=font_path)
    font_path_bold = 'Roboto-Bold.ttf'
    font_bold = FontProperties(fname=font_path_bold)

    # Load logo
    image_path = 'BostonBoltsLogo.png'  # Replace with the actual path to your image
    image = plt.imread(image_path)

    name_mapping = {
        'Forward Total Percentile': 'Forward Passes Percentile',
        'Pass Completion Percentile': 'Pass % Percentile',
        'Forward Completion Percentile': 'Forward Pass % Percentile',
        'Stand. Tackle Total Percentile': 'Total Tackles Percentile',
        'Rec Total Percentile': 'Total Recoveries Percentile',
        'Inter Total Percentile': 'Total Interceptions Percentile',
        'Progr Regain Percentile': 'Regain % Percentile',
        'Stand. Tackle Success Percentile': 'Tackle % Percentile',
        'Efforts on Goal Percentile': 'Shots Percentile',
        'Pass into Oppo Box Percentile': 'Passes into 18 Percentile'
    }

    name_mapping_filtered = {col: name_mapping[col] for col in bolts.columns if col in name_mapping}

    bolts.rename(columns=name_mapping_filtered, inplace=True)


    grouped = bolts.groupby('Player Name')

    # Define columns for each position
    position_columns = {
        'ATT': [
            'Total Tackles Percentile', 'Total Recoveries Percentile', 'Total Passes Percentile',
            'Pass % Percentile', 'Att 1v1 Percentile', 'Loss of Poss Percentile',
            'Shots Percentile', 'Shot on Target Percentile', 'Efficiency Percentile'
        ],
        'Wing': [
            'Total Tackles Percentile', 'Total Recoveries Percentile', 'Total Passes Percentile',
            'Pass % Percentile', 'Passes into 18 Percentile', 'Forward Pass % Percentile',
            'Dribble Percentile', 'Att 1v1 Percentile', 'Loss of Poss Percentile',
            'Shots Percentile', 'Shot on Target Percentile'
        ],
        'CM': [
            'Dribble Percentile', 'Loss of Poss Percentile', 'Total Tackles Percentile',
            'Total Recoveries Percentile', 'Regain % Percentile', 'Total Passes Percentile',
            'Pass % Percentile', 'Forward Passes Percentile', 'Forward Pass % Percentile',
            'Passes into 18 Percentile', 'Shots Percentile'
        ],
        'DM': [
            'Total Passes Percentile', 'Forward Passes Percentile', 'Pass % Percentile',
            'Forward Pass % Percentile', 'Total Tackles Percentile', 'Total Recoveries Percentile',
            'Regain % Percentile', 'Tackle % Percentile', 'Dribble Percentile',
            'Loss of Poss Percentile'
        ],
        'CB': [
            'Total Recoveries Percentile', 'Regain % Percentile', 'Tackle % Percentile',
            'Forward Passes Percentile', 'Passing Total Percentile', 'Pass % Percentile',
            'Forward Pass % Percentile', 'Loss of Poss Percentile'
        ],
        'FB': [
            'Total Tackles Percentile', 'Total Recoveries Percentile', 'Regain % Percentile',
            'Tackle % Percentile', 'Forward Passes Percentile', 'Total Passes Percentile',
            'Pass % Percentile', 'Forward Pass % Percentile', 'Dribble Percentile',
            'Loss of Poss Percentile', 'Passes into 18 Percentile'
        ]
    }

    for player_name, group in grouped:
        position = group['Position'].iloc[0]
        if position not in position_columns:
            continue  # Skip unknown positions

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

                # Define colors for slices and text
                slice_colors = ["#6bb2e2"] * len(params)  # Slices always light blue
                compare_colors = []  # Box colors for number values
                for spring_val, dec_val in zip(values, other_vals):
                    if dec_val > spring_val:
                        compare_colors.append("red")  # Worse performance
                    elif dec_val == spring_val:
                        compare_colors.append("orange")  # No change
                    else:
                        compare_colors.append("green")  # Better performance

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
                    slice_colors=slice_colors,  # Slices stay light blue
                    value_bck_colors=slice_colors,  # Slice background stays light blue
                    compare_colors=slice_colors,  # Slices themselves stay light blue
                    compare_value_colors=["#FFFFFF"] * len(params),  # White text
                    compare_value_bck_colors=compare_colors,  # Box colors change based on performance
                    blank_alpha=0.4,
                    kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=1),
                    kwargs_compare=dict(edgecolor="#F2F2F2", zorder=3, linewidth=2),
                    kwargs_params=dict(color="#000000", fontsize=13, fontproperties=font_normal, va="center"),
                    kwargs_values=dict(
                        color="#FFFFFF", fontsize=13, fontproperties=font_normal, zorder=3,
                        bbox=dict(edgecolor="#000000", facecolor="cornflowerblue", boxstyle="round,pad=0.2", lw=1)
                    ),
                    kwargs_compare_values=dict(
                        color="#FFFFFF", fontsize=13, fontproperties=font_normal, zorder=3,
                        bbox=dict(edgecolor="#000000", boxstyle="round,pad=0.2", lw=1)
                    )
                )
            else:  # If only 2024 data exists
                slice_colors = ["#6bb2e2"] * len(params)  # Light blue slices
                text_colors = ["#FFFFFF"] * len(params)  # White text for numbers

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
                    slice_colors=slice_colors,  # Slices remain light blue
                    value_colors=text_colors,  # White text for values
                    value_bck_colors=slice_colors,  # Slice backgrounds remain light blue
                    blank_alpha=0.4,
                    kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=1),
                    kwargs_params=dict(color="#000000", fontsize=13, fontproperties=font_normal, va="center"),
                    kwargs_values=dict(
                        color="#FFFFFF", fontsize=13, fontproperties=font_normal, zorder=3,
                        bbox=dict(edgecolor="#000000", facecolor="cornflowerblue", boxstyle="round,pad=0.2", lw=1)
                    )
                )

            # Adjust for overlapping text
            baker.adjust_texts(params_offset=[True] * len(params), offset=-0.15, adj_comp_values=True)

            fig.set_dpi(600)
            fig.set_facecolor('white')
            plt.gca().set_facecolor('white')

    return fig
