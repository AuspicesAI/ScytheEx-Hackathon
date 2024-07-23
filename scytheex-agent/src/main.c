/*
pf_ring installation:

# Ubuntu 22.04
sudo apt-get install software-properties-common wget
sudo add-apt-repository universe
wget https://packages.ntop.org/apt-stable/22.04/all/apt-ntop-stable.deb
sudo apt install ./apt-ntop-stable.deb
sudo apt-get install pfring

pf_ringcfg --configure-driver ixgbe
pf_ringcfg --list-interfaces

Install json-c: sudo apt-get install libjson-c-dev
Install yaml-c: sudo apt-get install libyaml-dev
*/
#include "agent.h"
#include "logger.h"

/* Without Elasticsearch (Testing)*/
int main(int argc, char **argv)
{
    const char *interface = "eth0";

    if (init_packet_capture(interface) != 0)
    {
        log_error("Failed to initialize packet capture.");
        return -1;
    }

    log_info("Starting packet capture.");
    capture_packets();
    log_info("Packet capture stopped.");

    cleanup_packet_capture();
    return 0;
}

/* With Elasticsearch */

// #include "agent.h"
// #include "logger.h"
// #include "config_manager.h"
// #include <stdio.h>

// int main(int argc, char **argv)
// {
//     Config config;
//     load_config("scytheex-agent/etc/config/config.yml", &config);

//     if (init_packet_capture(config.interface) != 0)
//     {
//         log_error("Failed to initialize packet capture.");
//         return -1;
//     }

//     log_info("Starting packet capture.");
//     capture_packets();
//     log_info("Packet capture stopped.");

//     cleanup_packet_capture();
//     return 0;
// }
