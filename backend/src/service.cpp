#include "service.h"
#include <tins/tcp.h>
#include <tins/udp.h>
#include <unordered_map>
#include <sstream>

// Helper function to initialize service maps
std::unordered_map<uint16_t, std::string> initializeServiceMap() {
    std::unordered_map<uint16_t, std::string> serviceMap{
        {80, "HTTP"}, {443, "HTTPS"}, {22, "SSH"}, {21, "FTP"}, {23, "Telnet"},
        {25, "SMTP"}, {110, "POP3"}, {143, "IMAP"}, {3306, "MySQL"}, {3389, "RDP"},
        {587, "SMTPS"}, {53, "DNS"}, {161, "SNMP"}, {123, "NTP"}, {500, "IKE"}, {40056, "Havoc C2"}
    };
    return serviceMap;
}

// Global service map for quick lookups
static const std::unordered_map<uint16_t, std::string> serviceMap = initializeServiceMap();

std::string identifyService(const Tins::Packet& pkt) {
    std::stringstream serviceInfo;

    if (auto tcp = pkt.pdu()->find_pdu<Tins::TCP>()) {
        auto it = serviceMap.find(tcp->dport());
        if (it != serviceMap.end()) {
            return it->second;
        }
        serviceInfo << "Unknown Service on TCP Port " << tcp->dport();
        return serviceInfo.str();
    } else if (auto udp = pkt.pdu()->find_pdu<Tins::UDP>()) {
        auto it = serviceMap.find(udp->dport());
        if (it != serviceMap.end()) {
            return it->second;
        }
        serviceInfo << "Unknown Service on UDP Port " << udp->dport();
        return serviceInfo.str();
    }

    return "Unknown Service";
}
