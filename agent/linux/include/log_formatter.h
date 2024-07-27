#ifndef LOG_FORMATTER_H
#define LOG_FORMATTER_H

#include <json-c/json.h>
#include <pfring.h>

#ifndef U_CHAR_DEFINED
typedef unsigned char u_char;
#define U_CHAR_DEFINED
#endif

json_object *format_log(const u_char *packet_data, struct pfring_pkthdr hdr);

#endif // LOG_FORMATTER_H
