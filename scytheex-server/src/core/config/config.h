#ifndef CONFIG_H
#define CONFIG_H

#define MAX_LINE_LENGTH 256

typedef struct {
    int port;
    char logfile[MAX_LINE_LENGTH];
    char loglevel[MAX_LINE_LENGTH];
} Config;

int load_config(const char *filename, Config *config);

#endif // CONFIG_H