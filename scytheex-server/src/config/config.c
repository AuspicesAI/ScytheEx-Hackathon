#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ini.h"
#include "config.h"

static int handler(void *user, const char *section, const char *name, const char *value)
{
    Config *config = (Config *)user;

    if (strcmp(section, "server") == 0)
    {
        if (strcmp(name, "port") == 0)
        {
            config->port = atoi(value);
        }
    }
    else if (strcmp(section, "logging") == 0)
    {
        if (strcmp(name, "logfile") == 0)
        {
            strncpy(config->logfile, value, MAX_LINE_LENGTH - 1);
            config->logfile[MAX_LINE_LENGTH - 1] = '\0';
        }
        else if (strcmp(name, "loglevel") == 0)
        {
            strncpy(config->loglevel, value, MAX_LINE_LENGTH - 1);
            config->loglevel[MAX_LINE_LENGTH - 1] = '\0';
        }
    }
    return 1;
}

int load_config(const char *filename, Config *config)
{
    return ini_parse(filename, handler, config);
}