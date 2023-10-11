cmake_minimum_required(VERSION 3.12)

project(MyProject)

# Find Protocol Buffers package
find_package(Protobuf REQUIRED)

# Generate C++ sources and headers from your .proto file
protobuf_generate_c(PROTO_SRCS PROTO_HDRS my_module.proto)

# Include generated headers
include_directories(${CMAKE_CURRENT_BINARY_DIR})

# Add your source files
add_executable(my_project my_module.c ${PROTO_SRCS} ${PROTO_HDRS})

# Link the Protocol Buffers library
target_link_libraries(my_project ${PROTOBUF_LIBRARIES})
