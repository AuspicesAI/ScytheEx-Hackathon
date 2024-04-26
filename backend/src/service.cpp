#include "service.h"
#include <tins/tcp.h>
#include <tins/udp.h>
#include <sstream>

std::string identifyService(const Tins::Packet& pkt) {
    std::stringstream serviceInfo;  // Use stringstream to format string with port number

    if (auto tcp = pkt.pdu()->find_pdu<Tins::TCP>()) {
        switch (tcp->dport()) {
            case 80: return "HTTP";
            case 443: return "HTTPS";
            case 22: return "SSH";
            case 21: return "FTP";
            case 23: return "Telnet";
            case 25: return "SMTP";
            case 110: return "POP3";
            case 143: return "IMAP";
            case 3306: return "MySQL";
            case 3389: return "RDP";
            case 587: return "SMTPS";
            // Add more cases as needed
            default:
                serviceInfo << "Unknown Service on TCP Port " << tcp->dport();
                return serviceInfo.str();
        }
    } else if (auto udp = pkt.pdu()->find_pdu<Tins::UDP>()) {
        switch (udp->dport()) {
            case 53: return "DNS";
            case 161: return "SNMP";
            case 123: return "NTP";
            case 500: return "IKE";
            case 1812: return "RADIUS";
            // Add more cases as needed
            default:
                serviceInfo << "Unknown Service on UDP Port " << udp->dport();
                return serviceInfo.str();
        }
    }
    return "Unknown Service";
}
