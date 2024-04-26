#include "dur.h"
#include <iostream>

void SessionDurationTracker::startSession(const std::string& key) {
    if (startTimes.find(key) == startTimes.end()) {
        startTimes[key] = Clock::now();
    }
}

double SessionDurationTracker::getSessionDuration(const std::string& key) {
    auto it = startTimes.find(key);
    if (it != startTimes.end()) {
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(Clock::now() - it->second).count();
        return static_cast<double>(duration);
    }
    return 0.0;
}

std::string SessionDurationTracker::extractKey(const Tins::Packet& pkt) {
    try {
        const Tins::IP& ip = pkt.pdu()->rfind_pdu<Tins::IP>();
        const Tins::TCP& tcp = pkt.pdu()->rfind_pdu<Tins::TCP>();
        return ip.src_addr().to_string() + ":" + std::to_string(tcp.sport()) + "->" +
               ip.dst_addr().to_string() + ":" + std::to_string(tcp.dport());
    } catch (...) {
        return "";  // Return an empty string if any part of the key extraction fails
    }
}
