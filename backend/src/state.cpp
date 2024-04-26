#include "state.h"

std::string ConnectionStateTracker::trackState(const Tins::Packet& pkt) {
    auto ip = pkt.pdu()->find_pdu<Tins::IP>();
    auto tcp = pkt.pdu()->find_pdu<Tins::TCP>();
    if (!ip || !tcp) return "Invalid TCP/IP packet";

    std::string key = ip->src_addr().to_string() + ":" + std::to_string(tcp->sport()) + "->"
                      + ip->dst_addr().to_string() + ":" + std::to_string(tcp->dport());
    auto& conn = connections[key];

    if (tcp->get_flag(Tins::TCP::SYN) && !tcp->get_flag(Tins::TCP::ACK)) {
        conn.syn_time = std::chrono::steady_clock::now();
        conn.state = "SYN_SENT";
    } else if (tcp->get_flag(Tins::TCP::SYN) && tcp->get_flag(Tins::TCP::ACK)) {
        conn.syn_ack_time = std::chrono::steady_clock::now();
        conn.state = "SYN_RECEIVED";
    } else if (tcp->get_flag(Tins::TCP::ACK) && conn.state == "SYN_RECEIVED") {
        conn.ack_time = std::chrono::steady_clock::now();
        conn.state = "ESTABLISHED";
    }
    return conn.state;
}

double ConnectionStateTracker::getSynAckTime(const std::string& key) {
    auto& conn = connections[key];
    if (conn.syn_time != std::chrono::steady_clock::time_point() && conn.syn_ack_time != std::chrono::steady_clock::time_point()) {
        return std::chrono::duration_cast<std::chrono::milliseconds>(conn.syn_ack_time - conn.syn_time).count();
    }
    return 0.0;
}

double ConnectionStateTracker::getAckDatTime(const std::string& key) {
    auto& conn = connections[key];
    if (conn.syn_ack_time != std::chrono::steady_clock::time_point() && conn.ack_time != std::chrono::steady_clock::time_point()) {
        return std::chrono::duration_cast<std::chrono::milliseconds>(conn.ack_time - conn.syn_ack_time).count();
    }
    return 0.0;
}
