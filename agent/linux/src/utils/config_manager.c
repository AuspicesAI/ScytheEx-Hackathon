#include "config_manager.h"
#include <yaml.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void load_config(const char *config_file, Config *config)
{
    FILE *file = fopen(config_file, "r");
    if (!file)
    {
        perror("Failed to open config file");
        exit(EXIT_FAILURE);
    }

    yaml_parser_t parser;
    yaml_event_t event;

    yaml_parser_initialize(&parser);
    yaml_parser_set_input_file(&parser, file);

    char key[256];
    int parsing_key = 1;

    while (yaml_parser_parse(&parser, &event))
    {
        switch (event.type)
        {
        case YAML_SCALAR_EVENT:
            if (parsing_key)
            {
                strcpy(key, (char *)event.data.scalar.value);
                parsing_key = 0;
            }
            else
            {
                if (strcmp(key, "interface") == 0)
                {
                    strncpy(config->interface, (char *)event.data.scalar.value, sizeof(config->interface) - 1);
                }
                else if (strcmp(key, "elasticsearch_host") == 0)
                {
                    strncpy(config->elasticsearch_host, (char *)event.data.scalar.value, sizeof(config->elasticsearch_host) - 1);
                }
                else if (strcmp(key, "log_level") == 0)
                {
                    strncpy(config->log_level, (char *)event.data.scalar.value, sizeof(config->log_level) - 1);
                }
                parsing_key = 1;
            }
            break;
        default:
            break;
        }
        yaml_event_delete(&event);
    }

    yaml_parser_delete(&parser);
    fclose(file);
}