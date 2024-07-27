cmake_minimum_required(VERSION 3.10)
project(scytheex-server)

set(CMAKE_C_STANDARD 11)

# Include directories
include_directories(${PROJECT_SOURCE_DIR}/server)
include_directories(${PROJECT_SOURCE_DIR}/analysisd)
include_directories(${PROJECT_SOURCE_DIR}/config)
include_directories(${PROJECT_SOURCE_DIR}/logging)
include_directories(${PROJECT_SOURCE_DIR}/db)
include_directories(${PROJECT_SOURCE_DIR}/active-response)
include_directories(${PROJECT_SOURCE_DIR}/logcollector)
include_directories(${PROJECT_SOURCE_DIR}/monitord)
include_directories(${PROJECT_SOURCE_DIR}/remoted)

# Source files
set(SOURCES
    main.c
    server/server.c
    analysisd/analysisd.c
    config/config.c
    config/ini.c
    logging/logging.c
    db/db.c
    db/setup_db.c
    db/events.c
    db/alerts.c
    active-response/active_response.c
    logcollector/logcollector.c
    monitord/monitord.c
    remoted/remoted.c
)

# Add executable
add_executable(scytheex-server ${SOURCES})

# Link SQLite3 library
find_package(SQLite3 REQUIRED)
if (SQLite3_FOUND)
    include_directories(${SQLite3_INCLUDE_DIRS})
    target_link_libraries(scytheex-server ${SQLite3_LIBRARIES})
endif()