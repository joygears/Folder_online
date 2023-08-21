cmake_minimum_required(VERSION 3.0.0)

project(test)


# 从文件夹从获取文件的决定路径
file(GLOB SOURCE_FILES "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp" "${CMAKE_CURRENT_SOURCE_DIR}/*.h" "${CMAKE_CURRENT_SOURCE_DIR}/*.ui")


add_executable(test	${SOURCE_FILES})


#添加编译选项(下面是添加以utf-8解码，避免中文跨平台乱码)
target_compile_options(test PUBLIC "/utf-8")