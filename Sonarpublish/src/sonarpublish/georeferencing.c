#include "georeferencing.h"
#include <math.h>
#include <stdlib.h>

// Function to convert degrees to radians
float radians(float degrees) {
    return degrees * (M_PI / 180.0);
}

void multiplyMatrices3x3(float result[3][3], float mat1[3][3], float mat2[3][3]) {
    for (int row = 0; row < 3; row++) {
        for (int col = 0; col < 3; col++) {
            result[row][col] = 0; // Initialize element
            for (int k = 0; k < 3; k++) {
                result[row][col] += mat1[row][k] * mat2[k][col];
            }
        }
    }
}

// Function to perform matrix-vector multiplication (3x3 matrix * 3x1 vector)
void multiplyMatrixVector3x3(float result[3], float mat[3][3], float vec[3]) {
    for (int i = 0; i < 3; i++) {
        result[i] = 0; // Initialize element
        for (int j = 0; j < 3; j++) {
            result[i] += mat[i][j] * vec[j];
        }
    }
}

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


Georef_data georeferencing(float roll, float pitch, float heading, float y[], float z[], int yz_length, float longitude, float latitude, float depth) {
    // Sonar to Body transformation
    float T_B[3] = {-0.6881, 0.007, -0.061};
    float (*P_B)[3] = malloc(yz_length * sizeof(*P_B));

    // Loop through each point in the input arrays
    for (int i = 0; i < yz_length; i++) { // P_B = P_S + T_B
        // x-component (T_B[0] since the x-component of P_S is always 0)
        P_B[i][0] = T_B[0];

        // y-component
        P_B[i][1] = y[i] + T_B[1]; // Adjust based on your coordinate system requirements

        // z-component
        P_B[i][2] = z[i] + T_B[2];
    }


    // Body to NED transformation
    roll = radians(roll);
    pitch = radians(pitch);
    heading = radians(heading); 

    float R_X[3][3] = {
        {1, 0, 0},
        {0, cos(roll), -sin(roll)},
        {0, sin(roll), cos(roll)}
    };

    float R_Y[3][3] = {
        {cos(pitch), 0, sin(pitch)},
        {0, 1, 0},
        {-sin(pitch), 0, cos(pitch)}
    };

    float R_Z[3][3] = {
        {cos(heading), -sin(heading), 0},
        {sin(heading), cos(heading), 0},
        {0, 0, 1}
    };

    // Intermediate result for R_Y * R_X
    float R_YX[3][3];
    multiplyMatrices3x3(R_YX, R_Y, R_X);
    // Final result for R_Z * R_YX = R_BN
    float R_BN[3][3];
    multiplyMatrices3x3(R_BN, R_Z, R_YX);

    // Calculate transformed points
    float (*P_N_B)[3] = malloc(yz_length * sizeof(*P_N_B));
    for (int i = 0; i < yz_length; i++) {
        float point[3] = {P_B[i][0], P_B[i][1], P_B[i][2]};
        float transformedPoint[3];
        multiplyMatrixVector3x3(transformedPoint, R_BN, point); // Transform each point
        P_N_B[i][0] = transformedPoint[0];
        P_N_B[i][1] = transformedPoint[1];
        P_N_B[i][2] = transformedPoint[2];
    }

    latitude = radians(latitude);
    longitude =  radians(longitude);
    ECEF_Coordinates points_ecef = llh2ecef(longitude, latitude, depth);


    float (*P_N)[3] = malloc(yz_length * sizeof(*P_N));
    // Add the ECEF coordinates as an offset to each transformed point in P_N_B
    for (int i = 0; i < yz_length; i++) {
        P_N[i][0] = P_N_B[i][0] + points_ecef.x;
        P_N[i][1] = P_N_B[i][1] + points_ecef.y;
        P_N[i][2] = P_N_B[i][2] + points_ecef.z;
    }

    Georef_data result;
    result.points = P_N; // This memory must be freed where georeferencing is called
    result.num_points = yz_length;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            result.R_BN[i][j] = R_BN[i][j];
        }
    }

    free(P_B);
    free(P_N_B);

    return result;

}