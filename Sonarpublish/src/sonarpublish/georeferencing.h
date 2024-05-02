#ifndef GEOREFERENCING_H
#define GEOREFERENCING_H

// Define a struct to hold the ECEF coordinates for easy return from the function
typedef struct {
    float x, y, z;
} ECEF_Coordinates;

#define MAX_POINTS 300  // Define MAX_POINTS as a macro

// Define a struct to hold the georeferenced data for easy return from the georeferencing function
typedef struct {
    int num_points;     // Number of points

    float PointCloud_Rotated_NED[MAX_POINTS][3]; // Pointer to an array of points, each with 3 float coordinates, transformed with orientation to NED, not translation vector
    float R_BN[3][3];   // Rotation matrix from Body to NED

    float PointCloud_Rotated_ECEF[MAX_POINTS][3]; // Pointer to an array of points, each with 3 float coordinates, transformed with orientation to ECEF, not translation vector
    float body_ecef[3]; // Array to hold the ECEF position of the robot
    float R_BECEF[3][3];   // Rotation matrix from Body to ECEF

} Georef_data;

// Function to perform georeferencing using ECEF coordinates
Georef_data georeferencing(float roll, float pitch, float heading, float y[], float z[], int yz_length, float longitude, float latitude, float depth);

// Function to convert latitude, longitude, and height to Earth-Centered, Earth-Fixed (ECEF) coordinates
ECEF_Coordinates llh2ecef(float l, float mu, float depth);

#endif // GEOREFERENCING_H