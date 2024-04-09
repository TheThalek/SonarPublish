#ifndef GEOREFERENCING_H
#define GEOREFERENCING_H

// Define a struct to hold the ECEF coordinates for easy return from the function
typedef struct {
    float x, y, z;
} ECEF_Coordinates;

// Define a struct to hold the georeferenced data for easy return from the georeferencing function
typedef struct {
    float (*points)[3]; // Pointer to an array of points, each with 3 float coordinates
    int num_points;     // Number of points
    float R_BN[3][3];   // Rotation matrix
    float body_ecef_position[3]; // Array to hold the ECEF coordinates for each point
} Georef_data;

// Function to perform georeferencing using ECEF coordinates
Georef_data georeferencing(float roll, float pitch, float heading, float y[], float z[], int yz_length, float longitude, float latitude, float depth);

// Function to convert latitude, longitude, and height to Earth-Centered, Earth-Fixed (ECEF) coordinates
ECEF_Coordinates llh2ecef(float l, float mu, float depth);

#endif // GEOREFERENCING_H