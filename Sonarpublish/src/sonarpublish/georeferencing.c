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
    float P_N_B[MAX_POINTS][3];
    float P_N_B_before[MAX_POINTS][3];
    float P_N[MAX_POINTS][3];


    // Loop through each point in the input arrays
    for (int i = 0; i < yz_length; i++) { // P_B = P_S + T_B
        // x-component (T_B[0] since the x-component of P_S is always 0)
        P_B[i][0] = T_B[0];

        // y-component
        P_B[i][1] = y[i] + T_B[1]; // Adjust based on your coordinate system requirements

        // z-component
        P_B[i][2] = z[i] + T_B[2];

        // printf("P_B: %.8f, %.8f, %.8f\n", P_B[i][0], P_B[i][1], P_B[i][2]);
    }
    

    // Testing the georef. with constant angle change, to see if it is correct
    // float jump = 0.01;
    // heading_test = heading_test + jump;
    // roll_test = roll_test + jump;
    // pitch_test = pitch_test + jump;
    
    // if (first_test == 1) {
    //     roll_test = radians(0);
    //     first_test = 0;
    // }
    // else {
    //     roll_test = radians(45);
    // }

    // float R_nb[3][3] = {
    //     {cos(heading_test)*cos(pitch_test), -sin(heading_test)*cos(roll_test)+cos(heading_test)*sin(pitch_test)*sin(roll_test), sin(heading_test)*sin(roll_test)+cos(heading_test)*cos(roll_test)*sin(pitch_test)},
    //     {sin(heading_test)*cos(pitch_test), cos(heading_test)*cos(roll_test)+sin(roll_test)*sin(pitch_test)*sin(heading_test), -cos(heading_test)*sin(roll_test)+sin(pitch_test)*sin(heading_test)*cos(roll_test)},
    //     {-sin(pitch_test), cos(pitch_test)*sin(roll_test), cos(pitch_test)*cos(roll_test)}
    // }; // In ZYX, from Fossens book


    float R_nb[3][3] = {
        {cos(heading)*cos(pitch), -sin(heading)*cos(roll)+cos(heading)*sin(pitch)*sin(roll), sin(heading)*sin(roll)+cos(heading)*cos(roll)*sin(pitch)},
        {sin(heading)*cos(pitch), cos(heading)*cos(roll)+sin(roll)*sin(pitch)*sin(heading), -cos(heading)*sin(roll)+sin(pitch)*sin(heading)*cos(roll)},
        {-sin(pitch), cos(pitch)*sin(roll), cos(pitch)*cos(roll)}
    }; // In ZYX, from Fossens book


    for (int i = 0; i < yz_length; i++) {
        P_N_B[i][0] = R_nb[0][0]*P_B[i][0] + R_nb[0][1]*P_B[i][1] + R_nb[0][2]*P_B[i][2]; // R_00*x+R_01*y+R_02*z
        P_N_B[i][1] = R_nb[1][0]*P_B[i][0] + R_nb[1][1]*P_B[i][1] + R_nb[1][2]*P_B[i][2]; // R_10*x+R_11*y+R_12*z
        P_N_B[i][2] = R_nb[2][0]*P_B[i][0] + R_nb[2][1]*P_B[i][1] + R_nb[2][2]*P_B[i][2];

    }

    ECEF_Coordinates body_position_ecef = llh2ecef(radians(longitude), radians(latitude), depth);
    // ALSO, double check this calculation! SHould still give the same depth out!!

    Georef_data result;

    result.body_ecef[0] = body_position_ecef.x;
    result.body_ecef[1] = body_position_ecef.y;
    result.body_ecef[2] = body_position_ecef.z;

    for (int i = 0; i < yz_length; i++) { // The points  of the robot, referenced to the robot body frame
        for (int j = 0; j < 3; j++) {
            result.points_body[i][j] = P_N_B[i][j];

        }
    }

    result.num_points = yz_length;

    for (int i = 0; i < 3; i++) { // The rotation matrix
        for (int j = 0; j < 3; j++) {
            result.R_BN[i][j] = R_nb[i][j];
        }
    }

    return result;
}