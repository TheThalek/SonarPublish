import json
import matplotlib.pyplot as plt
import numpy as np  # For mathematical constants and operations

def read_data(filename):
    """
    Reads JSON data from a file.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def plot_telemetry(data, filename, total_duration):
    """
    Plots roll, pitch, and heading data from the telemetry data.
    Adds filename to the plot, standardizes colors and legends, and uses seconds for x-axis.
    """
    if not data:
        print("No data to plot.")
        return

    # Scaling factor for size increase
    scale_factor = 1.2

    # Calculate updated sizes
    figsize = (10 * scale_factor, 10 * scale_factor)
    fontsize_title = 15.5 * scale_factor
    fontsize_label = 14 * scale_factor
    fontsize_legend = 12 * scale_factor
    major_grid_alpha = 0.3
    major_grid_color = '#DDDDDD'
    degree_line_width = 1.5 * scale_factor
    degree_line_color = '#888888'

    # Initialize lists for the data
    roll = []
    pitch = []
    heading = []
    # Create a time array up to the total duration (assuming data is at 1Hz for simplicity)
    timesteps = np.linspace(0, total_duration, len(data), endpoint=False)

    # Extract data
    for entry in data:
        if "pose" in entry:
            roll.append(entry["pose"]["roll"])
            pitch.append(entry["pose"]["pitch"])
        if "heading" in entry:
            heading.append(entry["heading"]["heading"])

    # Plotting
    plt.figure(figsize=figsize)

    # Roll subplot
    plt.subplot(3, 1, 1)
    plt.plot(timesteps, roll, label='Roll', color='red', linestyle='-')
    plt.axhline(y=180, color=degree_line_color, linestyle='--', linewidth=degree_line_width)
    plt.axhline(y=-180, color=degree_line_color, linestyle='--', linewidth=degree_line_width)
    plt.axhline(y=0, color=degree_line_color, linestyle='--', linewidth=degree_line_width)
    plt.title('Roll over Time', fontsize=fontsize_title)
    plt.xlabel('Time (seconds)', fontsize=fontsize_label, color='gray')
    plt.ylabel('Angle (Degrees)', fontsize=fontsize_label, color='gray')
    plt.legend(loc='upper left', fontsize=fontsize_legend)
    plt.grid(True, alpha=major_grid_alpha, color=major_grid_color)
    plt.ylim(-200, 200)
    plt.tick_params(axis='both', which='major', labelsize=fontsize_label)

    # Pitch subplot
    plt.subplot(3, 1, 2)
    plt.plot(timesteps, pitch, label='Pitch', color='green', linestyle='-')
    plt.axhline(y=180, color=degree_line_color, linestyle='--', linewidth=degree_line_width)
    plt.axhline(y=-180, color=degree_line_color, linestyle='--', linewidth=degree_line_width)
    plt.axhline(y=0, color=degree_line_color, linestyle='--', linewidth=degree_line_width)
    plt.title('Pitch over Time', fontsize=fontsize_title)
    plt.xlabel('Time (seconds)', fontsize=fontsize_label, color='gray')
    plt.ylabel('Angle (Degrees)', fontsize=fontsize_label, color='gray')
    plt.legend(loc='upper left', fontsize=fontsize_legend)
    plt.grid(True, alpha=major_grid_alpha, color=major_grid_color)
    plt.ylim(-200, 200)
    plt.tick_params(axis='both', which='major', labelsize=fontsize_label)

    # Heading subplot
    plt.subplot(3, 1, 3)
    plt.plot(timesteps, heading, label='Heading', color='blue', linestyle='-')
    plt.axhline(y=180, color=degree_line_color, linestyle='--', linewidth=degree_line_width)
    plt.axhline(y=-180, color=degree_line_color, linestyle='--', linewidth=degree_line_width)
    plt.axhline(y=0, color=degree_line_color, linestyle='--', linewidth=degree_line_width)
    plt.title('Heading over Time', fontsize=fontsize_title)
    plt.xlabel('Time (seconds)', fontsize=fontsize_label, color='gray')
    plt.ylabel('Angle (Degrees)', fontsize=fontsize_label, color='gray')
    plt.legend(loc='upper left', fontsize=fontsize_legend)
    plt.grid(True, alpha=major_grid_alpha, color=major_grid_color)
    plt.ylim(-200, 200)
    plt.tick_params(axis='both', which='major', labelsize=fontsize_label)

    # Adding a title for the entire plot
    # plt.suptitle('Pose values from the first 43 seconds of the Nyhavna data', fontsize=20 * scale_factor, x=0.53)
    # plt.suptitle('Pose values from the first 118 seconds of the Airplane data', fontsize=20 * scale_factor, x=0.53)
    plt.suptitle('Pose values from the first 43 seconds of the Nyhavna data', fontsize=20, x=0.53)


    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
   # filename = "pose_data_Airplane118sek.json"
    # total_duration = 118
    filename = "pose_data_Nyhavna43sek.json"
    total_duration = 43
    data = read_data(filename)
    plot_telemetry(data, filename, total_duration)
