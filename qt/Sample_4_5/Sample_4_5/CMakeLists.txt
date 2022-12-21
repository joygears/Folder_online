find_package(Qt5 COMPONENTS Widgets Gui REQUIRED)

set(HEADERS 
    Sample_4_5.h
)

set(SOURCES 
    main.cpp
    Sample_4_5.cpp
)

set(RESOURCES 
    Sample_4_5.qrc
)

set(UI
	Sample_4_5.ui
)

add_executable(${PROJECT_NAME}  ${HEADERS} ${SOURCES} ${RESOURCES} ${UI})


target_link_libraries(${PROJECT_NAME} Qt5::Widgets Qt5::Gui)

target_link_directories(${PROJECT_NAME} PUBLIC "hello")