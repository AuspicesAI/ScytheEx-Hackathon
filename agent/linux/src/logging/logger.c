#include "logger.h"
#include <stdio.h>

void log_info(const char *message)
{
    printf("[INFO]: %s\n", message);
}

void log_error(const char *message)
{
    fprintf(stderr, "[ERROR]: %s\n", message);
}
