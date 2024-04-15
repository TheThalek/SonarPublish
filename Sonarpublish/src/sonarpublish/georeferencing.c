#include "georeferencing.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

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

// // Function to perform matrix-vector multiplication (3x3 matrix * 3x1 vector)
// void multiplyMatrixVector3x3(float result[3], float mat[3][3], float vec[3]) {
//     for (int i = 0; i < 3; i++) {
//         result[i] = 0; // Initialize element
//         for (int j = 0; j < 3; j++) {
//             result[i] += mat[i][j] * vec[j];
//         }
//     }
// }


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
    // // print all input data
    // printf("Degrees; Roll: %.8f, Pitch: %.8f, Heading: %.8f\n", roll, pitch, heading);
    // printf("Longitude: %.8f, Latitude: %.8f, Depth: %.8f\n", longitude, latitude, depth);
    // printf("Y: ");
    // for (int i = 0; i < yz_length; i++) {
    //     printf("%.8f ", y[i]);
    // }
    // printf("\n");
    // printf("Z: ");
    // for (int i = 0; i < yz_length; i++) {
    //     printf("%.8f ", z[i]);
    // }
    // printf("\n");


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
    
    // // Body to NED transformation
    
    // Normalize the angles. 
    
    // float R_X[3][3] = {
    //     {1, 0, 0},
    //     {0, cos(roll), -sin(roll)},
    //     {0, sin(roll), cos(roll)}
    // };

    // float R_Y[3][3] = {
    //     {cos(pitch), 0, sin(pitch)},
    //     {0, 1, 0},
    //     {-sin(pitch), 0, cos(pitch)}
    // };

    // float R_Z[3][3] = {
    //     {cos(heading), -sin(heading), 0},
    //     {sin(heading), cos(heading), 0},
    //     {0, 0, 1}
    // };

    // heading = radians(0);
    // roll = radians(0);
    // pitch = radians(0);

    float R_nb[3][3] = {
        {cos(heading)*cos(pitch), -sin(heading)*cos(roll)+cos(heading)*sin(pitch)*sin(roll), sin(heading)*sin(roll)+cos(heading)*cos(roll)*sin(pitch)},
        {sin(heading)*cos(pitch), cos(heading)*cos(roll)+sin(roll)*sin(pitch)*sin(heading), -cos(heading)*sin(roll)+sin(pitch)*sin(heading)*cos(roll)},
        {-sin(pitch), cos(pitch)*sin(roll), cos(pitch)*cos(roll)}
    }; // In ZYX, from Fossens book
    


    // float R_nb[3][3] = {
    //     { cos(heading) * cos(pitch), cos(heading) * sin(pitch) * sin(roll) - sin(heading) * cos(roll), cos(heading) * sin(pitch) * cos(roll) + sin(heading) * sin(roll) },
    //     { sin(heading) * cos(pitch), sin(heading) * sin(pitch) * sin(roll) + cos(heading) * cos(roll), sin(heading) * sin(pitch) * cos(roll) - cos(heading) * sin(roll) },
    //     { -sin(pitch), cos(pitch) * sin(roll), cos(pitch) * cos(roll) }
    // };

    // A test where R_nb [0,0] and cos(heading) * cos(pitch) is printed. 



    // // Correct multiplication order for ZYX (heading, pitch, roll) rotation sequence
    // float R_ZY[3][3];
    // multiplyMatrices3x3(R_ZY, R_Z, R_Y);  // First Z and Y
    // float R_nb[3][3];
    // multiplyMatrices3x3(R_nb, R_ZY, R_X);  // Then the result with X

    // // Correct multiplication order for XYZ (roll, pitch, heading) rotation sequence
    // float R_XY[3][3];
    // multiplyMatrices3x3(R_XY, R_X, R_Y);  // First X and Y
    // float R_nb[3][3];
    // multiplyMatrices3x3(R_nb, R_XY, R_Z);  // Then the result with Z


    // printf("R_nb:\n");
    // for (int i = 0; i < 3; i++) {
    //     for (int j = 0; j < 3; j++) {
    //         printf("%.8f ", R_nb[i][j]);
    //     }
    //     printf("\n");
    // }
    

    printf("New scan \n");
    for (int i = 0; i < yz_length; i++) {
        P_N_B[i][0] = R_nb[0][0]*P_B[i][0] + R_nb[0][1]*P_B[i][1] + R_nb[0][2]*P_B[i][2]; // R_00*x+R_01*y+R_02*z
        P_N_B[i][1] = R_nb[1][0]*P_B[i][0] + R_nb[1][1]*P_B[i][1] + R_nb[1][2]*P_B[i][2]; // R_10*x+R_11*y+R_12*z
        P_N_B[i][2] = R_nb[2][0]*P_B[i][0] + R_nb[2][1]*P_B[i][1] + R_nb[2][2]*P_B[i][2];

        // P_N_B[i][0] = 0; // R_00*x+R_01*y+R_02*z
        // P_N_B[i][1] = y[i]; // R_10*x+R_11*y+R_12*z
        // P_N_B[i][2] = z[i];

        // float point[3] = {P_B[i][0], P_B[i][1], P_B[i][2]};
        // float transformedPoint[3];
        // multiplyMatrixVector3x3(transformedPoint, R_nb, point); // Transform each point
        // P_N_B_before[i][0] = transformedPoint[0];
        // P_N_B_before[i][1] = transformedPoint[1];
        // P_N_B_before[i][2] = transformedPoint[2];


        // printf("R_nb: %.8f, %.8f, %.8f R_nb: %.8f, %.8f, %.8f R_nb: %.8f, %.8f, %.8f\n", R_nb[0][0], R_nb[0][1], R_nb[0][2], R_nb[1][0], R_nb[1][1], R_nb[1][2], R_nb[2][0], R_nb[2][1], R_nb[2][2]);

        // Print point
        // printf("Point: %.8f, %.8f, %.8f\n", point[0], point[1], point[2]);
        
        // print the P_N_B
        printf("P_N_B: %.8f, %.8f, %.8f\n", P_N_B[i][0], P_N_B[i][1], P_N_B[i][2]);
        // printf("P_N_B_before: %.8f, %.8f, %.8f\n", P_N_B_before[i][0], P_N_B_before[i][1], P_N_B_before[i][2]);
        // Print all of R_nb
        // printf("R_nb: %.8f, %.8f, %.8f\n", R_nb[0][0], R_nb[0][1], R_nb[0][2]);
        // printf("R_nb: %.8f, %.8f, %.8f\n", R_nb[1][0], R_nb[1][1], R_nb[1][2]);
        // printf("R_nb: %.8f, %.8f, %.8f\n", R_nb[2][0], R_nb[2][1], R_nb[2][2]);
    }




    ECEF_Coordinates body_position_ecef = llh2ecef(radians(longitude), radians(latitude), depth);
    // ALSO, double check this calculation! SHould still give the same depth out!!
    
    // printf("Body position ECEF: %.8f, %.8f, %.8f\n", body_position_ecef.x, body_position_ecef.y, body_position_ecef.z);
    
    
    Georef_data result;

    result.body_ecef[0] = body_position_ecef.x;
    result.body_ecef[1] = body_position_ecef.y;
    result.body_ecef[2] = body_position_ecef.z;

    for (int i = 0; i < yz_length; i++) { // The points  of the robot, referenced to the robot body frame
        for (int j = 0; j < 3; j++) {
            result.points_body[i][j] = P_N_B[i][j];

            // printf result.points_body[i][j]
            // printf("Result points body: %.8f\n", result.points_body[i][j]);

        }
    }

    result.num_points = yz_length;

    for (int i = 0; i < 3; i++) { // The rotation matrix
        for (int j = 0; j < 3; j++) {
            result.R_BN[i][j] = R_nb[i][j];
            // printf("Result R_BN: %.8f\n", result.R_BN[i][j]);
        }
    }

    return result;
}