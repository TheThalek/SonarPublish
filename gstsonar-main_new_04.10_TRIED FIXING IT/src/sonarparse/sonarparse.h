// ***************************************************************************
// Part of Gstsonar - Gstreamer sonar processing plugins
//
// Copyright (c) 2023 Eelume AS <opensource@eelume.com>
// All rights reserved
//
// Licensed under the LGPL v2.1 License.
// See LICENSE file in the project root for full license information.
// ***************************************************************************
#ifndef __GST_sonarparse_H__
#define __GST_sonarparse_H__

#include <gst/base/gstbaseparse.h>
#include <gst/gst.h>

#include "common/sonarmeta.h"
#include "norbit_wbms.h"

G_BEGIN_DECLS

// sonarparse
#define GST_TYPE_sonarparse            (gst_sonarparse_get_type())
#define GST_sonarparse(obj)            (G_TYPE_CHECK_INSTANCE_CAST((obj), GST_TYPE_sonarparse, Gstsonarparse))
#define GST_sonarparse_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass), GST_TYPE_sonarparse, GstsonarparseClass))
#define GST_IS_sonarparse(obj)         (G_TYPE_CHECK_INSTANCE_TYPE((obj), GST_TYPE_sonarparse))
#define GST_IS_sonarparse_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass), GST_TYPE_sonarparse))

typedef struct _Gstsonarparse Gstsonarparse;
typedef struct _GstsonarparseClass GstsonarparseClass;

struct _Gstsonarparse
{
    GstBaseParse baseparse;

    /* < private > */
    guint32 n_beams;
    guint32 resolution;
    guint32 framerate;
    gchar* caps_name;

    guint64 initial_time;

    GstSonarMeta next_meta;
};

struct _GstsonarparseClass
{
    GstBaseParseClass parent_class;
};

GType gst_sonarparse_get_type(void);

G_END_DECLS

#endif /* __GST_sonarparse_H__ */
