cmake_minimum_required(VERSION 3.0.0 FATAL_ERROR)

project(13_6 VERSION 0.1.0)

add_executable(13_6 13_6_reverse.cpp)

#添加编译选项(下面是添加以utf-8解码，避免中文跨平台乱码)
# target_compile_options(13_6 PUBLIC "/utf-8")

if(MSVC)
	target_compile_options(13_6 PUBLIC "$<$<CXX_COMPILER_ID:MSVC>:/source-charset:utf-8>")
endif(MSVC)