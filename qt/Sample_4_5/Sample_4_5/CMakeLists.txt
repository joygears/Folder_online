find_package(Qt5 COMPONENTS Widgets REQUIRED)



# message(STATUS ---------------Qt5_DIR:${Qt5_DIR})
# message(STATUS ---------------Qt5_FOUND:${Qt5_FOUND})

# message(STATUS ---------------Qt5Widgets_INCLUDE_DIRS:${Qt5Widgets_INCLUDE_DIRS})
# message(STATUS ---------------Qt5Widgets_LIBRARIES:${Qt5Widgets_LIBRARIES})


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


target_link_libraries(${PROJECT_NAME} Qt5::Widgets)




# IF(WIN32)
#   IF(MSVC)
#     SET_TARGET_PROPERTIES(sample_4_5 PROPERTIES LINK_FLAGS_DEBUG "/SUBSYSTEM:WINDOWS")
#     SET_TARGET_PROPERTIES(sample_4_5 PROPERTIES LINK_FLAGS_RELWITHDEBINFO "/SUBSYSTEM:WINDOWS")
#     SET_TARGET_PROPERTIES(sample_4_5 PROPERTIES LINK_FLAGS_RELEASE "/SUBSYSTEM:WINDOWS")
#     SET_TARGET_PROPERTIES(sample_4_5 PROPERTIES LINK_FLAGS_MINSIZEREL "/SUBSYSTEM:WINDOWS")
#   ENDIF()
# ENDIF()