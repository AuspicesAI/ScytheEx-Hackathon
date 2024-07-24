#ifndef AGENT_H
#define AGENT_H

#include <pfring.h>

#ifndef U_CHAR_DEFINED
typedef unsigned char u_char;
#define U_CHAR_DEFINED
#endif

int init_packet_capture(const char *interface);
void capture_packets();
void cleanup_packet_capture();

#endif // AGENT_H
