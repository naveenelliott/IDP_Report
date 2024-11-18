import matplotlib.pyplot as plt

def plottingMinsPlayed(player_name, percentage_played):
    # Create a horizontal bar chart with fixed bar height
    fig, ax = plt.subplots(figsize=(10, 2))  # Consistent figure size
    ax.barh([player_name], [percentage_played], color='lightblue', height=0.4)  # Fixed bar height

    # Add title
    ax.set_title('% of Mins Played', fontsize=20)  # Consistent title font size
    ax.set_xlim(0, 100)  # Fixed x-axis range for consistent scaling

    # Add text label consistently outside the bar
    for index, value in enumerate([percentage_played]):
        # Use formatted string to ensure fixed alignment
        ax.text(105, index, f'{value:>6.2f}%', va='center', fontsize=15)  # Consistent alignment outside the bar

    # Hide unnecessary axes ticks
    ax.xaxis.set_ticks([])  # Hide x-axis ticks
    ax.yaxis.set_ticks([])  # Hide y-axis ticks

    plt.tight_layout()  # Optimize layout
    return fig


def plottingStarts(player_name, percentage_played):
    # Create a horizontal bar chart with fixed bar height
    fig, ax = plt.subplots(figsize=(10, 2))  # Consistent figure size
    ax.barh([player_name], [percentage_played], color='lightblue', height=0.4)  # Fixed bar height

    # Add title
    ax.set_title('% of Starts', fontsize=20)  # Consistent title font size
    ax.set_xlim(0, 100)  # Fixed x-axis range for consistent scaling

    # Add text label consistently outside the bar
    for index, value in enumerate([percentage_played]):
        # Use formatted string to ensure fixed alignment
        ax.text(105, index, f'{value:>6.2f}%', va='center', fontsize=15)  # Consistent alignment outside the bar

    # Hide unnecessary axes ticks
    ax.xaxis.set_ticks([])  # Hide x-axis ticks
    ax.yaxis.set_ticks([])  # Hide y-axis ticks

    plt.tight_layout()  # Optimize layout
    return fig
