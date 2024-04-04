
// ***************************************************************************
// Part of Gstsonar - Gstreamer sonar processing plugins
//
// Copyright (c) 2023 Eelume AS <opensource@eelume.com>
// All rights reserved
//
// Licensed under the LGPL v2.1 License.
// See LICENSE file in the project root for full license information.
// ***************************************************************************
#include "linalg.h"

#include <Eigen/Dense>

#include <stdio.h>

#include <map>
#include <vector>
#include <utility> // For std::pair

Eigen::Vector3f linalg_calculate_rotation_vector(const linalg_euler_angles_t* angles)
{
    Eigen::Quaternionf q =
        Eigen::AngleAxisf{angles->roll, Eigen::Vector3f::UnitX()} * Eigen::AngleAxisf{angles->pitch, Eigen::Vector3f::UnitY()} * Eigen::AngleAxisf{angles->yaw, Eigen::Vector3f::UnitZ()};

    Eigen::AngleAxisf axis_angle(q);

    return axis_angle.axis() * axis_angle.angle();
}

void linalg_calculate_euler_angles(linalg_euler_angles_t* angles, const Eigen::Vector3f& rotation_vector)
{
    Eigen::AngleAxisf axis_angle = Eigen::AngleAxisf(rotation_vector.norm(), rotation_vector.normalized());

    Eigen::Quaternionf q = Eigen::Quaternionf(axis_angle);

    auto euler = q.toRotationMatrix().eulerAngles(0, 1, 2);

    angles->roll  = euler.x();
    angles->pitch = euler.y();
    angles->yaw   = euler.z();
}

void linalg_interpolate_euler_angles(linalg_euler_angles_t* out, const linalg_euler_angles_t* first, const linalg_euler_angles_t* second, uint64_t interpolation_time)
{
    assert((interpolation_time >= first->time) && (interpolation_time <= second->time));

    auto first_rotation  = linalg_calculate_rotation_vector(first);
    auto second_rotation = linalg_calculate_rotation_vector(second);

    Eigen::Vector3f out_rotation;
    if (first->time == second->time)
        out_rotation = .5 * (first_rotation + second_rotation);
    else
        out_rotation = ((interpolation_time - first->time) * first_rotation + (second->time - interpolation_time) * second_rotation) * (1.f / (second->time - first->time));

    linalg_calculate_euler_angles(out, out_rotation);
}

float linalg_interpolate_scalar(float first, uint64_t first_time, float second, uint64_t second_time, uint64_t interpolation_time)
{
    assert((interpolation_time >= first_time) && (interpolation_time <= second_time));
    float interpolated_value = first + ((float)(interpolation_time - first_time) / (second_time - first_time)) * (second - first);

    return interpolated_value;
}



float linalg_interpolate_scalar_with_print(float first, uint64_t first_time, float second, uint64_t second_time, uint64_t interpolation_time)
{
    assert((interpolation_time >= first_time) && (interpolation_time <= second_time));
    printf("New set of data \n");
    printf("First Time: %llu\n", first_time);
    printf("Second Time: %llu\n", second_time);
    printf("Interpolation Time: %llu\n", interpolation_time);
    printf("First: %.18f\n", first);
    printf("Second: %.18f\n", second);
    float interpolated_value = first + ((float)(interpolation_time - first_time) / (second_time - first_time)) * (second - first);
    printf("Interpolated: %.18f\n", interpolated_value);

    return interpolated_value;
}







std::map<char, std::vector<std::pair<float, uint64_t>>> datapoints_and_time;

auto getValue = [](const std::pair<float, uint64_t>& p) { return p.first; };
auto getTime = [](const std::pair<float, uint64_t>& p) { return p.second; };

void appendNewDataToDatapoints(float data, uint64_t data_time, char data_name, int maxNumPoints = 50) {
    auto& dataPoints = datapoints_and_time[data_name];
    dataPoints.push_back(std::make_pair(data, data_time));
    
    while (dataPoints.size() > maxNumPoints) {
        dataPoints.erase(dataPoints.begin());
    }
}

float cubicSpline_interpolate_scalar(float first, uint64_t first_time, float second, uint64_t second_time, uint64_t interpolation_time, char data_name) {
    int maxNumOfControlPoints = 50;
    
    assert((interpolation_time >= first_time) && (interpolation_time <= second_time));

    // Save new data to list, if first time function is called save both first and second data
    if (datapoints_and_time[data_name].empty()) {
        appendNewDataToDatapoints(first, first_time, data_name, maxNumOfControlPoints);
    }   
    appendNewDataToDatapoints(second, second_time, data_name, maxNumOfControlPoints); 

    // Extract data from datapoints_and_time, and prepare it for GSL
    const auto& all_data = datapoints_and_time[data_name];
    std::vector<double> data_points, data_time;
    for (const auto& pair : all_data) {
        data_points.push_back(static_cast<double>(getTime(pair)));
        data_time.push_back(static_cast<double>(getValue(pair)));
    }

    // Cubic Spline Interpolation
    // GSL setup for cubic spline interpolation
    gsl_interp_accel *acc = gsl_interp_accel_alloc();
    gsl_spline *spline = gsl_spline_alloc(gsl_interp_cspline, data_time.size());

    gsl_spline_init(spline, data_time.data(), data_points.data(), data_time.size());

    // Perform the interpolation for the given interpolation_time.
    // Ensure interpolation_time is within the bounds of your data.
    double interpolated_data = gsl_spline_eval(spline, static_cast<double>(interpolation_time), acc);

    // Free GSL resources
    gsl_spline_free(spline);
    gsl_interp_accel_free(acc);

    return interpolated_data;
}




// void appendNewDataToDataMatrix(double data, uint64_t data_time, char data_name) {
//     Eigen::MatrixXd& matrix = dataMatrices[data_name]; // Using MatrixXd (double) instead of MatrixXf (float) to avoid precision loss
    
//     // Convert uint64_t to double (no significant precision loss expected).
//     double timeAsDouble = static_cast<double>(data_time);
    
//     // If this is the first data for data_name, initialize the matrix.
//     if (matrix.size() == 0) {
//         matrix.resize(2, 1); // 2 rows for second and second_time, 1 column for the data pair.
//         matrix(0, 0) = data;
//         matrix(1, 0) = timeAsDouble;
//     } else {
//         // Append a new column for the new data pair.
//         Eigen::MatrixXd newColumn(2, 1);
//         newColumn(0, 0) = data;
//         newColumn(1, 0) = timeAsDouble;
//         matrix.conservativeResize(Eigen::NoChange, matrix.cols() + 1);
//         matrix.col(matrix.cols() - 1) = newColumn;
// }


// float cubicSpline_interpolate_scalar(float first, uint64_t first_time, float second, uint64_t second_time, uint64_t interpolation_time, char data_name) {
//     assert((interpolation_time >= first_time) && (interpolation_time <= second_time));

//     // Save new data to list, if first time function is called save both first and second data
//     if (dataMatrices[data_name].cols() == 0) {
//         appendNewDataToDataMatrix(first, first_time, data_name);
//     }   
//     appendNewDataToDataMatrix(second, second_time, data_name); 

//     // Eigen::Spline<float, 1> spline = Eigen::SplineFitting<Eigen::Spline<float, 1>>::Interpolate(y_values, 3);
//     // interpolated_value = spline(interpolation_time);
//     float interpolated_value = 0.0;
//     return interpolated_value;
// }

