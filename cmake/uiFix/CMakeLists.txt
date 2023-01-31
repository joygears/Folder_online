 cmake_minimum_required(VERSION 3.1.0)

project(uiFix VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

if(CMAKE_VERSION VERSION_LESS "3.7.0")
    set(CMAKE_INCLUDE_CURRENT_DIR ON)
endif()


find_package(Qt5 COMPONENTS Widgets Network REQUIRED)

set(HEADERS 
    MyTabWidget.h
    uiFit.h
    TaskTable.h
    AboutWidget.h
)

set(SOURCES 
    main.cpp
    uiFit.cpp
    MyTabWidget.cpp
    TaskTable.cpp
    AboutWidget.cpp
)

set(RESOURCES 
    uiFit.qrc
)

set(UI
	uiFit.ui
)


add_executable(${PROJECT_NAME}  ${HEADERS} ${SOURCES} ${RESOURCES} ${UI})


target_link_libraries(${PROJECT_NAME} Qt5::Widgets Qt5::Network)

