import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors
import matplotlib.cm as cm  # Correct import for colormap utilities

from Classes import SonarData

def process_message(message):
    sonar = SonarData(**message['sonar']) if 'sonar' in message else None
    return sonar

def load_data_from_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    filename = "sonar_telemetry_data.json"
    data = load_data_from_json(filename)
    
    x_points = []
    y_points = []
    z_points = []

    z = 0
    z_jump = 1
    num = 10  # Assuming you are reading the first 15 messages for example

    outliers = 1 # 1: want outliers, 0: Do not want them

    for message in data[:num]:  # Limit to first num messages
        sonar = process_message(message)
        if sonar:
            # Prepare data, check if it's list or single value
            if isinstance(sonar.pointX, list):
                x_extend = sonar.pointX
                y_extend = sonar.pointY
                z_extend = [z] * len(sonar.pointX)
            else:
                x_extend = [sonar.pointX]
                y_extend = [sonar.pointY]
                z_extend = [z]
            
            # Append only those points where y is negative and greater than -0.5
            for x, y, z_val in zip(x_extend, y_extend, z_extend):
                if outliers:
                    x_points.append(x)
                    y_points.append(y)
                    z_points.append(z_val)
                if ~outliers:
                    if -0.5 < y < 0:
                        x_points.append(x)
                        y_points.append(y)
                        z_points.append(z_val)



            z += z_jump  # Increment z after processing all points from one message

    if y_points:
        # Normalize the color based on the y-values
        norm = mcolors.Normalize(vmin=min(y_points), vmax=max(y_points))
        cmap = plt.get_cmap('viridis')  # Using the correct colormap method
        colors = [cmap(norm(value)) for value in y_points]

        # Creating the 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(x_points, z_points, y_points, c=colors, cmap=cmap)
        
        # Color bar setup
        cbar = fig.colorbar(scatter, ax=ax, pad=0.1)
        cbar.set_label('Depth', fontsize=15)


        # Labeling
        ax.set_xlabel(r'$X_{S_0}$', fontsize=15)
        ax.set_ylabel('Scan number', fontsize=15)
        ax.set_zlabel(r'$Y_{S_1}$', fontsize=15)

        ax.set_title(f'{num} lines of MBES Measurements', fontsize=16)


        # ax.set_title(f'{num} lines of MBES Measurements: No outliers', fontsize=16)

        ax.tick_params(axis='both', which='major', labelsize=12)  # Enlarging the tick labels


        # Set the limits for the y-axis
        ax.set_zlim(-0.5, 0.4)

        plt.show()
    else:
        print("No data points available to plot. Check your data extraction.")





