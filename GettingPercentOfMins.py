import matplotlib.pyplot as plt

def format_percentage(value):
    """Format a float value with consistent length: 100 as 100.0, others as two decimal places."""
    if value == 100:
        return '100.0'  # Special case for 100
    return f'{value:.2f}'  # Two decimal places for other numbers

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
        format_percentage(percentage_played),  # Display formatted percentage
        va='center',  # Centered text vertically
        ha='left',  # Align text to the left
        fontsize=20,
        color='black'
    )

    # Add title
    ax.set_title('% of Available Mins Played', fontsize=30)

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
        format_percentage(percentage_played),  # Display formatted percentage
        va='center',  # Centered text vertically
        ha='left',  # Align text to the left
        fontsize=20,
        color='black'
    )

    # Add title
    ax.set_title('% of Available Starts', fontsize=30)

    # Hide unnecessary axes
    ax.xaxis.set_ticks([])  # Hide x-axis ticks
    ax.yaxis.set_ticks([])  # Hide y-axis ticks

    plt.tight_layout()
    return fig
