#ifndef GEOREFERENCING_H
#define GEOREFERENCING_H

// Function to convert latitude, longitude, and height to Earth-Centered, Earth-Fixed (ECEF) coordinates
void llh2ecef(double latitude, double longitude, double height);


// Define a struct to hold the ECEF coordinates for easy return from the function
typedef struct {
    float x;
    float y;
    float z;
} ECEF_Coordinates;

// Function to perform georeferencing using ECEF coordinates
void georeferencing(float roll, float pitch, float heading, float y, float z, float longitude, float latitude, float depth);

#endif // GEOREFERENCING_H