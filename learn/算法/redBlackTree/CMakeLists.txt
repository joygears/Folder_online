cmake_minimum_required(VERSION 3.0.0 FATAL_ERROR)
project(AVL)
file(GLOB SOURCE_FILES "${CMAKE_CURRENT_SOURCE_DIR}/*.c" "${CMAKE_CURRENT_SOURCE_DIR}/*.h")
add_executable(AVL ${SOURCE_FILES})
