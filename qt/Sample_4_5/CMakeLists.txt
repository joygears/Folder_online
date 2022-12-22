cmake_minimum_required(VERSION 3.1.0)

project(sample_4_5 VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# set(CMAKE_CREATE_CONSOLE_EXE "/subsystem:windows")


if(CMAKE_VERSION VERSION_LESS "3.7.0")
    set(CMAKE_INCLUDE_CURRENT_DIR ON)
endif()

add_subdirectory(Sample_4_5)






# function(print_directory_variables dir)
#     # Dump variables:
#     get_property(_variableNames DIRECTORY ${dir} PROPERTY VARIABLES)
#     list (SORT _variableNames)
#     foreach (_variableName ${_variableNames})
#         get_directory_property(_variableValue DIRECTORY ${dir} DEFINITION ${_variableName})
#         message(STATUS "DIR ${dir}: ${_variableName}=${_variableValue}")
#     endforeach()
# endfunction(print_directory_variables)

# # for example
# print_directory_variables(.)

