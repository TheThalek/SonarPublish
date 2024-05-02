/* Generated by the protocol buffer compiler.  DO NOT EDIT! */
/* Generated from: sonarData.proto */

/* Do not generate deprecated warnings for self */
#ifndef PROTOBUF_C__NO_DEPRECATED
#define PROTOBUF_C__NO_DEPRECATED
#endif

#include "sonarData.pb-c.h"
void   sonar_data__georef__ned__init
                     (SonarData__GeorefNED         *message)
{
  static const SonarData__GeorefNED init_value = SONAR_DATA__GEOREF__NED__INIT;
  *message = init_value;
}
size_t sonar_data__georef__ned__get_packed_size
                     (const SonarData__GeorefNED *message)
{
  assert(message->base.descriptor == &sonar_data__georef__ned__descriptor);
  return protobuf_c_message_get_packed_size ((const ProtobufCMessage*)(message));
}
size_t sonar_data__georef__ned__pack
                     (const SonarData__GeorefNED *message,
                      uint8_t       *out)
{
  assert(message->base.descriptor == &sonar_data__georef__ned__descriptor);
  return protobuf_c_message_pack ((const ProtobufCMessage*)message, out);
}
size_t sonar_data__georef__ned__pack_to_buffer
                     (const SonarData__GeorefNED *message,
                      ProtobufCBuffer *buffer)
{
  assert(message->base.descriptor == &sonar_data__georef__ned__descriptor);
  return protobuf_c_message_pack_to_buffer ((const ProtobufCMessage*)message, buffer);
}
SonarData__GeorefNED *
       sonar_data__georef__ned__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data)
{
  return (SonarData__GeorefNED *)
     protobuf_c_message_unpack (&sonar_data__georef__ned__descriptor,
                                allocator, len, data);
}
void   sonar_data__georef__ned__free_unpacked
                     (SonarData__GeorefNED *message,
                      ProtobufCAllocator *allocator)
{
  if(!message)
    return;
  assert(message->base.descriptor == &sonar_data__georef__ned__descriptor);
  protobuf_c_message_free_unpacked ((ProtobufCMessage*)message, allocator);
}
void   sonar_data__georef__ecef__init
                     (SonarData__GeorefECEF         *message)
{
  static const SonarData__GeorefECEF init_value = SONAR_DATA__GEOREF__ECEF__INIT;
  *message = init_value;
}
size_t sonar_data__georef__ecef__get_packed_size
                     (const SonarData__GeorefECEF *message)
{
  assert(message->base.descriptor == &sonar_data__georef__ecef__descriptor);
  return protobuf_c_message_get_packed_size ((const ProtobufCMessage*)(message));
}
size_t sonar_data__georef__ecef__pack
                     (const SonarData__GeorefECEF *message,
                      uint8_t       *out)
{
  assert(message->base.descriptor == &sonar_data__georef__ecef__descriptor);
  return protobuf_c_message_pack ((const ProtobufCMessage*)message, out);
}
size_t sonar_data__georef__ecef__pack_to_buffer
                     (const SonarData__GeorefECEF *message,
                      ProtobufCBuffer *buffer)
{
  assert(message->base.descriptor == &sonar_data__georef__ecef__descriptor);
  return protobuf_c_message_pack_to_buffer ((const ProtobufCMessage*)message, buffer);
}
SonarData__GeorefECEF *
       sonar_data__georef__ecef__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data)
{
  return (SonarData__GeorefECEF *)
     protobuf_c_message_unpack (&sonar_data__georef__ecef__descriptor,
                                allocator, len, data);
}
void   sonar_data__georef__ecef__free_unpacked
                     (SonarData__GeorefECEF *message,
                      ProtobufCAllocator *allocator)
{
  if(!message)
    return;
  assert(message->base.descriptor == &sonar_data__georef__ecef__descriptor);
  protobuf_c_message_free_unpacked ((ProtobufCMessage*)message, allocator);
}
void   sonar_data__telemetry__init
                     (SonarData__Telemetry         *message)
{
  static const SonarData__Telemetry init_value = SONAR_DATA__TELEMETRY__INIT;
  *message = init_value;
}
size_t sonar_data__telemetry__get_packed_size
                     (const SonarData__Telemetry *message)
{
  assert(message->base.descriptor == &sonar_data__telemetry__descriptor);
  return protobuf_c_message_get_packed_size ((const ProtobufCMessage*)(message));
}
size_t sonar_data__telemetry__pack
                     (const SonarData__Telemetry *message,
                      uint8_t       *out)
{
  assert(message->base.descriptor == &sonar_data__telemetry__descriptor);
  return protobuf_c_message_pack ((const ProtobufCMessage*)message, out);
}
size_t sonar_data__telemetry__pack_to_buffer
                     (const SonarData__Telemetry *message,
                      ProtobufCBuffer *buffer)
{
  assert(message->base.descriptor == &sonar_data__telemetry__descriptor);
  return protobuf_c_message_pack_to_buffer ((const ProtobufCMessage*)message, buffer);
}
SonarData__Telemetry *
       sonar_data__telemetry__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data)
{
  return (SonarData__Telemetry *)
     protobuf_c_message_unpack (&sonar_data__telemetry__descriptor,
                                allocator, len, data);
}
void   sonar_data__telemetry__free_unpacked
                     (SonarData__Telemetry *message,
                      ProtobufCAllocator *allocator)
{
  if(!message)
    return;
  assert(message->base.descriptor == &sonar_data__telemetry__descriptor);
  protobuf_c_message_free_unpacked ((ProtobufCMessage*)message, allocator);
}
void   sonar_data__telemetry_data_position__init
                     (SonarData__TelemetryDataPosition         *message)
{
  static const SonarData__TelemetryDataPosition init_value = SONAR_DATA__TELEMETRY_DATA_POSITION__INIT;
  *message = init_value;
}
size_t sonar_data__telemetry_data_position__get_packed_size
                     (const SonarData__TelemetryDataPosition *message)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_position__descriptor);
  return protobuf_c_message_get_packed_size ((const ProtobufCMessage*)(message));
}
size_t sonar_data__telemetry_data_position__pack
                     (const SonarData__TelemetryDataPosition *message,
                      uint8_t       *out)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_position__descriptor);
  return protobuf_c_message_pack ((const ProtobufCMessage*)message, out);
}
size_t sonar_data__telemetry_data_position__pack_to_buffer
                     (const SonarData__TelemetryDataPosition *message,
                      ProtobufCBuffer *buffer)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_position__descriptor);
  return protobuf_c_message_pack_to_buffer ((const ProtobufCMessage*)message, buffer);
}
SonarData__TelemetryDataPosition *
       sonar_data__telemetry_data_position__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data)
{
  return (SonarData__TelemetryDataPosition *)
     protobuf_c_message_unpack (&sonar_data__telemetry_data_position__descriptor,
                                allocator, len, data);
}
void   sonar_data__telemetry_data_position__free_unpacked
                     (SonarData__TelemetryDataPosition *message,
                      ProtobufCAllocator *allocator)
{
  if(!message)
    return;
  assert(message->base.descriptor == &sonar_data__telemetry_data_position__descriptor);
  protobuf_c_message_free_unpacked ((ProtobufCMessage*)message, allocator);
}
void   sonar_data__telemetry_data_pose__init
                     (SonarData__TelemetryDataPose         *message)
{
  static const SonarData__TelemetryDataPose init_value = SONAR_DATA__TELEMETRY_DATA_POSE__INIT;
  *message = init_value;
}
size_t sonar_data__telemetry_data_pose__get_packed_size
                     (const SonarData__TelemetryDataPose *message)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_pose__descriptor);
  return protobuf_c_message_get_packed_size ((const ProtobufCMessage*)(message));
}
size_t sonar_data__telemetry_data_pose__pack
                     (const SonarData__TelemetryDataPose *message,
                      uint8_t       *out)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_pose__descriptor);
  return protobuf_c_message_pack ((const ProtobufCMessage*)message, out);
}
size_t sonar_data__telemetry_data_pose__pack_to_buffer
                     (const SonarData__TelemetryDataPose *message,
                      ProtobufCBuffer *buffer)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_pose__descriptor);
  return protobuf_c_message_pack_to_buffer ((const ProtobufCMessage*)message, buffer);
}
SonarData__TelemetryDataPose *
       sonar_data__telemetry_data_pose__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data)
{
  return (SonarData__TelemetryDataPose *)
     protobuf_c_message_unpack (&sonar_data__telemetry_data_pose__descriptor,
                                allocator, len, data);
}
void   sonar_data__telemetry_data_pose__free_unpacked
                     (SonarData__TelemetryDataPose *message,
                      ProtobufCAllocator *allocator)
{
  if(!message)
    return;
  assert(message->base.descriptor == &sonar_data__telemetry_data_pose__descriptor);
  protobuf_c_message_free_unpacked ((ProtobufCMessage*)message, allocator);
}
void   sonar_data__telemetry_data_heading__init
                     (SonarData__TelemetryDataHeading         *message)
{
  static const SonarData__TelemetryDataHeading init_value = SONAR_DATA__TELEMETRY_DATA_HEADING__INIT;
  *message = init_value;
}
size_t sonar_data__telemetry_data_heading__get_packed_size
                     (const SonarData__TelemetryDataHeading *message)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_heading__descriptor);
  return protobuf_c_message_get_packed_size ((const ProtobufCMessage*)(message));
}
size_t sonar_data__telemetry_data_heading__pack
                     (const SonarData__TelemetryDataHeading *message,
                      uint8_t       *out)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_heading__descriptor);
  return protobuf_c_message_pack ((const ProtobufCMessage*)message, out);
}
size_t sonar_data__telemetry_data_heading__pack_to_buffer
                     (const SonarData__TelemetryDataHeading *message,
                      ProtobufCBuffer *buffer)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_heading__descriptor);
  return protobuf_c_message_pack_to_buffer ((const ProtobufCMessage*)message, buffer);
}
SonarData__TelemetryDataHeading *
       sonar_data__telemetry_data_heading__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data)
{
  return (SonarData__TelemetryDataHeading *)
     protobuf_c_message_unpack (&sonar_data__telemetry_data_heading__descriptor,
                                allocator, len, data);
}
void   sonar_data__telemetry_data_heading__free_unpacked
                     (SonarData__TelemetryDataHeading *message,
                      ProtobufCAllocator *allocator)
{
  if(!message)
    return;
  assert(message->base.descriptor == &sonar_data__telemetry_data_heading__descriptor);
  protobuf_c_message_free_unpacked ((ProtobufCMessage*)message, allocator);
}
void   sonar_data__telemetry_data_depth__init
                     (SonarData__TelemetryDataDepth         *message)
{
  static const SonarData__TelemetryDataDepth init_value = SONAR_DATA__TELEMETRY_DATA_DEPTH__INIT;
  *message = init_value;
}
size_t sonar_data__telemetry_data_depth__get_packed_size
                     (const SonarData__TelemetryDataDepth *message)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_depth__descriptor);
  return protobuf_c_message_get_packed_size ((const ProtobufCMessage*)(message));
}
size_t sonar_data__telemetry_data_depth__pack
                     (const SonarData__TelemetryDataDepth *message,
                      uint8_t       *out)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_depth__descriptor);
  return protobuf_c_message_pack ((const ProtobufCMessage*)message, out);
}
size_t sonar_data__telemetry_data_depth__pack_to_buffer
                     (const SonarData__TelemetryDataDepth *message,
                      ProtobufCBuffer *buffer)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_depth__descriptor);
  return protobuf_c_message_pack_to_buffer ((const ProtobufCMessage*)message, buffer);
}
SonarData__TelemetryDataDepth *
       sonar_data__telemetry_data_depth__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data)
{
  return (SonarData__TelemetryDataDepth *)
     protobuf_c_message_unpack (&sonar_data__telemetry_data_depth__descriptor,
                                allocator, len, data);
}
void   sonar_data__telemetry_data_depth__free_unpacked
                     (SonarData__TelemetryDataDepth *message,
                      ProtobufCAllocator *allocator)
{
  if(!message)
    return;
  assert(message->base.descriptor == &sonar_data__telemetry_data_depth__descriptor);
  protobuf_c_message_free_unpacked ((ProtobufCMessage*)message, allocator);
}
void   sonar_data__telemetry_data_altitude__init
                     (SonarData__TelemetryDataAltitude         *message)
{
  static const SonarData__TelemetryDataAltitude init_value = SONAR_DATA__TELEMETRY_DATA_ALTITUDE__INIT;
  *message = init_value;
}
size_t sonar_data__telemetry_data_altitude__get_packed_size
                     (const SonarData__TelemetryDataAltitude *message)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_altitude__descriptor);
  return protobuf_c_message_get_packed_size ((const ProtobufCMessage*)(message));
}
size_t sonar_data__telemetry_data_altitude__pack
                     (const SonarData__TelemetryDataAltitude *message,
                      uint8_t       *out)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_altitude__descriptor);
  return protobuf_c_message_pack ((const ProtobufCMessage*)message, out);
}
size_t sonar_data__telemetry_data_altitude__pack_to_buffer
                     (const SonarData__TelemetryDataAltitude *message,
                      ProtobufCBuffer *buffer)
{
  assert(message->base.descriptor == &sonar_data__telemetry_data_altitude__descriptor);
  return protobuf_c_message_pack_to_buffer ((const ProtobufCMessage*)message, buffer);
}
SonarData__TelemetryDataAltitude *
       sonar_data__telemetry_data_altitude__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data)
{
  return (SonarData__TelemetryDataAltitude *)
     protobuf_c_message_unpack (&sonar_data__telemetry_data_altitude__descriptor,
                                allocator, len, data);
}
void   sonar_data__telemetry_data_altitude__free_unpacked
                     (SonarData__TelemetryDataAltitude *message,
                      ProtobufCAllocator *allocator)
{
  if(!message)
    return;
  assert(message->base.descriptor == &sonar_data__telemetry_data_altitude__descriptor);
  protobuf_c_message_free_unpacked ((ProtobufCMessage*)message, allocator);
}
void   sonar_data__ungeoref__init
                     (SonarData__Ungeoref         *message)
{
  static const SonarData__Ungeoref init_value = SONAR_DATA__UNGEOREF__INIT;
  *message = init_value;
}
size_t sonar_data__ungeoref__get_packed_size
                     (const SonarData__Ungeoref *message)
{
  assert(message->base.descriptor == &sonar_data__ungeoref__descriptor);
  return protobuf_c_message_get_packed_size ((const ProtobufCMessage*)(message));
}
size_t sonar_data__ungeoref__pack
                     (const SonarData__Ungeoref *message,
                      uint8_t       *out)
{
  assert(message->base.descriptor == &sonar_data__ungeoref__descriptor);
  return protobuf_c_message_pack ((const ProtobufCMessage*)message, out);
}
size_t sonar_data__ungeoref__pack_to_buffer
                     (const SonarData__Ungeoref *message,
                      ProtobufCBuffer *buffer)
{
  assert(message->base.descriptor == &sonar_data__ungeoref__descriptor);
  return protobuf_c_message_pack_to_buffer ((const ProtobufCMessage*)message, buffer);
}
SonarData__Ungeoref *
       sonar_data__ungeoref__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data)
{
  return (SonarData__Ungeoref *)
     protobuf_c_message_unpack (&sonar_data__ungeoref__descriptor,
                                allocator, len, data);
}
void   sonar_data__ungeoref__free_unpacked
                     (SonarData__Ungeoref *message,
                      ProtobufCAllocator *allocator)
{
  if(!message)
    return;
  assert(message->base.descriptor == &sonar_data__ungeoref__descriptor);
  protobuf_c_message_free_unpacked ((ProtobufCMessage*)message, allocator);
}
static const ProtobufCFieldDescriptor sonar_data__georef__ned__field_descriptors[4] =
{
  {
    "x_pointCld_body_NED",
    1,
    PROTOBUF_C_LABEL_REPEATED,
    PROTOBUF_C_TYPE_FLOAT,
    offsetof(SonarData__GeorefNED, n_x_pointcld_body_ned),
    offsetof(SonarData__GeorefNED, x_pointcld_body_ned),
    NULL,
    NULL,
    0 | PROTOBUF_C_FIELD_FLAG_PACKED,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "y_pointCld_body_NED",
    2,
    PROTOBUF_C_LABEL_REPEATED,
    PROTOBUF_C_TYPE_FLOAT,
    offsetof(SonarData__GeorefNED, n_y_pointcld_body_ned),
    offsetof(SonarData__GeorefNED, y_pointcld_body_ned),
    NULL,
    NULL,
    0 | PROTOBUF_C_FIELD_FLAG_PACKED,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "z_pointCld_body_NED",
    3,
    PROTOBUF_C_LABEL_REPEATED,
    PROTOBUF_C_TYPE_FLOAT,
    offsetof(SonarData__GeorefNED, n_z_pointcld_body_ned),
    offsetof(SonarData__GeorefNED, z_pointcld_body_ned),
    NULL,
    NULL,
    0 | PROTOBUF_C_FIELD_FLAG_PACKED,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "rotationMatrix_NED",
    4,
    PROTOBUF_C_LABEL_REPEATED,
    PROTOBUF_C_TYPE_FLOAT,
    offsetof(SonarData__GeorefNED, n_rotationmatrix_ned),
    offsetof(SonarData__GeorefNED, rotationmatrix_ned),
    NULL,
    NULL,
    0 | PROTOBUF_C_FIELD_FLAG_PACKED,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
};
static const unsigned sonar_data__georef__ned__field_indices_by_name[] = {
  3,   /* field[3] = rotationMatrix_NED */
  0,   /* field[0] = x_pointCld_body_NED */
  1,   /* field[1] = y_pointCld_body_NED */
  2,   /* field[2] = z_pointCld_body_NED */
};
static const ProtobufCIntRange sonar_data__georef__ned__number_ranges[1 + 1] =
{
  { 1, 0 },
  { 0, 4 }
};
const ProtobufCMessageDescriptor sonar_data__georef__ned__descriptor =
{
  PROTOBUF_C__MESSAGE_DESCRIPTOR_MAGIC,
  "sonarData.Georef_NED",
  "GeorefNED",
  "SonarData__GeorefNED",
  "sonarData",
  sizeof(SonarData__GeorefNED),
  4,
  sonar_data__georef__ned__field_descriptors,
  sonar_data__georef__ned__field_indices_by_name,
  1,  sonar_data__georef__ned__number_ranges,
  (ProtobufCMessageInit) sonar_data__georef__ned__init,
  NULL,NULL,NULL    /* reserved[123] */
};
static const ProtobufCFieldDescriptor sonar_data__georef__ecef__field_descriptors[7] =
{
  {
    "x_pointCld_body_ECEF",
    1,
    PROTOBUF_C_LABEL_REPEATED,
    PROTOBUF_C_TYPE_FLOAT,
    offsetof(SonarData__GeorefECEF, n_x_pointcld_body_ecef),
    offsetof(SonarData__GeorefECEF, x_pointcld_body_ecef),
    NULL,
    NULL,
    0 | PROTOBUF_C_FIELD_FLAG_PACKED,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "y_pointCld_body_ECEF",
    2,
    PROTOBUF_C_LABEL_REPEATED,
    PROTOBUF_C_TYPE_FLOAT,
    offsetof(SonarData__GeorefECEF, n_y_pointcld_body_ecef),
    offsetof(SonarData__GeorefECEF, y_pointcld_body_ecef),
    NULL,
    NULL,
    0 | PROTOBUF_C_FIELD_FLAG_PACKED,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "z_pointCld_body_ECEF",
    3,
    PROTOBUF_C_LABEL_REPEATED,
    PROTOBUF_C_TYPE_FLOAT,
    offsetof(SonarData__GeorefECEF, n_z_pointcld_body_ecef),
    offsetof(SonarData__GeorefECEF, z_pointcld_body_ecef),
    NULL,
    NULL,
    0 | PROTOBUF_C_FIELD_FLAG_PACKED,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "rotationMatrix_ECEF",
    4,
    PROTOBUF_C_LABEL_REPEATED,
    PROTOBUF_C_TYPE_FLOAT,
    offsetof(SonarData__GeorefECEF, n_rotationmatrix_ecef),
    offsetof(SonarData__GeorefECEF, rotationmatrix_ecef),
    NULL,
    NULL,
    0 | PROTOBUF_C_FIELD_FLAG_PACKED,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "x_body_position_ECEF",
    5,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_FLOAT,
    0,   /* quantifier_offset */
    offsetof(SonarData__GeorefECEF, x_body_position_ecef),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "y_body_position_ECEF",
    6,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_FLOAT,
    0,   /* quantifier_offset */
    offsetof(SonarData__GeorefECEF, y_body_position_ecef),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "z_body_position_ECEF",
    7,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_FLOAT,
    0,   /* quantifier_offset */
    offsetof(SonarData__GeorefECEF, z_body_position_ecef),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
};
static const unsigned sonar_data__georef__ecef__field_indices_by_name[] = {
  3,   /* field[3] = rotationMatrix_ECEF */
  4,   /* field[4] = x_body_position_ECEF */
  0,   /* field[0] = x_pointCld_body_ECEF */
  5,   /* field[5] = y_body_position_ECEF */
  1,   /* field[1] = y_pointCld_body_ECEF */
  6,   /* field[6] = z_body_position_ECEF */
  2,   /* field[2] = z_pointCld_body_ECEF */
};
static const ProtobufCIntRange sonar_data__georef__ecef__number_ranges[1 + 1] =
{
  { 1, 0 },
  { 0, 7 }
};
const ProtobufCMessageDescriptor sonar_data__georef__ecef__descriptor =
{
  PROTOBUF_C__MESSAGE_DESCRIPTOR_MAGIC,
  "sonarData.Georef_ECEF",
  "GeorefECEF",
  "SonarData__GeorefECEF",
  "sonarData",
  sizeof(SonarData__GeorefECEF),
  7,
  sonar_data__georef__ecef__field_descriptors,
  sonar_data__georef__ecef__field_indices_by_name,
  1,  sonar_data__georef__ecef__number_ranges,
  (ProtobufCMessageInit) sonar_data__georef__ecef__init,
  NULL,NULL,NULL    /* reserved[123] */
};
static const ProtobufCFieldDescriptor sonar_data__telemetry__field_descriptors[5] =
{
  {
    "position",
    1,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_MESSAGE,
    0,   /* quantifier_offset */
    offsetof(SonarData__Telemetry, position),
    &sonar_data__telemetry_data_position__descriptor,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "pose",
    2,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_MESSAGE,
    0,   /* quantifier_offset */
    offsetof(SonarData__Telemetry, pose),
    &sonar_data__telemetry_data_pose__descriptor,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "heading",
    3,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_MESSAGE,
    0,   /* quantifier_offset */
    offsetof(SonarData__Telemetry, heading),
    &sonar_data__telemetry_data_heading__descriptor,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "depth",
    4,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_MESSAGE,
    0,   /* quantifier_offset */
    offsetof(SonarData__Telemetry, depth),
    &sonar_data__telemetry_data_depth__descriptor,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "altitude",
    5,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_MESSAGE,
    0,   /* quantifier_offset */
    offsetof(SonarData__Telemetry, altitude),
    &sonar_data__telemetry_data_altitude__descriptor,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
};
static const unsigned sonar_data__telemetry__field_indices_by_name[] = {
  4,   /* field[4] = altitude */
  3,   /* field[3] = depth */
  2,   /* field[2] = heading */
  1,   /* field[1] = pose */
  0,   /* field[0] = position */
};
static const ProtobufCIntRange sonar_data__telemetry__number_ranges[1 + 1] =
{
  { 1, 0 },
  { 0, 5 }
};
const ProtobufCMessageDescriptor sonar_data__telemetry__descriptor =
{
  PROTOBUF_C__MESSAGE_DESCRIPTOR_MAGIC,
  "sonarData.Telemetry",
  "Telemetry",
  "SonarData__Telemetry",
  "sonarData",
  sizeof(SonarData__Telemetry),
  5,
  sonar_data__telemetry__field_descriptors,
  sonar_data__telemetry__field_indices_by_name,
  1,  sonar_data__telemetry__number_ranges,
  (ProtobufCMessageInit) sonar_data__telemetry__init,
  NULL,NULL,NULL    /* reserved[123] */
};
static const ProtobufCFieldDescriptor sonar_data__telemetry_data_position__field_descriptors[3] =
{
  {
    "latitude",
    1,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_FLOAT,
    0,   /* quantifier_offset */
    offsetof(SonarData__TelemetryDataPosition, latitude),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "longitude",
    2,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_FLOAT,
    0,   /* quantifier_offset */
    offsetof(SonarData__TelemetryDataPosition, longitude),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "position_timestep",
    3,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_INT32,
    0,   /* quantifier_offset */
    offsetof(SonarData__TelemetryDataPosition, position_timestep),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
};
static const unsigned sonar_data__telemetry_data_position__field_indices_by_name[] = {
  0,   /* field[0] = latitude */
  1,   /* field[1] = longitude */
  2,   /* field[2] = position_timestep */
};
static const ProtobufCIntRange sonar_data__telemetry_data_position__number_ranges[1 + 1] =
{
  { 1, 0 },
  { 0, 3 }
};
const ProtobufCMessageDescriptor sonar_data__telemetry_data_position__descriptor =
{
  PROTOBUF_C__MESSAGE_DESCRIPTOR_MAGIC,
  "sonarData.telemetryData_position",
  "TelemetryDataPosition",
  "SonarData__TelemetryDataPosition",
  "sonarData",
  sizeof(SonarData__TelemetryDataPosition),
  3,
  sonar_data__telemetry_data_position__field_descriptors,
  sonar_data__telemetry_data_position__field_indices_by_name,
  1,  sonar_data__telemetry_data_position__number_ranges,
  (ProtobufCMessageInit) sonar_data__telemetry_data_position__init,
  NULL,NULL,NULL    /* reserved[123] */
};
static const ProtobufCFieldDescriptor sonar_data__telemetry_data_pose__field_descriptors[3] =
{
  {
    "roll",
    1,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_FLOAT,
    0,   /* quantifier_offset */
    offsetof(SonarData__TelemetryDataPose, roll),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "pitch",
    2,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_FLOAT,
    0,   /* quantifier_offset */
    offsetof(SonarData__TelemetryDataPose, pitch),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "pose_timestep",
    3,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_INT32,
    0,   /* quantifier_offset */
    offsetof(SonarData__TelemetryDataPose, pose_timestep),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
};
static const unsigned sonar_data__telemetry_data_pose__field_indices_by_name[] = {
  1,   /* field[1] = pitch */
  2,   /* field[2] = pose_timestep */
  0,   /* field[0] = roll */
};
static const ProtobufCIntRange sonar_data__telemetry_data_pose__number_ranges[1 + 1] =
{
  { 1, 0 },
  { 0, 3 }
};
const ProtobufCMessageDescriptor sonar_data__telemetry_data_pose__descriptor =
{
  PROTOBUF_C__MESSAGE_DESCRIPTOR_MAGIC,
  "sonarData.telemetryData_pose",
  "TelemetryDataPose",
  "SonarData__TelemetryDataPose",
  "sonarData",
  sizeof(SonarData__TelemetryDataPose),
  3,
  sonar_data__telemetry_data_pose__field_descriptors,
  sonar_data__telemetry_data_pose__field_indices_by_name,
  1,  sonar_data__telemetry_data_pose__number_ranges,
  (ProtobufCMessageInit) sonar_data__telemetry_data_pose__init,
  NULL,NULL,NULL    /* reserved[123] */
};
static const ProtobufCFieldDescriptor sonar_data__telemetry_data_heading__field_descriptors[2] =
{
  {
    "heading",
    1,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_FLOAT,
    0,   /* quantifier_offset */
    offsetof(SonarData__TelemetryDataHeading, heading),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "heading_timestep",
    2,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_INT32,
    0,   /* quantifier_offset */
    offsetof(SonarData__TelemetryDataHeading, heading_timestep),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
};
static const unsigned sonar_data__telemetry_data_heading__field_indices_by_name[] = {
  0,   /* field[0] = heading */
  1,   /* field[1] = heading_timestep */
};
static const ProtobufCIntRange sonar_data__telemetry_data_heading__number_ranges[1 + 1] =
{
  { 1, 0 },
  { 0, 2 }
};
const ProtobufCMessageDescriptor sonar_data__telemetry_data_heading__descriptor =
{
  PROTOBUF_C__MESSAGE_DESCRIPTOR_MAGIC,
  "sonarData.telemetryData_heading",
  "TelemetryDataHeading",
  "SonarData__TelemetryDataHeading",
  "sonarData",
  sizeof(SonarData__TelemetryDataHeading),
  2,
  sonar_data__telemetry_data_heading__field_descriptors,
  sonar_data__telemetry_data_heading__field_indices_by_name,
  1,  sonar_data__telemetry_data_heading__number_ranges,
  (ProtobufCMessageInit) sonar_data__telemetry_data_heading__init,
  NULL,NULL,NULL    /* reserved[123] */
};
static const ProtobufCFieldDescriptor sonar_data__telemetry_data_depth__field_descriptors[2] =
{
  {
    "depth",
    1,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_FLOAT,
    0,   /* quantifier_offset */
    offsetof(SonarData__TelemetryDataDepth, depth),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "depth_timestep",
    2,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_INT32,
    0,   /* quantifier_offset */
    offsetof(SonarData__TelemetryDataDepth, depth_timestep),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
};
static const unsigned sonar_data__telemetry_data_depth__field_indices_by_name[] = {
  0,   /* field[0] = depth */
  1,   /* field[1] = depth_timestep */
};
static const ProtobufCIntRange sonar_data__telemetry_data_depth__number_ranges[1 + 1] =
{
  { 1, 0 },
  { 0, 2 }
};
const ProtobufCMessageDescriptor sonar_data__telemetry_data_depth__descriptor =
{
  PROTOBUF_C__MESSAGE_DESCRIPTOR_MAGIC,
  "sonarData.telemetryData_depth",
  "TelemetryDataDepth",
  "SonarData__TelemetryDataDepth",
  "sonarData",
  sizeof(SonarData__TelemetryDataDepth),
  2,
  sonar_data__telemetry_data_depth__field_descriptors,
  sonar_data__telemetry_data_depth__field_indices_by_name,
  1,  sonar_data__telemetry_data_depth__number_ranges,
  (ProtobufCMessageInit) sonar_data__telemetry_data_depth__init,
  NULL,NULL,NULL    /* reserved[123] */
};
static const ProtobufCFieldDescriptor sonar_data__telemetry_data_altitude__field_descriptors[2] =
{
  {
    "altitude",
    1,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_FLOAT,
    0,   /* quantifier_offset */
    offsetof(SonarData__TelemetryDataAltitude, altitude),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "altitude_timestep",
    2,
    PROTOBUF_C_LABEL_NONE,
    PROTOBUF_C_TYPE_INT32,
    0,   /* quantifier_offset */
    offsetof(SonarData__TelemetryDataAltitude, altitude_timestep),
    NULL,
    NULL,
    0,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
};
static const unsigned sonar_data__telemetry_data_altitude__field_indices_by_name[] = {
  0,   /* field[0] = altitude */
  1,   /* field[1] = altitude_timestep */
};
static const ProtobufCIntRange sonar_data__telemetry_data_altitude__number_ranges[1 + 1] =
{
  { 1, 0 },
  { 0, 2 }
};
const ProtobufCMessageDescriptor sonar_data__telemetry_data_altitude__descriptor =
{
  PROTOBUF_C__MESSAGE_DESCRIPTOR_MAGIC,
  "sonarData.telemetryData_altitude",
  "TelemetryDataAltitude",
  "SonarData__TelemetryDataAltitude",
  "sonarData",
  sizeof(SonarData__TelemetryDataAltitude),
  2,
  sonar_data__telemetry_data_altitude__field_descriptors,
  sonar_data__telemetry_data_altitude__field_indices_by_name,
  1,  sonar_data__telemetry_data_altitude__number_ranges,
  (ProtobufCMessageInit) sonar_data__telemetry_data_altitude__init,
  NULL,NULL,NULL    /* reserved[123] */
};
static const ProtobufCFieldDescriptor sonar_data__ungeoref__field_descriptors[5] =
{
  {
    "pointX",
    1,
    PROTOBUF_C_LABEL_REPEATED,
    PROTOBUF_C_TYPE_FLOAT,
    offsetof(SonarData__Ungeoref, n_pointx),
    offsetof(SonarData__Ungeoref, pointx),
    NULL,
    NULL,
    0 | PROTOBUF_C_FIELD_FLAG_PACKED,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "pointY",
    2,
    PROTOBUF_C_LABEL_REPEATED,
    PROTOBUF_C_TYPE_FLOAT,
    offsetof(SonarData__Ungeoref, n_pointy),
    offsetof(SonarData__Ungeoref, pointy),
    NULL,
    NULL,
    0 | PROTOBUF_C_FIELD_FLAG_PACKED,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "beamIdx",
    3,
    PROTOBUF_C_LABEL_REPEATED,
    PROTOBUF_C_TYPE_INT32,
    offsetof(SonarData__Ungeoref, n_beamidx),
    offsetof(SonarData__Ungeoref, beamidx),
    NULL,
    NULL,
    0 | PROTOBUF_C_FIELD_FLAG_PACKED,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "quality",
    4,
    PROTOBUF_C_LABEL_REPEATED,
    PROTOBUF_C_TYPE_UINT32,
    offsetof(SonarData__Ungeoref, n_quality),
    offsetof(SonarData__Ungeoref, quality),
    NULL,
    NULL,
    0 | PROTOBUF_C_FIELD_FLAG_PACKED,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
  {
    "intensity",
    5,
    PROTOBUF_C_LABEL_REPEATED,
    PROTOBUF_C_TYPE_FLOAT,
    offsetof(SonarData__Ungeoref, n_intensity),
    offsetof(SonarData__Ungeoref, intensity),
    NULL,
    NULL,
    0 | PROTOBUF_C_FIELD_FLAG_PACKED,             /* flags */
    0,NULL,NULL    /* reserved1,reserved2, etc */
  },
};
static const unsigned sonar_data__ungeoref__field_indices_by_name[] = {
  2,   /* field[2] = beamIdx */
  4,   /* field[4] = intensity */
  0,   /* field[0] = pointX */
  1,   /* field[1] = pointY */
  3,   /* field[3] = quality */
};
static const ProtobufCIntRange sonar_data__ungeoref__number_ranges[1 + 1] =
{
  { 1, 0 },
  { 0, 5 }
};
const ProtobufCMessageDescriptor sonar_data__ungeoref__descriptor =
{
  PROTOBUF_C__MESSAGE_DESCRIPTOR_MAGIC,
  "sonarData.Ungeoref",
  "Ungeoref",
  "SonarData__Ungeoref",
  "sonarData",
  sizeof(SonarData__Ungeoref),
  5,
  sonar_data__ungeoref__field_descriptors,
  sonar_data__ungeoref__field_indices_by_name,
  1,  sonar_data__ungeoref__number_ranges,
  (ProtobufCMessageInit) sonar_data__ungeoref__init,
  NULL,NULL,NULL    /* reserved[123] */
};
