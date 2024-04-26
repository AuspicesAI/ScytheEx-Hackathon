#include <iostream>
#include <cstdio>
#include <sstream>
#include <tins/tins.h>
#include "dur.h"
#include "proto.h"
#include "service.h"
#include "state.h"
#include "tcp_utils.h"
#include "http_tracker.h"
#include "connection_tracker.h"
#include "ftp_tracker.h"

using namespace Tins;

std::string format_data(const Packet& pkt, SessionDurationTracker& durationTracker,
                        ConnectionStateTracker& stateTracker, HTTPTracker& httpTracker,
                        ConnectionTracker& connectionTracker, FTPTracker& ftpTracker,
                        const std::string& key, const std::string& srcAddress,
                        int dstPort, const std::string& dstAddress, int srcPort) {
    std::stringstream ss;
    ss << "Duration: " << durationTracker.getSessionDuration(key) << " microseconds, "
       << "Protocol: " << extractProtocol(pkt) << ", "
       << "Service: " << identifyService(pkt) << ", "
       << "State: " << stateTracker.trackState(pkt) << ", "
       << "TCP Sequence Number: " << getTCPSequenceNumber(pkt) << ", "
       << "Destination TCP Acknowledgement Number: " << getTCPAcknowledgementNumber(pkt) << ", "
       << "SYN to SYN_ACK Time: " << stateTracker.getSynAckTime(key) << " ms, "
       << "SYN_ACK to ACK Time: " << stateTracker.getAckDatTime(key) << " ms, "
       << "HTTP Transaction Depth: " << httpTracker.getTransactionDepth(key) << ", "
       << "Last HTTP Response Body Length: " << httpTracker.getResponseBodyLength(key) << ", "
       << "HTTP Methods Count: " << httpTracker.countHTTPMethods(key) << ", "
       << "Are Source and Destination Same: " << (httpTracker.areSourceAndDestinationSame(key) ? "Yes" : "No") << ", "
       << "Number of connections for the same src address and dst port: " << connectionTracker.countSrcDstPort(srcAddress, dstPort) << ", "
       << "Number of connections for the same dst address and src port: " << connectionTracker.countDstSrcPort(dstAddress, srcPort) << ", "
       << "Is FTP Login: " << (ftpTracker.isFTPLogin(key) ? "Yes" : "No") << ", "
       << "FTP Command Count: " << ftpTracker.countFTPCmds(key);
    return ss.str();
}

int main() {
    SessionDurationTracker durationTracker;
    ConnectionStateTracker stateTracker;
    HTTPTracker httpTracker;
    ConnectionTracker connectionTracker;
    FTPTracker ftpTracker;

    SnifferConfiguration config;

    config.set_promisc_mode(true);
    config.set_snap_len(64 * 1024);  // 64 KB maximum packet size
    config.set_filter("ip src 172.19.124.205 or ip dst 172.19.124.205");
    Sniffer sniffer("eth0", config);

    FILE* pipe = popen("python3 process_data.py", "w");
    if (!pipe) {
        std::cerr << "Failed to open pipe to Python script\n";
        return 1;
    }

    try {
        while (Packet pkt = sniffer.next_packet()) {
            auto ip = pkt.pdu()->find_pdu<Tins::IP>();
            auto tcp = pkt.pdu()->find_pdu<Tins::TCP>();
            if (ip && tcp) {
                std::string key = durationTracker.extractKey(pkt);
                std::string srcAddress = ip->src_addr().to_string();
                int dstPort = tcp->dport();
                std::string dstAddress = ip->dst_addr().to_string();
                int srcPort = tcp->sport();

                std::string data_to_send = format_data(pkt, durationTracker, stateTracker,
                                                       httpTracker, connectionTracker,
                                                       ftpTracker, key, srcAddress,
                                                       dstPort, dstAddress, srcPort);
                fprintf(pipe, "%s\n", data_to_send.c_str());
            }
        }
    } catch (const std::exception& e) {
        std::cerr << "Exception caught in main loop: " << e.what() << '\n';
        pclose(pipe);
        return 1;
    }

    pclose(pipe);
    return 0;
}
