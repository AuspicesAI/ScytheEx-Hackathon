#include "tcp_utils.h"

std::string getTCPSequenceNumber(const Tins::Packet& pkt) {
    auto tcp = pkt.pdu()->find_pdu<Tins::TCP>();
    if (tcp) {
        return std::to_string(tcp->seq());
    }
    return "No TCP layer found";
}

std::string getTCPAcknowledgementNumber(const Tins::Packet& pkt) {
    auto tcp = pkt.pdu()->find_pdu<Tins::TCP>();
    if (tcp) {
        return std::to_string(tcp->ack_seq());
    }
    return "No TCP layer found";
}
