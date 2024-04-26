#include "proto.h"

std::string extractProtocol(const Tins::Packet& pkt) {
    const Tins::PDU* pdu = pkt.pdu();

    // Check for layer types and extract the protocol type
    if (pdu->find_pdu<Tins::TCP>()) {
        return "TCP";
    } else if (pdu->find_pdu<Tins::UDP>()) {
        return "UDP";
    } else if (pdu->find_pdu<Tins::ICMP>()) {
        return "ICMP";
    } else {
        return "Unknown";
    }
}
