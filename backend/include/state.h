#ifndef STATE_H
#define STATE_H

#include <tins/tins.h>
#include <string>
#include <map>
#include <chrono>

class ConnectionStateTracker {
public:
    std::string trackState(const Tins::Packet& pkt);
    double getSynAckTime(const std::string& key);  // Time between SYN and SYN_ACK
    double getAckDatTime(const std::string& key);  // Time between SYN_ACK and ACK

private:
    struct ConnectionInfo {
        std::chrono::steady_clock::time_point syn_time;
        std::chrono::steady_clock::time_point syn_ack_time;
        std::chrono::steady_clock::time_point ack_time;
        std::string state;
    };

    std::map<std::string, ConnectionInfo> connections;
};

#endif // STATE_H
