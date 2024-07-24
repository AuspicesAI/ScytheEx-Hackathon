#include "agent.h"
#include "logger.h"
#include <pfring.h>
#include <stdio.h>

pfring *ring;

int init_packet_capture(const char *interface)
{
    ring = pfring_open(interface, 1500, PF_RING_PROMISC);
    if (!ring)
    {
        fprintf(stderr, "pfring_open error\n");
        return -1;
    }
    pfring_set_application_name(ring, "ScytheEx");
    pfring_enable_ring(ring);
    return 0;
}

void capture_packets()
{
    struct pfring_pkthdr hdr;
    u_char *pkt = NULL;
    while (1)
    {
        int rc = pfring_recv(ring, &pkt, 0, &hdr, 1);
        if (rc > 0)
        {
            log_info("Packet captured");
            printf("Timestamp: %ld, Length: %u\n", hdr.ts.tv_sec, hdr.caplen);
        }
    }
}

void cleanup_packet_capture()
{
    pfring_close(ring);
}
