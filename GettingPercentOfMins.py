import matplotlib.pyplot as plt

def plottingMinsPlayed(player_name, percentage_played):
    # Create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 2))  # Consistent figure size
    ax.barh([player_name], [percentage_played], color='lightblue', height=0.5)  # Fixed bar height

    # Set fixed x-axis range to ensure consistent bar scaling
    ax.set_xlim(0, 100)

    # Add text label consistently outside the bar, dynamically positioned
    for index, value in enumerate([percentage_played]):
        ax.text(
            value + 2 if value < 98 else value - 2,  # Adjust position based on value
            index, 
            f'{value:.2f}%', 
            va='center', 
            fontsize=20, 
            color='black'
        )

    # Add title
    ax.set_title('% of Mins Played', fontsize=25)

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

    # Add text label consistently outside the bar, dynamically positioned
    for index, value in enumerate([percentage_played]):
        ax.text(
            value + 2 if value < 98 else value - 2,  # Adjust position based on value
            index, 
            f'{value:.2f}%', 
            va='center', 
            fontsize=20, 
            color='black'
        )

    # Add title
    ax.set_title('% of Starts', fontsize=25)

    # Hide unnecessary axes
    ax.xaxis.set_ticks([])  # Hide x-axis ticks
    ax.yaxis.set_ticks([])  # Hide y-axis ticks

    plt.tight_layout()
    return fig
