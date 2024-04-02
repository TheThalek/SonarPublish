import json
import matplotlib.pyplot as plt

# Read the JSON file
with open('tel_data_before_serialization_Nyhavna20sek.json') as file:
    data = json.load(file)

# Check if data is a list
if isinstance(data, list):
    # Extract the telemetry data from each dictionary in the list
    telemetry = [item['telemetry'] for item in data if 'telemetry' in item]
else:
    # Extract the telemetry data
    telemetry = data['telemetry']

# Create a figure for the latitude
fig_latitude = plt.figure()
plt.plot([item['latitude'] for item in telemetry])
plt.xlabel('Time')
plt.ylabel('Latitude')
plt.title('Latitude Data')

# Create a figure for the longitude
fig_longitude = plt.figure()
plt.plot([item['longitude'] for item in telemetry])
plt.xlabel('Time')
plt.ylabel('Longitude')
plt.title('Longitude Data')

# Create a figure for the depth
fig_depth = plt.figure()
plt.plot([item['depth'] for item in telemetry])
plt.xlabel('Time')
plt.ylabel('Depth')
plt.title('Depth Data')

# Show the plots
plt.show()