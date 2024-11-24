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

def createPizzaChart(bolts):

    font_path = 'Roboto-Regular.ttf'
    font_normal = FontProperties(fname=font_path)

    
    font_path = 'Roboto-Bold.ttf'
    font_bold = FontProperties(fname=font_path)


    image_path = 'BostonBoltsLogo.png'  # Replace with the actual path to your image
    image = plt.imread(image_path)


    grouped = bolts.groupby('Player Name')

    for player_name, group in grouped:
        if group['Position'].iloc[0] == 'ATT':
            player_named = group['Player Name'].iloc[0]
            if (len(group['Position']) > 1) and (group['Position'] == 'ATT').all():
                cf_columns = ['Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Total Passes Percentile', 'Pass Completion Percentile', 
                'Att 1v1 Percentile', 'Loss of Poss Percentile', 'Efforts on Goal Percentile', 'Shot on Target Percentile',
                'Efficiency Percentile']
                cf_columns_wout = [col.replace(' Percentile', '') for col in cf_columns]
                group = group.fillna(0)
                params = list(cf_columns_wout)
                row_2024 = group[group['Date'] == '2024']
                row_2023 = group[group['Date'] == '2023']
                values = [int(row_2024[col]) for col in cf_columns]
                other_vals = [int(row_2023[col]) for col in cf_columns]

                params_offset = [True] * len(params)
                
                # color for the slices and text
                slice_colors = []
                slice_colors_bck = ["#6bb2e2"] * len(params)  # Use light blue for all slices
                text_colors =  ["#F2F2F2"] * len(params)
                text_colors_bck =  []
                compare_colors_bck = []
                
                compare_val_colors = len(values)*['#F2F2F2']
            
                compare_colors = []
                for spring_val, dec_val, color in zip(values, other_vals, slice_colors_bck):
                    if dec_val > spring_val:
                        compare_colors.append('red')
                        slice_colors.append(color)
                        text_colors_bck.append('red')
                        compare_colors_bck.append('red')
                    elif dec_val == spring_val:
                        compare_colors.append('orange')
                        slice_colors.append(color)
                        text_colors_bck.append('orange')
                        compare_colors_bck.append('orange')
                    elif dec_val < spring_val:
                        compare_colors.append('green')
                        slice_colors.append(color)
                        text_colors_bck.append('green')
                        compare_colors_bck.append('green')
            
                # instantiate PyPizza class
                baker = PyPizza(
                    params=params,                  # list of parameters
                    background_color="white",     # background color
                    straight_line_color="#EBEBE9",  # color for straight lines
                    straight_line_lw=1,             # linewidth for straight lines
                    last_circle_lw=0,               # linewidth of last circle
                    other_circle_lw=0,              # linewidth for other circles
                    inner_circle_size=9         # size of inner circle
                    )

                # plot pizza
                fig, ax = baker.make_pizza(
                    other_vals,     
                    compare_values=values,                     # list of values
                        figsize=(8, 8.5),                # adjust figsize according to your need
                        color_blank_space="same",        # use same color to fill blank space
                        slice_colors=slice_colors,       # color for individual slices
                        value_colors=text_colors,        # color for the value-text
                        value_bck_colors=slice_colors,   # color for the blank spaces
                        blank_alpha=0.4,                 # alpha for blank-space colors
                        compare_colors = slice_colors,
                        compare_value_colors = compare_val_colors,
                        compare_value_bck_colors = compare_colors_bck,
                        kwargs_slices=dict(
                            edgecolor="#F2F2F2", zorder=2, linewidth=1
                            ),                               # values to be used when plotting slices
                        kwargs_compare=dict(
                            edgecolor='#F2F2F2', zorder=3, linewidth=2
                            ), 
                        kwargs_params=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, va="center"
                            ),                               # values to be used when adding parameter
                        kwargs_values=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            ),
                        kwargs_compare_values=dict(
                            color='#F2F2F2', fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            )
                    # values to be used when adding parameter-values
                    )

                baker.adjust_texts(params_offset, offset=-0.2, adj_comp_values=True)
                
                fig.set_dpi(600)
            
                fig.set_facecolor('white')
                plt.gca().set_facecolor('white')
            else:
                cf_columns = ['Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Total Passes Percentile', 'Pass Completion Percentile', 
                    'Att 1v1 Percentile', 'Loss of Poss Percentile', 'Efforts on Goal Percentile', 'Shot on Target Percentile',
                    'Efficiency Percentile']
                cf_columns_wout = [col.replace(' Percentile', '') for col in cf_columns]
                cf_filtered = group[cf_columns]
                found_2024=False
                for index, row in group.iterrows():
                    if row['Date'] == '2024':
                        group = row
                        found_2024 = True
                        break
                if not found_2024:
                    group = group.head(1)
                params = list(cf_columns_wout)
                values = [int(group[col]) for col in cf_columns]

                # color for the slices and text
                slice_colors = ["#6bb2e2"] * len(params)  # Use light blue for all slices 
                text_colors =  ["#000000"] * 2 + ["#000000"] * 2 + ["#F2F2F2"] * 2 + ['#F2F2F2'] * 3
            
                # instantiate PyPizza class
                baker = PyPizza(
                    params=params,                  # list of parameters
                    background_color="white",     # background color
                    straight_line_color="#EBEBE9",  # color for straight lines
                    straight_line_lw=1,             # linewidth for straight lines
                    last_circle_lw=0,               # linewidth of last circle
                    other_circle_lw=0,              # linewidth for other circles
                    inner_circle_size=9         # size of inner circle
                    )

                # plot pizza
                fig, ax = baker.make_pizza(
                    values,                          # list of values
                        figsize=(8, 8.5),                # adjust figsize according to your need
                        color_blank_space="same",        # use same color to fill blank space
                        slice_colors=slice_colors,       # color for individual slices
                        value_colors=text_colors,        # color for the value-text
                        value_bck_colors=slice_colors,   # color for the blank spaces
                        blank_alpha=0.4,                 # alpha for blank-space colors
                        kwargs_slices=dict(
                            edgecolor="#F2F2F2", zorder=2, linewidth=1
                        ),                               # values to be used when plotting slices
                        kwargs_params=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, va="center"
                            ),                               # values to be used when adding parameter
                        kwargs_values=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            )                                # values to be used when adding parameter-values
                    )
                fig.set_dpi(600)
                
                player_name = grouped['Player Name']
                fig.set_facecolor('white')
                plt.gca().set_facecolor('white')
        elif group['Position'].iloc[0] == 'Wing':
            player_named = group['Player Name'].iloc[0]
            if (len(group['Position']) > 1) and (group['Position'] == 'Wing').all():
                wing_columns = ['Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Total Passes Percentile', 'Pass Completion Percentile', 
                'Pass into Oppo Box Percentile', 'Forward Completion Percentile', 'Dribble Percentile', 'Att 1v1 Percentile', 
                'Loss of Poss Percentile', 'Efforts on Goal Percentile', 'Shot on Target Percentile']
                wing_columns_wout = [col.replace(' Percentile', '') for col in wing_columns]
                group = group.fillna(0)
                params = list(wing_columns_wout)
                row_2024 = group[group['Date'] == '2024']
                row_2023 = group[group['Date'] == '2023']
                values = [int(row_2024[col]) for col in wing_columns]
                other_vals = [int(row_2023[col]) for col in wing_columns]

                params_offset = [True] * len(params)
                
                # color for the slices and text
                slice_colors = []
                slice_colors_bck = ["#6bb2e2"] * len(params)  # Use light blue for all slices
                text_colors =  ["#F2F2F2"] * len(params)
                text_colors_bck =  []
                compare_colors_bck = []
                
                compare_val_colors = len(values)*['#F2F2F2']
            
                compare_colors = []
                for spring_val, dec_val, color in zip(values, other_vals, slice_colors_bck):
                    if dec_val > spring_val:
                        compare_colors.append('red')
                        slice_colors.append(color)
                        text_colors_bck.append('red')
                        compare_colors_bck.append('red')
                    elif dec_val == spring_val:
                        compare_colors.append('orange')
                        slice_colors.append(color)
                        text_colors_bck.append('orange')
                        compare_colors_bck.append('orange')
                    elif dec_val < spring_val:
                        compare_colors.append('green')
                        slice_colors.append(color)
                        text_colors_bck.append('green')
                        compare_colors_bck.append('green')
            
                # instantiate PyPizza class
                baker = PyPizza(
                    params=params,                  # list of parameters
                    background_color="white",     # background color
                    straight_line_color="#EBEBE9",  # color for straight lines
                    straight_line_lw=1,             # linewidth for straight lines
                    last_circle_lw=0,               # linewidth of last circle
                    other_circle_lw=0,              # linewidth for other circles
                    inner_circle_size=9         # size of inner circle
                    )

                # plot pizza
                fig, ax = baker.make_pizza(
                    other_vals,     
                    compare_values=values,                     # list of values
                        figsize=(8, 8.5),                # adjust figsize according to your need
                        color_blank_space="same",        # use same color to fill blank space
                        slice_colors=slice_colors,       # color for individual slices
                        value_colors=text_colors,        # color for the value-text
                        value_bck_colors=slice_colors,   # color for the blank spaces
                        blank_alpha=0.4,                 # alpha for blank-space colors
                        compare_colors = slice_colors,
                        compare_value_colors = compare_val_colors,
                        compare_value_bck_colors = compare_colors_bck,
                        kwargs_slices=dict(
                            edgecolor="#F2F2F2", zorder=2, linewidth=1
                            ),                               # values to be used when plotting slices
                        kwargs_compare=dict(
                            edgecolor='#F2F2F2', zorder=3, linewidth=2
                            ), 
                        kwargs_params=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, va="center"
                            ),                               # values to be used when adding parameter
                        kwargs_values=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            ),
                        kwargs_compare_values=dict(
                            color='#F2F2F2', fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            )
                    # values to be used when adding parameter-values
                    )

                baker.adjust_texts(params_offset, offset=-0.2, adj_comp_values=True)
                
                fig.set_dpi(600)
            
                fig.set_facecolor('white')
                plt.gca().set_facecolor('white')
            else:
                wing_columns = ['Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Total Passes Percentile', 'Pass Completion Percentile', 
                    'Pass into Oppo Box Percentile', 'Forward Completion Percentile', 'Dribble Percentile', 'Att 1v1 Percentile', 
                    'Loss of Poss Percentile', 'Efforts on Goal Percentile', 'Shot on Target Percentile']
                wing_columns_wout = [col.replace(' Percentile', '') for col in wing_columns]
                wing_filtered = group[wing_columns]
                for index, row in group.iterrows():
                    if row['Date'] == '2024':
                        group = row
                        found_2024 = True
                        break
                if not found_2024:
                    group = group.head(1)
                params = list(wing_columns_wout)
                values = [int(group[col]) for col in wing_columns]

                # color for the slices and text
                slice_colors_bck = ["#6bb2e2"] * len(params)  # Use light blue for all slices 
                text_colors =  ["#000000"] * 2 + ["#000000"] * 4 + ["#F2F2F2"] * 3 + ['#F2F2F2'] * 2
            
                # instantiate PyPizza class
                baker = PyPizza(
                    params=params,                  # list of parameters
                    background_color="white",     # background color
                    straight_line_color="#EBEBE9",  # color for straight lines
                    straight_line_lw=1,             # linewidth for straight lines
                    last_circle_lw=0,               # linewidth of last circle
                    other_circle_lw=0,              # linewidth for other circles
                    inner_circle_size=9         # size of inner circle
                    )

                # plot pizza
                fig, ax = baker.make_pizza(
                    values,                          # list of values
                        figsize=(8, 8.5),                # adjust figsize according to your need
                        color_blank_space="same",        # use same color to fill blank space
                        slice_colors=slice_colors,       # color for individual slices
                        value_colors=text_colors,        # color for the value-text
                        value_bck_colors=slice_colors,   # color for the blank spaces
                        blank_alpha=0.4,                 # alpha for blank-space colors
                        kwargs_slices=dict(
                            edgecolor="#F2F2F2", zorder=2, linewidth=1
                        ),                               # values to be used when plotting slices
                        kwargs_params=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, va="center"
                            ),                               # values to be used when adding parameter
                        kwargs_values=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            )                                # values to be used when adding parameter-values
                    )
                fig.set_dpi(600)
                
        elif group['Position'].iloc[0] == 'CM':
            player_named = group['Player Name'].iloc[0]
            if (len(group['Position']) > 1) and (group['Position'] == 'CM').all():
                cm_columns = ['Dribble Percentile', 'Loss of Poss Percentile', 'Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Progr Regain Percentile',
                    'Total Passes Percentile', 'Pass Completion Percentile', 'Forward Total Percentile', 'Forward Completion Percentile',
                    'Line Break Percentile', 'Pass into Oppo Box Percentile', 'Efforts on Goal Percentile']
                cm_columns_wout = [col.replace(' Percentile', '') for col in cm_columns]
                group = group.fillna(0)
                params = list(cm_columns_wout)
                row_2024 = group[group['Date'] == '2024']
                row_2023 = group[group['Date'] == '2023']
                values = [int(row_2024[col]) for col in cm_columns]
                other_vals = [int(row_2023[col]) for col in cm_columns]

                params_offset = [True] * len(params)
                
                # color for the slices and text
                slice_colors = []
                slice_colors_bck = ["#6bb2e2"] * len(params)  # Use light blue for all slices
                text_colors =  ["#F2F2F2"] * len(params)
                text_colors_bck =  []
                compare_colors_bck = []
                
                compare_val_colors = len(values)*['#F2F2F2']
            
                compare_colors = []
                for spring_val, dec_val, color in zip(values, other_vals, slice_colors_bck):
                    if dec_val > spring_val:
                        compare_colors.append('red')
                        slice_colors.append(color)
                        text_colors_bck.append('red')
                        compare_colors_bck.append('red')
                    elif dec_val == spring_val:
                        compare_colors.append('orange')
                        slice_colors.append(color)
                        text_colors_bck.append('orange')
                        compare_colors_bck.append('orange')
                    elif dec_val < spring_val:
                        compare_colors.append('green')
                        slice_colors.append(color)
                        text_colors_bck.append('green')
                        compare_colors_bck.append('green')
            
                # instantiate PyPizza class
                baker = PyPizza(
                    params=params,                  # list of parameters
                    background_color="white",     # background color
                    straight_line_color="#EBEBE9",  # color for straight lines
                    straight_line_lw=1,             # linewidth for straight lines
                    last_circle_lw=0,               # linewidth of last circle
                    other_circle_lw=0,              # linewidth for other circles
                    inner_circle_size=9         # size of inner circle
                    )

                # plot pizza
                fig, ax = baker.make_pizza(
                    other_vals,     
                    compare_values=values,                     # list of values
                        figsize=(8, 8.5),                # adjust figsize according to your need
                        color_blank_space="same",        # use same color to fill blank space
                        slice_colors=slice_colors,       # color for individual slices
                        value_colors=text_colors,        # color for the value-text
                        value_bck_colors=slice_colors,   # color for the blank spaces
                        blank_alpha=0.4,                 # alpha for blank-space colors
                        compare_colors = slice_colors,
                        compare_value_colors = compare_val_colors,
                        compare_value_bck_colors = compare_colors_bck,
                        kwargs_slices=dict(
                            edgecolor="#F2F2F2", zorder=2, linewidth=1
                            ),                               # values to be used when plotting slices
                        kwargs_compare=dict(
                            edgecolor='#F2F2F2', zorder=3, linewidth=2
                            ), 
                        kwargs_params=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, va="center"
                            ),                               # values to be used when adding parameter
                        kwargs_values=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            ),
                        kwargs_compare_values=dict(
                            color='#F2F2F2', fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            )
                    # values to be used when adding parameter-values
                    )

                baker.adjust_texts(params_offset, offset=-0.2, adj_comp_values=True)
                
                fig.set_dpi(600)
            
                fig.set_facecolor('white')
                plt.gca().set_facecolor('white')
                
            else:
                cm_columns = ['Dribble Percentile', 'Loss of Poss Percentile', 'Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Progr Regain Percentile',
                    'Total Passes Percentile', 'Pass Completion Percentile', 'Forward Total Percentile', 'Forward Completion Percentile',
                    'Line Break Percentile', 'Pass into Oppo Box Percentile', 'Efforts on Goal Percentile']
                cm_columns_wout = [col.replace(' Percentile', '') for col in cm_columns]
                for index, row in group.iterrows():
                    if row['Date'] == '2024':
                        group = row
                        found_2024 = True
                        break
                if not found_2024:
                    group = group.head(1)
                group = group.fillna(0)
                params = list(cm_columns_wout)
                values = [int(group[col]) for col in cm_columns]

                # color for the slices and text
                slice_colors_bck = ["#6bb2e2"] * len(params)  # Use light blue for all slices
                text_colors =  ["#000000"] * 2 + ["#000000"] * 3 + ["#F2F2F2"] * 4 + ['#F2F2F2'] * 3
            
                # instantiate PyPizza class
                baker = PyPizza(
                    params=params,                  # list of parameters
                    background_color="white",     # background color
                    straight_line_color="#EBEBE9",  # color for straight lines
                    straight_line_lw=1,             # linewidth for straight lines
                    last_circle_lw=0,               # linewidth of last circle
                    other_circle_lw=0,              # linewidth for other circles
                    inner_circle_size=9         # size of inner circle
                    )

                # plot pizza
                fig, ax = baker.make_pizza(
                    values,                          # list of values
                        figsize=(8, 8.5),                # adjust figsize according to your need
                        color_blank_space="same",        # use same color to fill blank space
                        slice_colors=slice_colors,       # color for individual slices
                        value_colors=text_colors,        # color for the value-text
                        value_bck_colors=slice_colors,   # color for the blank spaces
                        blank_alpha=0.4,                 # alpha for blank-space colors
                        kwargs_slices=dict(
                            edgecolor="#F2F2F2", zorder=2, linewidth=1
                        ),                               # values to be used when plotting slices
                        kwargs_params=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, va="center"
                            ),                               # values to be used when adding parameter
                        kwargs_values=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            )                                # values to be used when adding parameter-values
                    )
                fig.set_dpi(600)
            
        elif group['Position'].iloc[0] == 'DM':
            player_named = group['Player Name'].iloc[0]
            if (len(group['Position']) > 1) and (group['Position'] == 'DM').all():
                cdm_columns = ['Total Passes Percentile', 'Forward Total Percentile', 'Pass Completion Percentile', 'Forward Completion Percentile',
                                'Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Progr Regain Percentile', 'Stand. Tackle Success Percentile',
                                'Dribble Percentile', 'Loss of Poss Percentile', 'Line Break Percentile']
                cdm_columns_wout = [col.replace(' Percentile', '') for col in cdm_columns]
                group = group.fillna(0)
                params = list(cdm_columns_wout)
                row_2024 = group[group['Date'] == '2024']
                row_2023 = group[group['Date'] == '2023']
                values = [int(row_2024[col]) for col in cdm_columns]
                other_vals = [int(row_2023[col]) for col in cdm_columns]

                params_offset = [True] * len(params)
                
                # color for the slices and text
                slice_colors = []
                slice_colors_bck = ["#6bb2e2"] * len(params)  # Use light blue for all slices
                text_colors =  ["#F2F2F2"] * len(params)
                text_colors_bck =  []
                compare_colors_bck = []
                
                compare_val_colors = len(values)*['#F2F2F2']
            
                compare_colors = []
                for spring_val, dec_val, color in zip(values, other_vals, slice_colors_bck):
                    if dec_val > spring_val:
                        compare_colors.append('red')
                        slice_colors.append(color)
                        text_colors_bck.append('red')
                        compare_colors_bck.append('red')
                    elif dec_val == spring_val:
                        compare_colors.append('orange')
                        slice_colors.append(color)
                        text_colors_bck.append('orange')
                        compare_colors_bck.append('orange')
                    elif dec_val < spring_val:
                        compare_colors.append('green')
                        slice_colors.append(color)
                        text_colors_bck.append('green')
                        compare_colors_bck.append('green')
            
                # instantiate PyPizza class
                baker = PyPizza(
                    params=params,                  # list of parameters
                    background_color="white",     # background color
                    straight_line_color="#EBEBE9",  # color for straight lines
                    straight_line_lw=1,             # linewidth for straight lines
                    last_circle_lw=0,               # linewidth of last circle
                    other_circle_lw=0,              # linewidth for other circles
                    inner_circle_size=9         # size of inner circle
                    )

                # plot pizza
                fig, ax = baker.make_pizza(
                    other_vals,     
                    compare_values=values,                     # list of values
                        figsize=(8, 8.5),                # adjust figsize according to your need
                        color_blank_space="same",        # use same color to fill blank space
                        slice_colors=slice_colors,       # color for individual slices
                        value_colors=text_colors,        # color for the value-text
                        value_bck_colors=slice_colors,   # color for the blank spaces
                        blank_alpha=0.4,                 # alpha for blank-space colors
                        compare_colors = slice_colors,
                        compare_value_colors = compare_val_colors,
                        compare_value_bck_colors = compare_colors_bck,
                        kwargs_slices=dict(
                            edgecolor="#F2F2F2", zorder=2, linewidth=1
                            ),                               # values to be used when plotting slices
                        kwargs_compare=dict(
                            edgecolor='#F2F2F2', zorder=3, linewidth=2
                            ), 
                        kwargs_params=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, va="center"
                            ),                               # values to be used when adding parameter
                        kwargs_values=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            ),
                        kwargs_compare_values=dict(
                            color='#F2F2F2', fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            )
                    # values to be used when adding parameter-values
                    )

                baker.adjust_texts(params_offset, offset=-0.2, adj_comp_values=True)
                
                fig.set_dpi(600)
            
                fig.set_facecolor('white')
                plt.gca().set_facecolor('white')
        
            else:
                cdm_columns = ['Total Passes Percentile', 'Forward Total Percentile', 'Pass Completion Percentile', 'Forward Completion Percentile',
                                'Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Progr Regain Percentile', 'Stand. Tackle Success Percentile',
                                'Dribble Percentile', 'Loss of Poss Percentile', 'Line Break Percentile']
                cdm_columns_wout = [col.replace(' Percentile', '') for col in cdm_columns]
                for index, row in group.iterrows():
                    if row['Date'] == '2024':
                        group = row
                        found_2024 = True
                        break
                if not found_2024:
                    group = group.head(1)
                group = group.fillna(0)
                params = list(cdm_columns_wout)
                values = [int(group[col]) for col in cdm_columns]

                # color for the slices and text
                slice_colors_bck = ["#6bb2e2"] * len(params)  # Use light blue for all slices
                text_colors =  ["#000000"] * 4 + ["#000000"] * 4 + ['#F2F2F2'] * 3

                    # instantiate PyPizza class
                baker = PyPizza(
                        params=params,                  # list of parameters
                        background_color="white",     # background color
                        straight_line_color="#EBEBE9",  # color for straight lines
                        straight_line_lw=1,             # linewidth for straight lines
                        last_circle_lw=0,               # linewidth of last circle
                        other_circle_lw=0,              # linewidth for other circles
                        inner_circle_size=9         # size of inner circle
                        )

                    # plot pizza
                fig, ax = baker.make_pizza(
                        values,                          # list of values
                            figsize=(8, 8.5),                # adjust figsize according to your need
                            color_blank_space="same",        # use same color to fill blank space
                            slice_colors=slice_colors,       # color for individual slices
                            value_colors=text_colors,        # color for the value-text
                            value_bck_colors=slice_colors,   # color for the blank spaces
                            blank_alpha=0.4,                 # alpha for blank-space colors
                            kwargs_slices=dict(
                                edgecolor="#F2F2F2", zorder=2, linewidth=1
                            ),                               # values to be used when plotting slices
                            kwargs_params=dict(
                                color="#000000", fontsize=13,
                                fontproperties=font_normal, va="center"
                                ),                               # values to be used when adding parameter
                            kwargs_values=dict(
                                color="#000000", fontsize=13,
                                fontproperties=font_normal, zorder=3,
                                bbox=dict(
                                    edgecolor="#000000", facecolor="cornflowerblue",
                                    boxstyle="round,pad=0.2", lw=1
                                    )
                                )                                # values to be used when adding parameter-values
                        )
                fig.set_dpi(600)
                    
        elif group['Position'].iloc[0] == 'CB':
            player_named = group['Player Name'].iloc[0]
            if (len(group['Position']) > 1) and (group['Position'] == 'CB').all():
                cb_columns = ['Rec Total Percentile', 'Progr Regain Percentile', 'Stand. Tackle Success',
                                'Forward Total Percentile', 'Passing Total Percentile', 'Pass Completion Percentile', 'Forward Completion Percentile', 'Line Break Percentile',
                                'Loss of Poss Percentile']
                cb_columns_wout = [col.replace(' Percentile', '') for col in cb_columns]
                group = group.fillna(0)
                params = list(cb_columns_wout)
                row_2024 = group[group['Date'] == '2024']
                row_2023 = group[group['Date'] == '2023']
                values = [int(row_2024[col]) for col in cb_columns]
                other_vals = [int(row_2023[col]) for col in cb_columns]

                params_offset = [True] * len(params)
                
                # color for the slices and text
                slice_colors = []
                slice_colors_bck = ["#6bb2e2"] * len(params)  # Use light blue for all slices
                text_colors =  ["#F2F2F2"] * len(params)
                text_colors_bck =  []
                compare_colors_bck = []
                
                compare_val_colors = len(values)*['#F2F2F2']
            
                compare_colors = []
                for spring_val, dec_val, color in zip(values, other_vals, slice_colors_bck):
                    if dec_val > spring_val:
                        compare_colors.append('red')
                        slice_colors.append(color)
                        text_colors_bck.append('red')
                        compare_colors_bck.append('red')
                    elif dec_val == spring_val:
                        compare_colors.append('orange')
                        slice_colors.append(color)
                        text_colors_bck.append('orange')
                        compare_colors_bck.append('orange')
                    elif dec_val < spring_val:
                        compare_colors.append('green')
                        slice_colors.append(color)
                        text_colors_bck.append('green')
                        compare_colors_bck.append('green')
            
                # instantiate PyPizza class
                baker = PyPizza(
                    params=params,                  # list of parameters
                    background_color="white",     # background color
                    straight_line_color="#EBEBE9",  # color for straight lines
                    straight_line_lw=1,             # linewidth for straight lines
                    last_circle_lw=0,               # linewidth of last circle
                    other_circle_lw=0,              # linewidth for other circles
                    inner_circle_size=9         # size of inner circle
                    )

                # plot pizza
                fig, ax = baker.make_pizza(
                    other_vals,     
                    compare_values=values,                     # list of values
                        figsize=(8, 8.5),                # adjust figsize according to your need
                        color_blank_space="same",        # use same color to fill blank space
                        slice_colors=slice_colors,       # color for individual slices
                        value_colors=text_colors,        # color for the value-text
                        value_bck_colors=slice_colors,   # color for the blank spaces
                        blank_alpha=0.4,                 # alpha for blank-space colors
                        compare_colors = slice_colors,
                        compare_value_colors = compare_val_colors,
                        compare_value_bck_colors = compare_colors_bck,
                        kwargs_slices=dict(
                            edgecolor="#F2F2F2", zorder=2, linewidth=1
                            ),                               # values to be used when plotting slices
                        kwargs_compare=dict(
                            edgecolor='#F2F2F2', zorder=3, linewidth=2
                            ), 
                        kwargs_params=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, va="center"
                            ),                               # values to be used when adding parameter
                        kwargs_values=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            ),
                        kwargs_compare_values=dict(
                            color='#F2F2F2', fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            )
                    # values to be used when adding parameter-values
                    )

                baker.adjust_texts(params_offset, offset=-0.2, adj_comp_values=True)
                
                fig.set_dpi(600)
            
                fig.set_facecolor('white')
                plt.gca().set_facecolor('white')
                    
            else:
                cb_columns = ['Rec Total Percentile', 'Progr Regain Percentile', 'Stand. Tackle Success',
                                'Forward Total Percentile', 'Passing Total Percentile', 'Pass Completion Percentile', 'Forward Completion Percentile', 'Line Break Percentile',
                                'Loss of Poss Percentile']
                cb_columns_wout = [col.replace(' Percentile', '') for col in cb_columns]
                found_2024=False
                for index, row in group.iterrows():
                    if row['Date'] == '2024':
                        group = row
                        found_2024 = True
                        break
                if not found_2024:
                    group = group.head(1)
                group = group.fillna(0)
                params = list(cb_columns_wout)
                values = [int(group[col]) for col in cb_columns]

                # color for the slices and text
                slice_colors_bck = ["#6bb2e2"] * len(params)  # Use light blue for all slices
                text_colors =  ["#000000"] * 3 + ["#000000"] * 4 + ["#F2F2F2"] * 2

                    # instantiate PyPizza class
                baker = PyPizza(
                        params=params,                  # list of parameters
                        background_color="white",     # background color
                        straight_line_color="#EBEBE9",  # color for straight lines
                        straight_line_lw=1,             # linewidth for straight lines
                        last_circle_lw=0,               # linewidth of last circle
                        other_circle_lw=0,              # linewidth for other circles
                        inner_circle_size=9         # size of inner circle
                        )

                    # plot pizza
                fig, ax = baker.make_pizza(
                        values,                          # list of values
                            figsize=(8, 8.5),                # adjust figsize according to your need
                            color_blank_space="same",        # use same color to fill blank space
                            slice_colors=slice_colors,       # color for individual slices
                            value_colors=text_colors,        # color for the value-text
                            value_bck_colors=slice_colors,   # color for the blank spaces
                            blank_alpha=0.4,                 # alpha for blank-space colors
                            kwargs_slices=dict(
                                edgecolor="#F2F2F2", zorder=2, linewidth=1
                            ),                               # values to be used when plotting slices
                            kwargs_params=dict(
                                color="#000000", fontsize=13,
                                fontproperties=font_normal, va="center"
                                ),                               # values to be used when adding parameter
                            kwargs_values=dict(
                                color="#000000", fontsize=13,
                                fontproperties=font_normal, zorder=3,
                                bbox=dict(
                                    edgecolor="#000000", facecolor="cornflowerblue",
                                    boxstyle="round,pad=0.2", lw=1
                                    )
                                )                                # values to be used when adding parameter-values
                        )
                fig.set_dpi(600)

        elif group['Position'].iloc[0] == 'FB':
            player_named = group['Player Name'].iloc[0]
            if (len(group['Position']) > 1) and (group['Position'] == 'FB').all():
                fb_columns = ['Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Progr Regain Percentile', 'Stand. Tackle Success Percentile',
                                'Forward Total Percentile', 'Total Passes Percentile', 'Pass Completion Percentile', 'Forward Completion Percentile', 
                                'Dribble Percentile', 'Loss of Poss Percentile', 'Line Break Percentile', 'Pass into Oppo Box Percentile']
                fb_columns_wout = [col.replace(' Percentile', '') for col in fb_columns]
                group = group.fillna(0)
                params = list(fb_columns_wout)
                row_2024 = group[group['Date'] == '2024']
                row_2023 = group[group['Date'] == '2023']
                values = [int(row_2024[col]) for col in fb_columns]
                other_vals = [int(row_2023[col]) for col in fb_columns]


                params_offset = [True] * len(params)
                
                # color for the slices and text
                slice_colors = []
                slice_colors_bck = ["#6bb2e2"] * len(params)  # Use light blue for all slices
                text_colors =  ["#F2F2F2"] * len(params)
                text_colors_bck =  []
                compare_colors_bck = []
                
                compare_val_colors = len(values)*['#F2F2F2']
            
                compare_colors = []
                for spring_val, dec_val, color in zip(values, other_vals, slice_colors_bck):
                    if dec_val > spring_val:
                        compare_colors.append('red')
                        slice_colors.append(color)
                        text_colors_bck.append('red')
                        compare_colors_bck.append('red')
                    elif dec_val == spring_val:
                        compare_colors.append('orange')
                        slice_colors.append(color)
                        text_colors_bck.append('orange')
                        compare_colors_bck.append('orange')
                    elif dec_val < spring_val:
                        compare_colors.append('green')
                        slice_colors.append(color)
                        text_colors_bck.append('green')
                        compare_colors_bck.append('green')
            
                # instantiate PyPizza class
                baker = PyPizza(
                    params=params,                  # list of parameters
                    background_color="white",     # background color
                    straight_line_color="#EBEBE9",  # color for straight lines
                    straight_line_lw=1,             # linewidth for straight lines
                    last_circle_lw=0,               # linewidth of last circle
                    other_circle_lw=0,              # linewidth for other circles
                    inner_circle_size=9         # size of inner circle
                    )

                # plot pizza
                fig, ax = baker.make_pizza(
                    other_vals,     
                    compare_values=values,                     # list of values
                        figsize=(8, 8.5),                # adjust figsize according to your need
                        color_blank_space="same",        # use same color to fill blank space
                        slice_colors=slice_colors,       # color for individual slices
                        value_colors=text_colors,        # color for the value-text
                        value_bck_colors=slice_colors,   # color for the blank spaces
                        blank_alpha=0.4,                 # alpha for blank-space colors
                        compare_colors = slice_colors,
                        compare_value_colors = compare_val_colors,
                        compare_value_bck_colors = compare_colors_bck,
                        kwargs_slices=dict(
                            edgecolor="#F2F2F2", zorder=2, linewidth=1
                            ),                               # values to be used when plotting slices
                        kwargs_compare=dict(
                            edgecolor='#F2F2F2', zorder=3, linewidth=2
                            ), 
                        kwargs_params=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, va="center"
                            ),                               # values to be used when adding parameter
                        kwargs_values=dict(
                            color="#000000", fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            ),
                        kwargs_compare_values=dict(
                            color='#F2F2F2', fontsize=13,
                            fontproperties=font_normal, zorder=3,
                            bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                                )
                            )
                    # values to be used when adding parameter-values
                    )

                baker.adjust_texts(params_offset, offset=-0.2, adj_comp_values=True)
                
                fig.set_dpi(600)
            
                fig.set_facecolor('white')
                plt.gca().set_facecolor('white')
                
            else:
                fb_columns = ['Stand. Tackle Total Percentile', 'Rec Total Percentile', 'Progr Regain Percentile', 'Stand. Tackle Success Percentile',
                                'Forward Total Percentile', 'Total Passes Percentile', 'Pass Completion Percentile', 'Forward Completion Percentile', 
                                'Dribble Percentile', 'Loss of Poss Percentile', 'Line Break Percentile', 'Pass into Oppo Box Percentile']
                fb_columns_wout = [col.replace(' Percentile', '') for col in fb_columns]
                for index, row in group.iterrows():
                    if row['Date'] == '2024':
                        group = row
                        found_2024 = True
                        break
                if not found_2024:
                    group = group.head(1)
                group = group.fillna(0)
                params = list(fb_columns_wout)
                values = [int(group[col]) for col in fb_columns]

                # color for the slices and text
                slice_colors_bck = ["#6bb2e2"] * len(params)  # Use light blue for all slices 
                text_colors =  ["#000000"] * 4 + ["#000000"] * 4 + ['#F2F2F2'] * 4

                    # instantiate PyPizza class
                baker = PyPizza(
                        params=params,                  # list of parameters
                        background_color="white",     # background color
                        straight_line_color="#EBEBE9",  # color for straight lines
                        straight_line_lw=1,             # linewidth for straight lines
                        last_circle_lw=0,               # linewidth of last circle
                        other_circle_lw=0,              # linewidth for other circles
                        inner_circle_size=9         # size of inner circle
                    )

                    # plot pizza
                fig, ax = baker.make_pizza(values,                          # list of values
                            figsize=(8, 8.5),                # adjust figsize according to your need
                            color_blank_space="same",        # use same color to fill blank space
                            slice_colors=slice_colors,       # color for individual slices
                            value_colors=text_colors,        # color for the value-text
                            value_bck_colors=slice_colors,   # color for the blank spaces
                            blank_alpha=0.4,                 # alpha for blank-space colors
                            kwargs_slices=dict(
                                edgecolor="#F2F2F2", zorder=2, linewidth=1
                            ),                               # values to be used when plotting slices
                            kwargs_params=dict(
                                color="#000000", fontsize=13,
                                fontproperties=font_normal, va="center"
                                ),                               # values to be used when adding parameter
                            kwargs_values=dict(
                                color="#000000", fontsize=13,
                                fontproperties=font_normal, zorder=3,
                                bbox=dict(
                                    edgecolor="#000000", facecolor="cornflowerblue",
                                    boxstyle="round,pad=0.2", lw=1
                                    )
                            )                                # values to be used when adding parameter-values
                        )
                fig.set_dpi(600)
                
    return fig
