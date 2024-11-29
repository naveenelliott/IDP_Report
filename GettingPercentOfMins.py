import matplotlib.pyplot as plt

def format_percentage(value):
    """Format a float value with consistent length: 100 as 100.0, others as two decimal places."""
    if value == 100:
        return '100.0%'  # Special case for 100
    return f'{value:.2f}%'  # Two decimal places for other numbers

def create_horizontal_bar_chart(title, percentage_played):
    # Create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 2))  # Consistent figure size
    ax.barh(
        0, percentage_played, color='lightblue', height=0.5, edgecolor='black', linewidth=2  # Add darker border
    )

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
    ax.set_title(title, fontsize=20, pad=10)

    # Remove x-axis ticks and numbers
    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Remove y-ticks and labels
    ax.set_yticks([])

    plt.subplots_adjust(left=0.2, right=0.8)  # Consistent layout adjustments
    plt.tight_layout(pad=1.0)  # Ensure consistent spacing
    return fig

def plottingMinsPlayed(player_name, percentage_played):
    return create_horizontal_bar_chart('% of Available Mins Played', percentage_played)

def plottingStarts(player_name, percentage_played):
    return create_horizontal_bar_chart('% of Available Starts', percentage_played)
