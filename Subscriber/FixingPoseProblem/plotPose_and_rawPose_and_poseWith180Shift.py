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



def plot_raw_data(data, total_duration):
    """
    Plots raw telemetry data.
    """
    attributes = ['rawPose rawRoll', 'rawPose rawPitch', 'rawHeading rawHeading']
    plot_data(data, attributes, "(RawData)", total_duration)


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


def plot_corrected_and_combined_data(data, total_duration):
    """
    Corrects jumps in smoothed data around ±180 degrees and plots corrected data
    alongside original smoothed and raw telemetry data.
    """
    if not data:
        print("No data to plot.")
        return
    
    attributes = [
        'pose roll', 'rawPose rawRoll',
        'pose pitch', 'rawPose rawPitch',
        'heading heading', 'rawHeading rawHeading'
    ]
    num_plots = len(attributes) // 2
    fig, axs = plt.subplots(num_plots, 1, figsize=(10, 6 * num_plots))
    
    if num_plots == 1:
        axs = [axs]
    
    timesteps = np.linspace(0, total_duration, len(data), endpoint=False)

    for i in range(num_plots):
        attr = attributes[i*2].split()
        raw_attr = attributes[i*2 + 1].split()
        
        if attr[0] in data[0] and raw_attr[0] in data[0]:
            values = np.array([entry[attr[0]][attr[1]] for entry in data if attr[0] in entry])
            raw_values = np.array([entry[raw_attr[0]][raw_attr[1]] for entry in data if raw_attr[0] in entry])
            
            # Correcting the smoothed data for jumps
            corrected_values = np.copy(values)
            for j in range(1, len(values)):
                diff = corrected_values[j] - corrected_values[j-1]
                if abs(diff) > 170 and abs(diff) < 190:  # Adjust this threshold as needed
                    corrected_values[j:] += -np.sign(diff) * 180
            
            axs[i].plot(timesteps, values, label='Smoothed', linestyle='-', color='blue')
            axs[i].plot(timesteps, corrected_values, label='Corrected Smoothed', linestyle='-', color='green')
            axs[i].plot(timesteps, raw_values, label='Raw', linestyle='--', color='red')
            axs[i].set_title(f"{attr[1]} and {raw_attr[1]} over Time (Corrected Data)")
            axs[i].set_xlabel('Time (seconds)')
            axs[i].set_ylabel('Angle (Degrees)')
            axs[i].legend()
            axs[i].grid(True)
    
    plt.tight_layout()
    plt.show()




if __name__ == "__main__":
    filename = "pose_and_rawPose_data_Nyhavna2min.json"
    total_duration = 120  # Adjust based on your data
    data = read_data(filename)

    # Uncomment the function you wish to use
    # plot_raw_data(data, total_duration)
    # plot_combined_data(data, total_duration)  # This should plot both interpolated/smoothed data and raw data

    plot_corrected_and_combined_data(data, total_duration) #