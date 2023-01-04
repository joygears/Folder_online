

find_package(Qt5 COMPONENTS Widgets Network REQUIRED)
find_package(Qt5Network)
set(HEADERS 
    ${CMAKE_CURRENT_SOURCE_DIR}/SingleApplication.h
    ${CMAKE_CURRENT_SOURCE_DIR}/SingleApplicationPrivate.h
    ${CMAKE_CURRENT_SOURCE_DIR}/config.h
)

set(SOURCES 
    ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/SingleApplication.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/SingleApplicationPrivate.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/config.cpp
)

set(RESOURCES 
   res.qrc
)

# set(UI
# 	Sample_4_5.ui
# )


add_executable(${PROJECT_NAME}  ${HEADERS} ${SOURCES} ${RESOURCES} ${UI})

add_definitions(-DUNICODE -D_UNICODE)
target_link_libraries(${PROJECT_NAME} Qt5::Widgets Qt5::Network)