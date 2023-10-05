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

#include "sonarsink.h"

#include <stdio.h>
#include <math.h>


GST_DEBUG_CATEGORY_STATIC(sonarsink_debug);
#define GST_CAT_DEFAULT sonarsink_debug

#define gst_sonarsink_parent_class parent_class
G_DEFINE_TYPE(GstSonarsink, gst_sonarsink, GST_TYPE_BASE_SINK);


static GstStaticPadTemplate gst_sonarsink_sink_template = GST_STATIC_PAD_TEMPLATE("sink", GST_PAD_SINK, GST_PAD_ALWAYS, GST_STATIC_CAPS("sonar/multibeam ; sonar/bathymetry"));

static GstFlowReturn gst_sonarsink_render(GstBaseSink* basesink, GstBuffer* buf)
{
    GstSonarsink* sonarsink = GST_SONARSINK(basesink);

    GST_OBJECT_LOCK(sonarsink);

    // GstSonarMeta *meta = GST_SONAR_META_GET(buf);
    const GstSonarMeta* meta     = GST_SONAR_META_GET(buf);
    const GstSonarFormat* format = &meta->format;
    const GstSonarParams* params = &meta->params;

    GST_DEBUG_OBJECT(sonarsink, "%lu: rendering buffer: %p, width n_beams = %d, resolution = %d, sound_speed = %f, sample_rate = %f, t0 = %d", buf->pts, buf, sonarsink->n_beams,
        sonarsink->resolution, params->sound_speed, params->sample_rate, params->t0);

    GstMapInfo mapinfo;
    if (!gst_buffer_map(buf, &mapinfo, GST_MAP_READ))
    {
        GST_OBJECT_UNLOCK(sonarsink);
        return GST_FLOW_ERROR;
    }

    switch (sonarsink->sonar_type)
    {
        case GST_SONAR_TYPE_FLS: // "Forward Looking Sonar"
        {
            const float max_range = ((params->t0 + sonarsink->resolution) * params->sound_speed) / (2 * params->sample_rate);

            for (int range_index = 0; range_index < sonarsink->resolution; ++range_index)
            {
                for (int beam_index = 0; beam_index < sonarsink->n_beams; ++beam_index)
                {
                    float beam_intensity = gst_sonar_format_get_measurement(format, mapinfo.data, beam_index, range_index);
                    float beam_angle     = gst_sonar_format_get_angle(format, mapinfo.data, beam_index);
                    float range          = ((params->t0 + range_index) * params->sound_speed) / (2 * params->sample_rate);

                    float range_norm = range / max_range;

                    printf("FLS: The beam_index is: %d\n", beam_index);
                    printf("FLS: The intensity is: %f\n", beam_intensity);
                    printf("Bath: The range is: %f\n", range);
                    int res = sonarsink->resolution;
                    printf("Bath: The res is: %d\n", res);

                }
            }
            break;
        }

        case GST_SONAR_TYPE_BATHYMETRY: //nyhavna og airplane er her. Bathymetry; "Measurement of depth of lakes and oceans"
        {
            //g_assert(sonarsink->resolution == 1);

            const float max_range = ((params->t0 + sonarsink->resolution) * params->sound_speed) / (2 * params->sample_rate);
            printf("Params before:");
            printf("Bath: The max_range is: %f\n", max_range);
            printf("Bath: The params->t0 is: %d\n", params->t0);
            printf("Bath: The sonarsink->resolution is: %d\n", sonarsink->resolution);
            printf("Bath: The params->sound_speed is: %f\n", params->sound_speed);
            printf("Bath: The params->sample_rate is: %f\n", params->sample_rate);

            int max_range_index = sonarsink->resolution;
            int num_of_beams = sonarsink->n_beams;

            double x[max_range_index][num_of_beams]; //[beam, range]
            double y[max_range_index][num_of_beams];

            for (int range_index = 0; range_index < sonarsink->resolution; ++range_index){
                for (int beam_index = 0; beam_index < num_of_beams; ++beam_index){

                    float beam_intensity = gst_sonar_format_get_measurement(format, mapinfo.data, beam_index, range_index);
                    float beam_angle     = gst_sonar_format_get_angle(format, mapinfo.data, beam_index);
                    float range          = ((params->t0 + range_index) * params->sound_speed) / (2 * params->sample_rate);

                    printf("Params after, in loop:\n");
                    printf("Bath: The max_range_index is: %d\n", max_range_index);
                    printf("Bath: The params->t0 is: %d\n", params->t0);
                    printf("Bath: The range_index is: %d\n", range_index);
                    printf("Bath: The params->sound_speed is: %f\n", params->sound_speed);
                    printf("Bath: The params->sample_rate is: %f\n", params->sample_rate);
                    printf("Bath: The range is: %f\n", range);

                    int vertex_index = 3 * (beam_index * sonarsink->resolution + range_index);
                    float* vertex    = sonarsink->vertices + vertex_index;

                    float range_norm = range / max_range;
                    printf("Bath: The beam_index is: %d\n", beam_index);
                    //printf("Bath: The intensity is: %f\n", beam_intensity);
                    printf("Bath: The angle is: %f\n", beam_angle);
                    
                    x[range_index][beam_index] = range*cos(beam_angle);
                    printf("Bath: The x is: %f\n", x[range_index][beam_index]);
                    y[range_index][beam_index] = range*sin(beam_angle);
                    printf("Bath: The y is: %f\n", y[range_index][beam_index]);
                }
            }

            break;
        }
    }

    gst_buffer_unmap(buf, &mapinfo);
    GST_OBJECT_UNLOCK(sonarsink);
    return GST_FLOW_OK;
}

static gboolean gst_sonarsink_set_caps(GstBaseSink* basesink, GstCaps* caps)
{
    GstSonarsink* sonarsink = GST_SONARSINK(basesink);

    GstStructure* s = gst_caps_get_structure(caps, 0);

    GST_DEBUG_OBJECT(sonarsink, "caps structure: %s\n", gst_structure_to_string(s));

    gint n_beams, resolution;
    const gchar* caps_name;

    if ((caps_name = gst_structure_get_name(s)) && gst_structure_get_int(s, "n_beams", &n_beams) && gst_structure_get_int(s, "resolution", &resolution))
    {
        GST_OBJECT_LOCK(sonarsink);
        guint32 old_n_beams    = sonarsink->n_beams;
        guint32 old_resolution = sonarsink->resolution;

        GST_DEBUG_OBJECT(sonarsink, "got caps details caps_name: %s, n_beams: %d, resolution: %d", caps_name, n_beams, resolution);
        sonarsink->n_beams    = (guint32)n_beams;
        sonarsink->resolution = (guint32)resolution;

        if (strcmp(caps_name, "sonar/multibeam") == 0)
            sonarsink->sonar_type = GST_SONAR_TYPE_FLS;
        else if (strcmp(caps_name, "sonar/bathymetry") == 0)
            sonarsink->sonar_type = GST_SONAR_TYPE_BATHYMETRY;
        else
            g_assert_not_reached();

        GST_OBJECT_UNLOCK(sonarsink);

        return TRUE;
    }
    else
    {
        GST_DEBUG_OBJECT(sonarsink, "no details in caps\n");
        return FALSE;
    }
}

static void gst_sonarsink_set_property(GObject* object, guint prop_id, const GValue* value, GParamSpec* pspec)
{
    GstSonarsink* sonarsink = GST_SONARSINK(object);

}

static void gst_sonarsink_get_property(GObject* object, guint prop_id, GValue* value, GParamSpec* pspec)
{
    GstSonarsink* sonarsink = GST_SONARSINK(object);

}

static void gst_sonarsink_finalize(GObject* object)
{
    GstSonarsink* sonarsink = GST_SONARSINK(object);

    G_OBJECT_CLASS(parent_class)->finalize(object);
}

static void gst_sonarsink_class_init(GstSonarsinkClass* klass)
{
    GObjectClass* gobject_class       = (GObjectClass*)klass;
    GstElementClass* gstelement_class = (GstElementClass*)klass;
    GstBaseSinkClass* basesink_class  = (GstBaseSinkClass*)klass;

    gobject_class->finalize     = gst_sonarsink_finalize;
    gobject_class->set_property = gst_sonarsink_set_property;
    gobject_class->get_property = gst_sonarsink_get_property;

    basesink_class->render   = GST_DEBUG_FUNCPTR(gst_sonarsink_render);
    basesink_class->set_caps = GST_DEBUG_FUNCPTR(gst_sonarsink_set_caps);

    GST_DEBUG_CATEGORY_INIT(sonarsink_debug, "sonarsink", 0, "sonarsink");

    gst_element_class_set_static_metadata(gstelement_class, "Sonarsink", "Sink", "sends sonar data", "Thale Eliassen Fink <finkthale@gamail.com>");

    gst_element_class_add_static_pad_template(gstelement_class, &gst_sonarsink_sink_template);
}

static void gst_sonarsink_init(GstSonarsink* sonarsink)
{
    sonarsink->n_beams    = 0;
    sonarsink->resolution = 0;
    sonarsink->vertices   = NULL;
    sonarsink->playpause  = GST_STATE_PAUSED;

}
