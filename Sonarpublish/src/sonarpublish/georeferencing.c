#include "georeferencing.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

// Testing the georef
static float heading_test = 0;
static float pitch_test = 0;
static float roll_test = 0;

static int first_test = 1;


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

void transposeMatrix3x3(float result[3][3], float matrix[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            result[j][i] = matrix[i][j];
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

    float h = -depth; // Should be Height above the WGS-84 ellipsoid in meters. In practice, this is the depth of the robot in the water, relative to ocean surface, not WGS-84 ellipsoid

    float r_e = 6378137.0;  // Radius of the Earth at the equator in meters (WGS-84)
    float r_p = 6356752.3142;  // Polar radius in meters (WGS-84)

    // Calculation of N using the correct squaring operation
    float N = pow(r_e, 2) / sqrt(pow(r_e * cos(mu), 2) + pow(r_p * sin(mu), 2));

    ECEF_Coordinates coordinates;
    coordinates.x = (N + h) * cos(mu) * cos(l);
    coordinates.y = (N + h) * cos(mu) * sin(l);
    coordinates.z = (N * pow(r_p / r_e, 2) + h) * sin(mu);

    return coordinates;
}

Georef_data georeferencing(float roll, float pitch, float heading, float y[], float z[], int yz_length, float longitude, float latitude, float depth) {

    // Sonar to Body transformation
    float T_B[3] = {-0.6881, 0.007, -0.061};

    if (yz_length > MAX_POINTS) {
        printf("Too many points as input");
    }


    float P_B[MAX_POINTS][3];
    float P_ECEF[MAX_POINTS][3];
    float P_ECEF_before[MAX_POINTS][3];
    float P_NED[MAX_POINTS][3];

    // Loop through each point in the input arrays
    for (int i = 0; i < yz_length; i++) { // P_B = P_S + T_B
        // x-component (T_B[0] since the x-component of P_S is always 0)
        P_B[i][0] = T_B[0];

        // y-component
        P_B[i][1] = y[i] + T_B[1]; 

        // z-component
        P_B[i][2] = z[i] + T_B[2];

    }

    float R_bn[3][3] = { 
        {cos(heading)*cos(pitch), -sin(heading)*cos(roll)+cos(heading)*sin(pitch)*sin(roll), sin(heading)*sin(roll)+cos(heading)*cos(roll)*sin(pitch)},
        {sin(heading)*cos(pitch), cos(heading)*cos(roll)+sin(roll)*sin(pitch)*sin(heading), -cos(heading)*sin(roll)+sin(pitch)*sin(heading)*cos(roll)},
        {-sin(pitch), cos(pitch)*sin(roll), cos(pitch)*cos(roll)}
    }; // In ZYX, from Fossens book

    float R_ne[3][3] = {
        {-sin(radians(longitude)) * cos(radians(latitude)), -sin(radians(longitude))*sin(radians(latitude)), cos(radians(longitude)) },
        {cos(radians(longitude))*cos(radians(latitude)), cos(radians(longitude))*sin(radians(latitude)), sin(radians(longitude))},
        {-cos(radians(latitude)), sin(radians(latitude)), 0}
    };

    // Transpose R_ne to be R_ne_trans or something 
    float R_ne_trans[3][3];
    transposeMatrix3x3(R_ne_trans, R_ne); 

    float R_be[3][3];

    multiplyMatrices3x3(R_be, R_bn, R_ne);

    for (int i = 0; i < yz_length; i++) {
        P_NED[i][0] = R_bn[0][0]*P_B[i][0] + R_bn[0][1]*P_B[i][1] + R_bn[0][2]*P_B[i][2]; // R_00*x+R_01*y+R_02*z
        P_NED[i][1] = R_bn[1][0]*P_B[i][0] + R_bn[1][1]*P_B[i][1] + R_bn[1][2]*P_B[i][2]; // R_10*x+R_11*y+R_12*z
        P_NED[i][2] = R_bn[2][0]*P_B[i][0] + R_bn[2][1]*P_B[i][1] + R_bn[2][2]*P_B[i][2];
    }

    for (int i = 0; i < yz_length; i++) {
        P_ECEF[i][0] = R_be[0][0]*P_B[i][0] + R_be[0][1]*P_B[i][1] + R_be[0][2]*P_B[i][2]; // R_00*x+R_01*y+R_02*z
        P_ECEF[i][1] = R_be[1][0]*P_B[i][0] + R_be[1][1]*P_B[i][1] + R_be[1][2]*P_B[i][2]; // R_10*x+R_11*y+R_12*z
        P_ECEF[i][2] = R_be[2][0]*P_B[i][0] + R_be[2][1]*P_B[i][1] + R_be[2][2]*P_B[i][2];
    }

    ECEF_Coordinates body_position_ecef = llh2ecef(radians(longitude), radians(latitude), depth);
    // ALSO, double check this calculation! SHould still give the same depth out!!

    Georef_data result;

    result.body_ecef[0] = body_position_ecef.x;
    result.body_ecef[1] = body_position_ecef.y;
    result.body_ecef[2] = body_position_ecef.z;

    for (int i = 0; i < yz_length; i++) { // The points  of the robot, referenced to the robot body frame
        for (int j = 0; j < 3; j++) {
            result.PointCloud_Rotated_ECEF[i][j] = P_ECEF[i][j];
        }
    }

    for (int i = 0; i < yz_length; i++) { // The points  of the robot, referenced to the robot body frame
        for (int j = 0; j < 3; j++) {
            result.PointCloud_Rotated_NED[i][j] = P_NED[i][j];
        }
    }


    result.num_points = yz_length;

    for (int i = 0; i < 3; i++) { // The rotation matrix
        for (int j = 0; j < 3; j++) {
            result.R_BN[i][j] = R_bn[i][j];
        }
    }

    for (int i = 0; i < 3; i++) { // The rotation matrix
        for (int j = 0; j < 3; j++) {
            result.R_BECEF[i][j] = R_be[i][j];
        }
    }

    return result;
}
