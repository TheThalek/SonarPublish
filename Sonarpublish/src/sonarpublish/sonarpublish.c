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

#include "sonarpublish.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>    // Include the socket functions
#include <sys/un.h>        // Include the Unix domain socket functions
#include "sonarData.pb-c.h"

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

// // Define a struct to store point data
// typedef struct {
//     float x;
//     float y;
// } Point;





#define DEFAULT_PROP_ZOOM 1
#define DEFAULT_PROP_GAIN 1

static GstStaticPadTemplate gst_sonarpublish_sink_template = GST_STATIC_PAD_TEMPLATE("sink", GST_PAD_SINK, GST_PAD_ALWAYS, GST_STATIC_CAPS("sonar/multibeam ; sonar/bathymetry"));


static GstFlowReturn gst_sonarpublish_render(GstBaseSink* basesink, GstBuffer* buf)
{
    Gstsonarpublish* sonarpublish = GST_sonarpublish(basesink);

    GST_OBJECT_LOCK(sonarpublish);

    // GstSonarMeta *meta = GST_SONAR_META_GET(buf);
    const GstSonarMeta* meta     = GST_SONAR_META_GET(buf);
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

            // Initialize a Point message
            SonarData__SonarData sonar_data = SONAR_DATA__SONAR_DATA__INIT;

            int num_points = sonarpublish->n_beams;

            // Allocate memory for arrays
            sonar_data.n_pointx = num_points;
            sonar_data.pointx = (float*)malloc(sizeof(float) * num_points);
            sonar_data.n_pointy = num_points;
            sonar_data.pointy = (float*)malloc(sizeof(float) * num_points);
            sonar_data.n_beamidx = num_points;
            sonar_data.beamidx = (int*)malloc(sizeof(int) * num_points);


            for (int beam_index = 0; beam_index < sonarpublish->n_beams; ++beam_index)
            {
                float sample_number = gst_sonar_format_get_measurement(format, mapinfo.data, beam_index, 0);
                float angle = gst_sonar_format_get_angle(format, mapinfo.data, beam_index);
                float range = (sample_number * params->sound_speed) / (2 * params->sample_rate);

                // int vertex_index = 3 * beam_index;
                // float* vertex    = sonarpublish->vertices + vertex_index;
                // vertex[0] = sin(angle) * range * sonarpublish->zoom;
                // vertex[1] = -cos(angle) * range * sonarpublish->zoom;
                // vertex[2] = -1;
                // printf("Bath: The BeamIdx is: %d\n", beam_index);
                // printf("Bath: The vertex[0] are: %f\n", vertex[0]);
                // printf("Bath: The vertex[1] are: %f\n", vertex[1]);

                // Set values for the array elements
                sonar_data.pointx[beam_index] = sin(angle) * range * sonarpublish->zoom;
                sonar_data.pointy[beam_index] = -cos(angle) * range * sonarpublish->zoom;
                sonar_data.beamidx[beam_index] = beam_index;

                printf("Bath: The pointx are: %f\n", sonar_data.pointx[beam_index]); 
                printf("Bath: The pointy are: %f\n", sonar_data.pointy[beam_index]); 
                printf("Bath: The beam_index are: %d\n", sonar_data.beamidx[beam_index]); 
            }

            // Serialize the message into a binary format. 
            size_t packed_size = sonar_data__sonar_data__get_packed_size(&sonar_data);
            printf("Packed size of sonar_data: %zu bytes\n", packed_size);
            uint8_t* buffer = (uint8_t*)malloc(packed_size);
            sonar_data__sonar_data__pack(&sonar_data, buffer);

            //Create a socket and establish a connection to your Python script's Unix domain socket:
            int sockfd = socket(AF_UNIX, SOCK_STREAM, 0); // Create a Unix domain socket
            struct sockaddr_un server_address;
            server_address.sun_family = AF_UNIX;
            strcpy(server_address.sun_path, "/tmp/socket_sonar"); // Adjust the socket path

            if (connect(sockfd, (struct sockaddr*)&server_address, sizeof(server_address)) < 0) {
                perror("Error connecting to the socket");
                return -1;
            }

            //Send the serialized data over the socket:
            if (send(sockfd, buffer, packed_size, 0) < 0) {
                perror("Error sending data over the socket");
                return -1;
            }

            // Free the allocated memory and close the socket:
            free(buffer);
            close(sockfd);

            // Free the allocated memory 
            free(sonar_data.pointx);
            free(sonar_data.pointy);
            free(sonar_data.beamidx);
            break;
        }
    }

    gst_buffer_unmap(buf, &mapinfo);

    // update graphic MAYBE ADD THE UPDATE THINGS CODE HERE;

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
}
