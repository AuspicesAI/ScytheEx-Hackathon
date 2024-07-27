#ifndef LOGGING_H
#define LOGGING_H

#include <stdio.h>

typedef enum
{
    LOG_DEBUG,
    LOG_INFO,
    LOG_WARN,
    LOG_ERROR
} LogLevel;

void init_logging(const char *logfile, LogLevel level);
void log_message(LogLevel level, const char *format, ...);
void close_logging();

#endif // LOGGING_H