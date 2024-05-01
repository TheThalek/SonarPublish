import json
import matplotlib.pyplot as plt
import numpy as np  # For mathematical constants and operations
from matplotlib.ticker import FuncFormatter


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
    



def plot_data(data, attributes, title_suffix, total_duration):
    """
    Generic function to plot given telemetry data attributes.
    """
    if not data:
        print("No data to plot.")
        return
    
    num_plots = len(attributes) // 2
    fig, axs = plt.subplots(num_plots, 1, figsize=(10, 6 * num_plots))
    
    if num_plots == 1:
        axs = [axs]  # Make axs iterable if there's only one subplot
    
    timesteps = np.linspace(0, total_duration, len(data), endpoint=False)

    for i in range(num_plots):
        attr = attributes[i*2].split()
        raw_attr = attributes[i*2 + 1].split()
        
        # Ensure the key exists in the dictionary before trying to plot
        if attr[0] in data[0] and raw_attr[0] in data[0]:
            values = [entry[attr[0]][attr[1]] for entry in data if attr[0] in entry]
            raw_values = [entry[raw_attr[0]][raw_attr[1]] for entry in data if raw_attr[0] in entry]
            
            axs[i].plot(timesteps, values, label=f'{attr[1]} (Smoothed)', linestyle='-', color='blue')
            axs[i].plot(timesteps, raw_values, label=f'{raw_attr[1]} (Raw)', linestyle='--', color='red')
            axs[i].set_title(f"{attr[1]} and {raw_attr[1]} over Time {title_suffix}")
            axs[i].set_xlabel('Time (seconds)')
            axs[i].set_ylabel('Angle (Degrees)')
            axs[i].legend()
            axs[i].grid(True)
    
    plt.tight_layout()
    plt.show()



def format_func(value, tick_number):
    """
    Custom formatter for plotting degrees with a degree symbol.
    """
    return f"{value:.2f}°"




def plot_raw_data(data, total_duration):
    """
    Plots raw telemetry data for the first 200 data points after removing duplicates,
    organizing the plots within a single figure with increased text sizes and adjusted subplot spacing.
    """
    if not data:
        print("No data to plot.")
        return

    # Remove duplicate data points where all attributes are the same as the previous
    unique_data = []
    prev_entry = None
    for entry in data:
        if prev_entry is None or not all(entry.get(attr[0], {}).get(attr[1], None) == prev_entry.get(attr[0], {}).get(attr[1], None) 
                                         for attr in [('rawPose', 'rawRoll'), ('rawPose', 'rawPitch'), ('rawHeading', 'rawHeading')]):
            unique_data.append(entry)
        prev_entry = entry

    # Limit data to the first 200 unique entries
    unique_data = unique_data[:200]
    num_points = len(unique_data)

    attributes = [
        ('rawPose', 'rawRoll'),
        ('rawPose', 'rawPitch'),
        ('rawHeading', 'rawHeading')  # Assuming 'rawYaw' data is actually under 'rawHeading'
    ]

    # Create a single figure for all subplots
    fig, axs = plt.subplots(len(attributes), 1, figsize=(10, 15))
    fig.suptitle('Orientation for the First 200 Measurements', fontsize=24)

    for i, (component, measure) in enumerate(attributes):
        if component in unique_data[0] and measure in unique_data[0][component]:
            values = [entry[component][measure] for entry in unique_data if component in entry and measure in entry[component]]
            axs[i].plot(values, marker='x', linestyle='-', color='blue', label=f'{measure}')
            axs[i].set_xlabel('Measurement Number', fontsize=18)
            axs[i].set_ylabel(f'{measure} (Degrees)', fontsize=18)
            axs[i].legend(fontsize=14)
            axs[i].grid(True)
            axs[i].set_xticks(np.arange(0, num_points, step=20))
            min_val, max_val = np.min(values), np.max(values)
            step = np.ptp(values) / 5  # Compute step as one fifth of the peak-to-peak range
            step = max(round(step, -int(np.floor(np.log10(abs(step))))), 0.1)  # Round step to significant figure
            y_ticks = np.arange(start=np.floor(min_val/step)*step, stop=np.ceil(max_val/step)*step + step, step=step)
            axs[i].set_yticks(y_ticks)  # Set y-ticks dynamically based on data range
            axs[i].tick_params(axis='both', which='major', labelsize=14)

    # Adjust layout to make more space between the subplots
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.subplots_adjust(hspace=0.3)  # Increase horizontal space

    plt.show()



def plot_combined_data(data, total_duration):
    """
    Plots combined "smoothed" and raw telemetry data.
    """
    attributes = [
        'pose roll', 'rawPose rawRoll',
        'pose pitch', 'rawPose rawPitch',
        'heading heading', 'rawHeading rawHeading'
    ]
    plot_data(data, attributes, "(Combined Data)", total_duration)



if __name__ == "__main__":
    filename = "pose_and_rawPose_data_Nyhavna2min.json"
    total_duration = 120  # Adjust based on your data

    # filename = "pose_and_rawPose_data_Airplane100sek.json"
    # total_duration = 100  # Adjust based on your data

    # filename = "pose_and_rawPose_data_Airplane30sek_HavingFixedPosesInPublisherByAddingOnPiAndRemovingAfterinterpolation.json"
    # total_duration = 30  # Adjust based on your data

    # filename = "pose_and_rawPose_data.json"
    # total_duration = 50  # Adjust based on your data

    data = read_data(filename)

    # Uncomment the function you wish to use
    plot_raw_data(data, total_duration)
    # plot_combined_data(data, total_duration)  # This should plot both interpolated/smoothed data and raw data

