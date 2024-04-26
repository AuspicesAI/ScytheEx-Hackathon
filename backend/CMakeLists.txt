cmake_minimum_required(VERSION 3.10)
project(ScytheEx_Backend)

set(CMAKE_CXX_STANDARD 11)

include_directories(include)

file(GLOB SOURCES "src/*.cpp")

add_executable(scytheex_backend ${SOURCES})

target_link_libraries(scytheex_backend tins)
