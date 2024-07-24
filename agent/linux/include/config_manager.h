#ifndef CONFIG_MANAGER_H
#define CONFIG_MANAGER_H

typedef struct
{
    char interface[32];
    char elasticsearch_host[256];
    char log_level[16];
} Config;

void load_config(const char *config_file, Config *config);

#endif // CONFIG_MANAGER_H
