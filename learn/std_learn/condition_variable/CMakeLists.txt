cmake_minimum_required(VERSION 3.0.0 FATAL_ERROR)
project(condivar)
add_executable(condivar condivar.cpp)
add_library(func SHARED  func.h func.cpp)

target_include_directories(condivar PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(condivar func)