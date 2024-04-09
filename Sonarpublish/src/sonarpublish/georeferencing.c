#include "georeferencing.h"

ECEF_Coordinates llh2ecef(float l, float mu, float depth) {
    // Function originally in matlab code, found  in https://github.com/cybergalactic/MSS/blob/master/GNC/llh2ecef.m
    // Translated myself to python

    // Converts geodetic coordinates (longitude, latitude, and height) to 
    // Earth-Centered, Earth-Fixed (ECEF) coordinates.
    
    // Parameters:
    // - l: Longitude in radians.
    // - mu: Latitude in radians.
    // - depth: 
    
    // Returns:
    // - x, y, z: ECEF coordinates. 

    float h = -depth; // Height above the WGS-84 ellipsoid in meters.

    float r_e = 6378137.0;  // Radius of the Earth at the equator in meters (WGS-84)
    float r_p = 6356752.3142;  // Polar radius in meters (WGS-84)
    float e = 0.08181979099211;  // Eccentricity not used in this calculation, can be omitted if not needed elsewhere
    float N = r_e * r_e / sqrt((r_e * cos(mu)) * (r_e * cos(mu)) + (r_p * sin(mu)) * (r_p * sin(mu)));

    // Initialize struct to hold ECEF coordinates
    ECEF_Coordinates coordinates;

    coordinates.x = (N + h) * cos(mu) * cos(l);
    coordinates.y = (N + h) * cos(mu) * sin(l);
    coordinates.z = (N * (r_p / r_e) * (r_p / r_e) + h) * sin(mu);

    return coordinates; // Return the struct containing ECEF coordinates
}


void georeferencing(float roll, float pitch, float heading, float y[], float z[], int yz_length, float longitude, float latitude, float depth) {
    // Sonar to Body transformation
    float T_B[3] = {-0.6881, 0.007, -0.061};
    float P_B[yz_length][3];

    // Loop through each point in the input arrays
    for (int i = 0; i < yz_length; i++) {
        // x-component (T_B[0] since the x-component of P_S is always 0)
        P_B[i][0] = T_B[0];

        // y-component
        P_B[i][1] = y[i] + T_B[1]; // Adjust based on your coordinate system requirements

        // z-component
        P_B[i][2] = z[i] + T_B[2];
    }

    // Body to NED transformation




}