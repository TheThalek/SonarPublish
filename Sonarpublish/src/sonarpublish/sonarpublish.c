// ***************************************************************************
// Part of Gstsonar - Gstreamer sonar processing plugins
//
// Copyright (c) 2023 Eelume AS <opensource@eelume.com>
// All rights reserved
//
// Licensed under the LGPL v2.1 License.
// See LICENSE file in the project root for full license information.
// ***************************************************************************
/**
 * SECTION:element-gst_sonarsink
 *
 * Sonarsink visualizes sonar data
 *
 *
 * <refsect2>
 * <title>Example launch line</title>
 * |[
  TODO
 * </refsect2>
 */


// export SBD=./samples/2022-11-22_09-41-38_eelume_ntnu_Nyhavna.SBD
// GST_PLUGIN_PATH=. GST_DEBUG=2,sonarsink:9 gst-launch-1.0 filesrc location=$SBD ! sonarparse ! sonarmux name=mux ! sonarpublish zoom=0.1 filesrc location=$SBD ! nmeaparse ! eelnmeadec ! mux.


#include "sonarpublish.h"
#include "georeferencing.h"

#include <math.h>
#include <stdio.h>

#include <stdlib.h>
#include "sonarData.pb-c.h"
#include <stdbool.h>

#include <jansson.h>


GST_DEBUG_CATEGORY_STATIC(sonarpublish_debug);
#define GST_CAT_DEFAULT sonarpublish_debug

#define gst_sonarpublish_parent_class parent_class
G_DEFINE_TYPE(Gstsonarpublish, gst_sonarpublish, GST_TYPE_BASE_SINK);

enum
{
    PROP_0,
    PROP_ZOOM,
    PROP_GAIN,
};

const double rad2deg_sonarpub = 180.0/M_PI;
const double deg2rad_sonarpub = M_PI/180.0;
bool metadata_warning_shown_sonarpub = false;

#define DEFAULT_PROP_ZOOM 1
#define DEFAULT_PROP_GAIN 1

static GstStaticPadTemplate gst_sonarpublish_sink_template = GST_STATIC_PAD_TEMPLATE("sink", GST_PAD_SINK, GST_PAD_ALWAYS, GST_STATIC_CAPS("sonar/multibeam ; sonar/bathymetry"));



static GstFlowReturn gst_sonarpublish_render(GstBaseSink* basesink, GstBuffer* buf) {
    Gstsonarpublish* sonarpublish = GST_sonarpublish(basesink);
    GST_OBJECT_LOCK(sonarpublish);

    // Extract the metadata from the buffer
    const GstSonarMeta* meta = GST_SONAR_META_GET(buf);
    const GstSonarFormat* format = &meta->format;
    const GstSonarParams* params = &meta->params;

    GST_DEBUG_OBJECT(sonarpublish, "%lu: rendering buffer: %p, width n_beams = %d, resolution = %d, sound_speed = %f, sample_rate = %f, t0 = %d, gain = %f", buf->pts, buf, sonarpublish->n_beams,
        sonarpublish->resolution, params->sound_speed, params->sample_rate, params->t0, params->gain);

    GstMapInfo mapinfo;
    if (!gst_buffer_map(buf, &mapinfo, GST_MAP_READ))
    {
        GST_OBJECT_UNLOCK(sonarpublish);
        return GST_FLOW_ERROR;
    }


    switch (sonarpublish->sonar_type)
    {
        case GST_SONAR_TYPE_FLS:
        {
            const float max_range = ((params->t0 + sonarpublish->resolution) * params->sound_speed) / (2 * params->sample_rate);

            const float total_gain = sonarpublish->gain / params->gain;

            for (int range_index = 0; range_index < sonarpublish->resolution; ++range_index)
            {
                for (int beam_index = 0; beam_index < sonarpublish->n_beams; ++beam_index)
                {
                    float beam_intensity = gst_sonar_format_get_measurement(format, mapinfo.data, beam_index, range_index);
                    float beam_angle     = gst_sonar_format_get_angle(format, mapinfo.data, beam_index);
                    float range          = ((params->t0 + range_index) * params->sound_speed) / (2 * params->sample_rate);

                    int vertex_index = 3 * (beam_index * sonarpublish->resolution + range_index);
                    float* vertex    = sonarpublish->vertices + vertex_index;

                    float range_norm = range / max_range;

                    vertex[0] = -sin(beam_angle) * range_norm * sonarpublish->zoom;
                    vertex[1] = -1 + cos(beam_angle) * range_norm * sonarpublish->zoom;
                    vertex[2] = -1;

                    float I = total_gain * beam_intensity;
                    if (I > 1)
                    {
                        GST_TRACE_OBJECT(sonarpublish, "intensity too large: %f > %f", beam_intensity, total_gain);
                        I = 1;
                        // gst_buffer_unmap (buf, &mapinfo);
                        // GST_OBJECT_UNLOCK (sonarpublish);
                        // return GST_FLOW_ERROR;
                    }

                    if (sonarpublish->detected)
                    {
                        // the index of the detected first point of contact is stored in the first range_index for each beam
                        float first_contact = gst_sonar_format_get_measurement(format, mapinfo.data, beam_index, 0);
                    }
                }
            }
            break;
        }
        case GST_SONAR_TYPE_BATHYMETRY:
        {
            g_assert(sonarpublish->resolution == 1);

            // Initialize your main messages
            SonarData__Telemetry Telemetry = SONAR_DATA__TELEMETRY__INIT;
            SonarData__Georef Georef = SONAR_DATA__GEOREF__INIT;
            SonarData__Ungeoref Ungeoref = SONAR_DATA__UNGEOREF__INIT;

            int num_points = sonarpublish->n_beams;

            Ungeoref.n_pointx = num_points; Ungeoref.pointx = (float*)malloc(sizeof(float) * num_points);
            Ungeoref.n_pointy = num_points; Ungeoref.pointy = (float*)malloc(sizeof(float) * num_points);
            Ungeoref.n_beamidx = num_points; Ungeoref.beamidx = (int*)malloc(sizeof(int) * num_points);
            Ungeoref.n_quality = num_points; Ungeoref.quality = (uint32_t*)malloc(sizeof(uint32_t) * num_points);
            Ungeoref.n_intensity = num_points; Ungeoref.intensity = (float*)malloc(sizeof(float) * num_points);
            
            for (int beam_index = 0; beam_index < sonarpublish->n_beams; ++beam_index)
            {
                float sample_number = gst_sonar_format_get_measurement(format, mapinfo.data, beam_index, 0);
                float angle = gst_sonar_format_get_angle(format, mapinfo.data, beam_index);
                uint8_t quality     = gst_sonar_format_get_quality_val(format, mapinfo.data, beam_index);                
                float intensity     = gst_sonar_format_get_intensity(format, mapinfo.data, beam_index);

                float range = (sample_number * params->sound_speed) / (2 * params->sample_rate);

                // Set values for the array elements
                Ungeoref.pointx[beam_index] = sin(angle) * range * sonarpublish->zoom;
                Ungeoref.pointy[beam_index] = -cos(angle) * range * sonarpublish->zoom;
                Ungeoref.beamidx[beam_index] = beam_index;
                Ungeoref.quality[beam_index] = quality;
                Ungeoref.intensity[beam_index] = intensity;
                // printf("beamIdx=%d, PointX=%f, PointY=%f, quality=%u, intensity =%f\n", subMsg_sonarData.beamidx[beam_index], subMsg_sonarData.pointx[beam_index], subMsg_sonarData.pointy[beam_index], subMsg_sonarData.quality[beam_index], subMsg_sonarData.intensity[beam_index]);
            }

            // Initializing and populating telemetry and rawPoses subMessages
            GstTelemetryMeta* tele_meta = GST_TELEMETRY_META_GET(buf);


            SonarData__TelemetryDataPosition subMsg_tel_Position = SONAR_DATA__TELEMETRY_DATA_POSITION__INIT;
            SonarData__TelemetryDataPose subMsg_tel_Pose = SONAR_DATA__TELEMETRY_DATA_POSE__INIT;
            SonarData__TelemetryDataHeading subMsg_tel_Heading = SONAR_DATA__TELEMETRY_DATA_HEADING__INIT;
            SonarData__TelemetryDataDepth subMsg_tel_Depth = SONAR_DATA__TELEMETRY_DATA_DEPTH__INIT;
            SonarData__TelemetryDataAltitude subMsg_tel_Altitude = SONAR_DATA__TELEMETRY_DATA_ALTITUDE__INIT;

            
            if(tele_meta != NULL)
            {
                GST_INFO_OBJECT(sonarpublish, "telemetry: lat: %.6f  long: %.6f  roll: %.2f  pitch: %.2f  heading: %.2f  depth: %.2f m  altitude: %.2f m", 
                    tele_meta->tel.latitude,  tele_meta->tel.longitude,
                    tele_meta->tel.roll*rad2deg_sonarpub, tele_meta->tel.pitch*rad2deg_sonarpub,  tele_meta->tel.yaw*rad2deg_sonarpub,
                    tele_meta->tel.depth, tele_meta->tel.altitude);
                
                subMsg_tel_Position.latitude = tele_meta->tel.latitude;
                subMsg_tel_Position.longitude = tele_meta->tel.longitude;
                subMsg_tel_Position.position_timestep = 1;

                subMsg_tel_Pose.pitch = tele_meta->tel.pitch*rad2deg_sonarpub;
                subMsg_tel_Pose.roll = tele_meta->tel.roll*rad2deg_sonarpub;
                subMsg_tel_Pose.pose_timestep = 1;

                subMsg_tel_Heading.heading =  tele_meta->tel.yaw*rad2deg_sonarpub; 
                subMsg_tel_Heading.heading_timestep = 1;

                subMsg_tel_Depth.depth = tele_meta->tel.depth;
                subMsg_tel_Depth.depth_timestep = 1;

                subMsg_tel_Altitude.altitude = tele_meta->tel.altitude;
                subMsg_tel_Altitude.altitude_timestep = 1;


                bool print = 0;
                if (print == true){
                    printf("Raw angles - Roll: %f, Pitch: %f, Yaw: %f\n",
                        tele_meta->tel.raw_roll,
                        tele_meta->tel.raw_pitch,
                        tele_meta->tel.raw_yaw);
                    

                    printf("Telemetry Data:\n"
                        "Position: Latitude=%.6f  Longitude=%.6f\n"
                        "Pose: Roll=%.2f  Pitch=%.2f\n"
                        "Heading: Heading=%.2f\n"
                        "Depth: Depth=%.2f\n"
                        "Altitude: Altitude=%.2f\n",
                        subMsg_tel_Position.latitude, subMsg_tel_Position.longitude,
                        subMsg_tel_Pose.roll, subMsg_tel_Pose.pitch,
                        subMsg_tel_Heading.heading,
                        subMsg_tel_Depth.depth,
                        subMsg_tel_Altitude.altitude);
                }


            // Call the georeferencing function
            Georef_data georef_result = georeferencing(
                tele_meta->tel.roll,
                tele_meta->tel.pitch,
                tele_meta->tel.yaw,
                Ungeoref.pointx,
                Ungeoref.pointy,
                Ungeoref.n_pointx,
                tele_meta->tel.longitude,
                tele_meta->tel.latitude,
                tele_meta->tel.depth
            );
            
            Georef.x_pointcld_body = (float*)malloc(georef_result.num_points * sizeof(float));
            Georef.y_pointcld_body = (float*)malloc(georef_result.num_points * sizeof(float));
            Georef.z_pointcld_body = (float*)malloc(georef_result.num_points * sizeof(float));

            for (int i = 0; i < georef_result.num_points; i++) {
                Georef.x_pointcld_body[i] = georef_result.points_body[i][0];
                Georef.y_pointcld_body[i] = georef_result.points_body[i][1];
                Georef.z_pointcld_body[i] = georef_result.points_body[i][2];
            }

            Georef.rotationmatrix = (float*)malloc(9 * sizeof(float));

            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    Georef.rotationmatrix[i * 3 + j] = georef_result.R_BN[i][j];
                }
            }

            Georef.n_x_pointcld_body = georef_result.num_points;
            Georef.n_y_pointcld_body = georef_result.num_points;
            Georef.n_z_pointcld_body = georef_result.num_points;
            Georef.n_rotationmatrix = 9;

            Georef.x_body_position_ecef = georef_result.body_ecef[0];
            Georef.y_body_position_ecef = georef_result.body_ecef[1];
            Georef.z_body_position_ecef = georef_result.body_ecef[2];

            }
            else
            {
                if(!metadata_warning_shown_sonarpub)
                {
                    GST_INFO_OBJECT(sonarpublish, "telemetry not available");
                    printf("Tel not available\n");
                }
                metadata_warning_shown_sonarpub = true;
            }

            // Add sonarData and telemetryData to Ungeoref_And_Telemetry

            Telemetry.altitude = &subMsg_tel_Altitude;
            Telemetry.depth = &subMsg_tel_Depth;
            Telemetry.heading = &subMsg_tel_Heading;
            Telemetry.pose = &subMsg_tel_Pose;
            Telemetry.position = &subMsg_tel_Position;

            // Save data before serialization
            // saveDataToFile("Tel_data_before_serialization.json", &Ungeoref_And_Telemetry);

            // Serialize the Ungeoref message into a binary format and publish the message
            size_t packed_size_data_UnRef = sonar_data__ungeoref__get_packed_size(&Ungeoref); // serialize
            uint8_t* buffer_data_UnRef = (uint8_t*)malloc(packed_size_data_UnRef);
            sonar_data__ungeoref__pack(&Ungeoref, buffer_data_UnRef);            

            zmq_msg_t message_UnRef; // create zeromq multipart message with the Ungeoref data as one part
            zmq_msg_init_size(&message_UnRef, packed_size_data_UnRef);
            memcpy(zmq_msg_data(&message_UnRef), buffer_data_UnRef, packed_size_data_UnRef);
            
            int rc_UnRef = zmq_msg_send(&message_UnRef, sonarpublish->zmq_publisher, ZMQ_SNDMORE); // send message
            
            zmq_msg_close(&message_UnRef); // close message



            // Serialize the Telemetry message into a binary format and publish the message
            size_t packed_size_data_Tel = sonar_data__telemetry__get_packed_size(&Telemetry); // serialize
            uint8_t* buffer_data_Tel = (uint8_t*)malloc(packed_size_data_Tel);
            sonar_data__telemetry__pack(&Telemetry, buffer_data_Tel);

            zmq_msg_t message_Tel; // create zeromq multipart message with the Telemetry data as one part
            zmq_msg_init_size(&message_Tel, packed_size_data_Tel);
            memcpy(zmq_msg_data(&message_Tel), buffer_data_Tel, packed_size_data_Tel);

            int rc_Tel = zmq_msg_send(&message_Tel, sonarpublish->zmq_publisher, ZMQ_SNDMORE); // send message

            zmq_msg_close(&message_Tel); // close message


            // Serialize the Georef message into a binary format and publish the message
            size_t packed_size_data_Georef = sonar_data__georef__get_packed_size(&Georef); // serialize
            uint8_t* buffer_data_Georef = (uint8_t*)malloc(packed_size_data_Georef);
            sonar_data__georef__pack(&Georef, buffer_data_Georef);

            zmq_msg_t message_Georef; // create zeromq multipart message with the Georef data as one part
            zmq_msg_init_size(&message_Georef, packed_size_data_Georef);
            memcpy(zmq_msg_data(&message_Georef), buffer_data_Georef, packed_size_data_Georef);

            int rc_Georef = zmq_msg_send(&message_Georef, sonarpublish->zmq_publisher, 0); // send message

            zmq_msg_close(&message_Georef); // close message



            // Check for errors
            if (rc_UnRef < 0 || rc_Tel < 0 || rc_Georef < 0) {
                perror("Error sending data over ZeroMQ");
                // Handle error as needed
            }


            // Free the allocated memory and close the socket:
            free(buffer_data_UnRef);
            free(buffer_data_Tel);
            free(buffer_data_Georef);


            // Free the allocated memory (Specifically for the arrays of data, unnecessary otherwise)
            free(Ungeoref.pointx);
            free(Ungeoref.pointy);
            free(Ungeoref.beamidx);
            free(Ungeoref.quality);
            free(Ungeoref.intensity);

            free(Georef.x_pointcld_body);
            free(Georef.y_pointcld_body);
            free(Georef.z_pointcld_body);
            free(Georef.rotationmatrix);

            break;
        }
    }

    gst_buffer_unmap(buf, &mapinfo);

    GST_OBJECT_UNLOCK(sonarpublish);

    return GST_FLOW_OK;
}

static gboolean gst_sonarpublish_set_caps(GstBaseSink* basesink, GstCaps* caps)
{
    Gstsonarpublish* sonarpublish = GST_sonarpublish(basesink);

    GstStructure* s = gst_caps_get_structure(caps, 0);

    GST_DEBUG_OBJECT(sonarpublish, "caps structure: %s\n", gst_structure_to_string(s));

    gint n_beams, resolution;
    const gchar* caps_name;

    if ((caps_name = gst_structure_get_name(s)) && gst_structure_get_int(s, "n_beams", &n_beams) && gst_structure_get_int(s, "resolution", &resolution))
    {
        GST_OBJECT_LOCK(sonarpublish);
        guint32 old_n_beams    = sonarpublish->n_beams;
        guint32 old_resolution = sonarpublish->resolution;

        GST_DEBUG_OBJECT(sonarpublish, "got caps details caps_name: %s, n_beams: %d, resolution: %d", caps_name, n_beams, resolution);
        sonarpublish->n_beams    = (guint32)n_beams;
        sonarpublish->resolution = (guint32)resolution;

        if ((sonarpublish->n_beams != old_n_beams) || (sonarpublish->resolution != old_resolution))
        {
            const int size = sonarpublish->n_beams * sonarpublish->resolution * 3 * sizeof(sonarpublish->vertices[0]);

            free(sonarpublish->vertices);
            sonarpublish->vertices = (float*)malloc(size);
        }

        if (strcmp(caps_name, "sonar/multibeam") == 0)
            sonarpublish->sonar_type = GST_SONAR_TYPE_FLS;
        else if (strcmp(caps_name, "sonar/bathymetry") == 0)
            sonarpublish->sonar_type = GST_SONAR_TYPE_BATHYMETRY;
        else
            g_assert_not_reached();

        gboolean detected;
        if (gst_structure_get_boolean(s, "detected", &detected))
            sonarpublish->detected = detected;

        GST_OBJECT_UNLOCK(sonarpublish);

        return TRUE;
    }
    else
    {
        GST_DEBUG_OBJECT(sonarpublish, "no details in caps\n");

        return FALSE;
    }
}

static void gst_sonarpublish_set_property(GObject* object, guint prop_id, const GValue* value, GParamSpec* pspec)
{
    Gstsonarpublish* sonarpublish = GST_sonarpublish(object);

    GST_OBJECT_LOCK(sonarpublish);
    switch (prop_id)
    {
        case PROP_ZOOM:
            sonarpublish->zoom = g_value_get_double(value);
            break;
        case PROP_GAIN:
            sonarpublish->gain = g_value_get_double(value);
            break;
        default:
            G_OBJECT_WARN_INVALID_PROPERTY_ID(object, prop_id, pspec);
            break;
    }
    GST_OBJECT_UNLOCK(sonarpublish);
}

static void gst_sonarpublish_get_property(GObject* object, guint prop_id, GValue* value, GParamSpec* pspec)
{
    Gstsonarpublish* sonarpublish = GST_sonarpublish(object);

    switch (prop_id)
    {
        case PROP_ZOOM:
            g_value_set_double(value, sonarpublish->zoom);
            break;
        case PROP_GAIN:
            g_value_set_double(value, sonarpublish->gain);
            break;
        default:
            G_OBJECT_WARN_INVALID_PROPERTY_ID(object, prop_id, pspec);
            break;
    }
}

static void gst_sonarpublish_finalize(GObject* object)
{
    Gstsonarpublish* sonarpublish = GST_sonarpublish(object);

    free(sonarpublish->vertices);


    // ZeroMQ Cleanup (If-sentences so that it is only closed IF they were intialized/used)
    if (sonarpublish->zmq_publisher) {
        zmq_close(sonarpublish->zmq_publisher);
        sonarpublish->zmq_publisher = NULL;
        printf("Zmq closed successfully.\n");
    }
    if (sonarpublish->zmq_context) {
        zmq_ctx_destroy(sonarpublish->zmq_context);
        sonarpublish->zmq_context = NULL;
        printf("Zmq destroyed successfully.\n");
    }


    G_OBJECT_CLASS(parent_class)->finalize(object);
}

static void gst_sonarpublish_class_init(GstsonarpublishClass* klass)
{
    GObjectClass* gobject_class       = (GObjectClass*)klass;
    GstElementClass* gstelement_class = (GstElementClass*)klass;
    GstBaseSinkClass* basesink_class  = (GstBaseSinkClass*)klass;

    gobject_class->finalize     = gst_sonarpublish_finalize;
    gobject_class->set_property = gst_sonarpublish_set_property;
    gobject_class->get_property = gst_sonarpublish_get_property;

    basesink_class->render   = GST_DEBUG_FUNCPTR(gst_sonarpublish_render);
    basesink_class->set_caps = GST_DEBUG_FUNCPTR(gst_sonarpublish_set_caps);

    GST_DEBUG_CATEGORY_INIT(sonarpublish_debug, "sonarpublish", 0, "sonarpublish");

    g_object_class_install_property(G_OBJECT_CLASS(klass), PROP_ZOOM,
        g_param_spec_double("zoom", "zoom", "Zoom", G_MINDOUBLE, G_MAXDOUBLE, DEFAULT_PROP_ZOOM, G_PARAM_READWRITE | GST_PARAM_CONTROLLABLE | G_PARAM_STATIC_STRINGS));

    g_object_class_install_property(G_OBJECT_CLASS(klass), PROP_GAIN,
        g_param_spec_double("gain", "gain", "Gain", G_MINDOUBLE, G_MAXDOUBLE, DEFAULT_PROP_GAIN, G_PARAM_READWRITE | GST_PARAM_CONTROLLABLE | G_PARAM_STATIC_STRINGS));

    gst_element_class_set_static_metadata(gstelement_class, "sonarpublish", "Sink", "visualizes sonar data", "Eelume AS <opensource@eelume.com>");

    gst_element_class_add_static_pad_template(gstelement_class, &gst_sonarpublish_sink_template);
}

static void gst_sonarpublish_init(Gstsonarpublish* sonarpublish)
{
    sonarpublish->n_beams    = 0;
    sonarpublish->resolution = 0;
    sonarpublish->detected   = FALSE;
    sonarpublish->vertices   = NULL;
    sonarpublish->playpause  = GST_STATE_PAUSED;

    sonarpublish->zoom = DEFAULT_PROP_ZOOM;
    sonarpublish->gain = DEFAULT_PROP_GAIN;

    // ZeroMQ Initialization
    sonarpublish->zmq_context = zmq_ctx_new();
    sonarpublish->zmq_publisher = zmq_socket(sonarpublish->zmq_context, ZMQ_PUB);
    zmq_bind(sonarpublish->zmq_publisher, "tcp://*:5555"); // Adjust the address/port as needed

}

