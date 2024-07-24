/*
pf_ring installation:

# Ubuntu 22.04
sudo apt-get install software-properties-common wget
sudo add-apt-repository universe
wget https://packages.ntop.org/apt-stable/22.04/all/apt-ntop-stable.deb
sudo apt install ./apt-ntop-stable.deb
sudo apt update
sudo apt install pfring

sudo pf_ringcfg --configure-driver ixgbe
sudo pf_ringcfg --list-interfaces

Install libjson-dev: sudo apt-get install libjson-c-dev
Install libyaml-dev: sudo apt-get install libyaml-dev
Install libcurl-dev: sudo apt install libcurl4-openssl-dev
*/
// #include "agent.h"
// #include "logger.h"

/* Without Elasticsearch (Testing)*/
// int main(int argc, char **argv)
// {
//     const char *interface = "enp0s3";

//     if (init_packet_capture(interface) != 0)
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

#include "agent.h"
#include "logger.h"
#include "config_manager.h"
#include <stdio.h>
#include <curl/curl.h>

void send_data_to_logstash(const char *data, const char *url) {
    CURL *curl;
    CURLcode res;

    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);

        res = curl_easy_perform(curl);

        if(res != CURLE_OK) {
            // log_error("cURL error: %s", curl_easy_strerror(res));
        }

        curl_easy_cleanup(curl);
    }
}

int main(int argc, char **argv)
{
    Config config;
    load_config("/home/smadi0x86/Desktop/ScytheEx/etc/config/config.yml", &config);

    if (init_packet_capture(config.interface) != 0)
    {
        log_error("Failed to initialize packet capture.");
        return -1;
    }

    log_info("Starting packet capture.");

    const char *logstash_url = "http://localhost:5044";
    const char *data = "{\"message\": \"example log data\"}";

    send_data_to_logstash(data, logstash_url);

    log_info("Packet capture stopped.");

    cleanup_packet_capture();
    return 0;
}
