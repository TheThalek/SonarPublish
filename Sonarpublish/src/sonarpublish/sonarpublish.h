// ***************************************************************************
// Part of Gstsonar - Gstreamer sonar processing plugins
//
// Copyright (c) 2023 Eelume AS <opensource@eelume.com>
// All rights reserved
//
// Licensed under the LGPL v2.1 License.
// See LICENSE file in the project root for full license information.
// ***************************************************************************
#ifndef __GST_sonarpublish_H__
#define __GST_sonarpublish_H__

#include <gst/base/gstbasesink.h>
#include <gst/gst.h>

#include "common/sonarmeta.h"

G_BEGIN_DECLS

#define GST_TYPE_sonarpublish            (gst_sonarpublish_get_type())
#define GST_sonarpublish(obj)            (G_TYPE_CHECK_INSTANCE_CAST((obj), GST_TYPE_sonarpublish, Gstsonarpublish))
#define GST_sonarpublish_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass), GST_TYPE_sonarpublish, GstsonarpublishClass))
#define GST_IS_sonarpublish(obj)         (G_TYPE_CHECK_INSTANCE_TYPE((obj), GST_TYPE_sonarpublish))
#define GST_IS_sonarpublish_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass), GST_TYPE_sonarpublish))

typedef struct _Gstsonarpublish Gstsonarpublish;
typedef struct _GstsonarpublishClass GstsonarpublishClass;



struct _Gstsonarpublish
{
    GstBaseSink basesink;

    /* < private > */
    GstSonarType sonar_type;
    guint32 n_beams;
    guint32 resolution;
    gboolean detected;    // if detection was run on the data

    float* vertices;
    float* colors;

    // initializer flag for openglWp
    int init_wp;

    GstState playpause;    // which state to set on next space press

    float zoom;    // factor to scale ranges with
    float gain;    // factor to scale intensities with
};

struct _GstsonarpublishClass
{
    GstBaseSinkClass parent_class;
};

GType gst_sonarpublish_get_type(void);

G_END_DECLS

#endif /* __GST_sonarpublish_H__ */
