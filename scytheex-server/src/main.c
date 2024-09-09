#include <stdio.h>
#include <stdlib.h>
#include "server.h"
#include "config.h"

int main()
{
    Config config = {0};

    // Load configuration
    if (load_config("../core/config/scytheex.conf", &config) != 0)
    {
        fprintf(stderr, "Failed to load configuration\n");

        return EXIT_FAILURE;
    }

    start_server(&config);
    return 0;
}