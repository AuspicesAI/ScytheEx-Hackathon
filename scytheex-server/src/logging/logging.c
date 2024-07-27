#include "logging.h"
#include <stdarg.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

static FILE *log_file = NULL;
static LogLevel log_level = LOG_INFO;

void init_logging(const char *logfile, LogLevel level)
{
    // Create parent directories if they do not exist
    char dir[256];
    strncpy(dir, logfile, sizeof(dir) - 1);
    dir[sizeof(dir) - 1] = '\0';

    // Find the last slash in the path
    char *last_slash = strrchr(dir, '/');
    if (last_slash != NULL)
    {
        *last_slash = '\0'; // Null-terminate the directory path

        struct stat st = {0};
        if (stat(dir, &st) == -1)
        {
            if (mkdir(dir, 0755) == -1)
            {
                perror("Failed to create directory");
                exit(EXIT_FAILURE);
            }
        }
        else if (!S_ISDIR(st.st_mode))
        {
            fprintf(stderr, "Failed to create directory: %s exists and is not a directory\n", dir);
            exit(EXIT_FAILURE);
        }
    }

    // Open the log file
    log_file = fopen(logfile, "a");
    if (log_file == NULL)
    {
        perror("Failed to open log file");
        exit(EXIT_FAILURE);
    }

    log_level = level;
}

void log_message(LogLevel level, const char *format, ...)
{
    if (level < log_level || log_file == NULL)
    {
        return;
    }

    static const char *level_strings[] = {"DEBUG", "INFO", "WARN", "ERROR"};

    time_t now = time(NULL);
    struct tm *local_time = localtime(&now);

    fprintf(log_file, "%04d-%02d-%02d %02d:%02d:%02d [%s] ",
            local_time->tm_year + 1900, local_time->tm_mon + 1, local_time->tm_mday,
            local_time->tm_hour, local_time->tm_min, local_time->tm_sec,
            level_strings[level]);

    va_list args;
    va_start(args, format);
    vfprintf(log_file, format, args);
    va_end(args);

    fprintf(log_file, "\n");
    fflush(log_file);
}

void close_logging()
{
    if (log_file)
    {
        fclose(log_file);
        log_file = NULL;
    }
}