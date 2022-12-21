cmake_minimum_required(VERSION 3.2.0 FATAL_ERROR)

project(qt_cmake VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)

add_executable(${PROJECT_NAME} 
main.cpp
qtcmake.ui
)


find_package(Qt5 COMPONENTS Widgets REQUIRED)

target_link_libraries(${PROJECT_NAME} 
Qt5::Widgets
qtcmake.ui
	)
