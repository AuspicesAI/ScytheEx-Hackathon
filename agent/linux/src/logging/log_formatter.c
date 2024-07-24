#include "log_formatter.h"
#include <json-c/json.h>

json_object *format_log(const u_char *packet_data, struct pfring_pkthdr hdr)
{
    json_object *log_entry = json_object_new_object();
    json_object_object_add(log_entry, "timestamp", json_object_new_int64(hdr.ts.tv_sec));
    json_object_object_add(log_entry, "length", json_object_new_int(hdr.caplen));
    // ...
    return log_entry;
}
