#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "decoders.h"

static void extract_ip(const char *log_data, char *ip_buffer)
{
    // Basic IP extraction logic (you can refine with regex or other methods)
    const char *ip_start = strstr(log_data, "IP:");
    if (ip_start)
    {
        sscanf(ip_start, "IP:%49s", ip_buffer);
    }
}

// SSH log decoder
int decode_ssh_log(const char *log_data, DecodedLog *decoded_log)
{
    strcpy(decoded_log->log_type, "SSH");

    // Extract IP address from the SSH log
    extract_ip(log_data, decoded_log->source_ip);

    // Check for specific events in the SSH log
    if (strstr(log_data, "Failed password"))
    {
        strcpy(decoded_log->event_data, "SSH failed login attempt");
    }
    else if (strstr(log_data, "Accepted password"))
    {
        strcpy(decoded_log->event_data, "SSH successful login");
    }
    else
    {
        strcpy(decoded_log->event_data, "Other SSH event");
    }

    return 0; // Successful decoding
}

// Syslog log decoder
int decode_syslog_log(const char *log_data, DecodedLog *decoded_log)
{
    strcpy(decoded_log->log_type, "Syslog");

    // Extract IP address from syslog (or other relevant fields)
    extract_ip(log_data, decoded_log->source_ip);

    // Match patterns based on syslog events
    if (strstr(log_data, "Couldn't open /etc/securetty"))
    {
        strcpy(decoded_log->event_data, "Syslog: Root access unrestricted due to missing securetty");
    }
    else if (strstr(log_data, "Segmentation Fault"))
    {
        strcpy(decoded_log->event_data, "Syslog: Segmentation Fault detected");
    }
    else if (strstr(log_data, "error"))
    {
        strcpy(decoded_log->event_data, "Syslog: General error detected");
    }
    else
    {
        strcpy(decoded_log->event_data, "Other Syslog event");
    }

    return EXIT_SUCCESS;
}