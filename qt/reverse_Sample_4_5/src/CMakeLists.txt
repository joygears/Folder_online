
set(HEADERS 
    ${CMAKE_CURRENT_SOURCE_DIR}/Sample_4_5.h
	${CMAKE_CURRENT_SOURCE_DIR}/ui_Sample_4_5.h
)
set(SOURCES 
    ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/Sample_4_5.cpp
)


add_executable(${PROJECT_NAME} ${SOURCES})


find_package(Qt5 COMPONENTS Widgets REQUIRED)

target_link_libraries(${PROJECT_NAME} Qt5::Widgets)