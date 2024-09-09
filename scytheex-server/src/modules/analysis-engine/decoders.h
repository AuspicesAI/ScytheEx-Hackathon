#ifndef DECODERS_H
#define DECODERS_H

typedef struct
{
    char log_type[50];     // Log type (e.g., SSH, syslog)
    char source_ip[50];    // Source IP extracted from the log
    char event_data[2048]; // Parsed event data
} DecodedLog;

int decode_ssh_log(const char *log_data, DecodedLog *decoded_log);
int decode_syslog_log(const char *log_data, DecodedLog *decoded_log);

#endif // DECODERS_H