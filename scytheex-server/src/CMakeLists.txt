cmake_minimum_required(VERSION 3.10)
project(scytheex-server)

set(CMAKE_C_STANDARD 11)

# Include directories
include_directories(${PROJECT_SOURCE_DIR}/core/server)
include_directories(${PROJECT_SOURCE_DIR}/core/config)
include_directories(${PROJECT_SOURCE_DIR}/core/db)
include_directories(${PROJECT_SOURCE_DIR}/modules/analysis-engine)
include_directories(${PROJECT_SOURCE_DIR}/modules/alert-management)
include_directories(${PROJECT_SOURCE_DIR}/core/logging)
# Source files
set(SOURCES
    main.c
    core/server/server.c
    modules/analysis-engine/decoders.c
    modules/analysis-engine/actions.c
    modules/analysis-engine/rule-engine.c
    modules/analysis-engine/rules-loader.c
    core/logging/logging.c
    core/config/config.c
    core/config/ini.c
    core/db/db.c
    core/db/setup_db.c
    modules/alert-management/alerts.c
    modules/alert-management/events.c
)

# Add executable
add_executable(scytheex-server ${SOURCES})

# Link SQLite3 library
find_package(SQLite3 REQUIRED)
if (SQLite3_FOUND)
    include_directories(${SQLite3_INCLUDE_DIRS})
    target_link_libraries(scytheex-server ${SQLite3_LIBRARIES})
endif()

# Link libxml2 library
find_package(PkgConfig REQUIRED)
pkg_check_modules(LIBXML2 REQUIRED libxml-2.0)

include_directories(${LIBXML2_INCLUDE_DIRS})
link_directories(${LIBXML2_LIBRARY_DIRS})

target_link_libraries(scytheex-server ${LIBXML2_LIBRARIES})