cmake_minimum_required(VERSION 3.0)
project(publisher)

find_package(PkgConfig)
pkg_check_modules(ZMQ libzmq)

include_directories(${ZMQ_INCLUDE_DIRS})
link_directories(${ZMQ_LIBRARY_DIRS})

add_executable(publisher publisher.c)
target_link_libraries(publisher ${ZMQ_LIBRARIES})
