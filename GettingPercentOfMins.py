import matplotlib.pyplot as plt

def plottingMinsPlayed(player_name, percentage_played):
    # Create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 2))  # Consistent figure size
    ax.barh([player_name], [percentage_played], color='lightblue', height=0.5)  # Fixed bar height

    # Set fixed x-axis range to ensure consistent bar scaling
    ax.set_xlim(0, 100)

    # Add text label outside the bar at the same horizontal position
    ax.text(
        105,  # Fixed position outside the bar
        0,  # Vertical alignment (same for all bars)
        f'{percentage_played:.2f}%',  # Display the percentage
        va='center',  # Centered text vertically
        ha='left',  # Align text to the left
        fontsize=12,
        color='black'
    )

    # Add title
    ax.set_title('% of Minutes Played', fontsize=16)

    # Hide unnecessary axes
    ax.xaxis.set_ticks([])  # Hide x-axis ticks
    ax.yaxis.set_ticks([])  # Hide y-axis ticks

    plt.tight_layout()
    return fig


def plottingStarts(player_name, percentage_played):
    # Create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 2))  # Consistent figure size
    ax.barh([player_name], [percentage_played], color='lightblue', height=0.5)  # Fixed bar height

    # Set fixed x-axis range to ensure consistent bar scaling
    ax.set_xlim(0, 100)

    # Add text label outside the bar at the same horizontal position
    ax.text(
        105,  # Fixed position outside the bar
        0,  # Vertical alignment (same for all bars)
        f'{percentage_played:.2f}%',  # Display the percentage
        va='center',  # Centered text vertically
        ha='left',  # Align text to the left
        fontsize=12,
        color='black'
    )

    # Add title
    ax.set_title('% of Starts', fontsize=16)

    # Hide unnecessary axes
    ax.xaxis.set_ticks([])  # Hide x-axis ticks
    ax.yaxis.set_ticks([])  # Hide y-axis ticks

    plt.tight_layout()
    return fig
