import numpy as np

# Initialize x_value outside the function to persist its value between calls
x_value = 0

def generate_point_cloud(num_points=255, x_increment=0.1):
    global x_value

    # Ensure x_values has exactly num_points elements
    stop_x_value = x_value + (num_points - 1) * x_increment
    x_values = np.linspace(start=x_value, stop=stop_x_value, num=num_points)
    
    # Update x_value for the next set of points
    x_value = stop_x_value + x_increment

    y_values = np.random.uniform(-50, 50, num_points)
    z_values = np.random.uniform(0, 5, num_points)

    return np.stack((x_values, y_values, z_values), axis=-1)
