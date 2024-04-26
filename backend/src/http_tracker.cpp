#include "http_tracker.h"
#include <tins/tcp.h>
#include <tins/ip.h>
#include <tins/rawpdu.h>
#include <regex>

void HTTPTracker::processPacket(const Tins::Packet& pkt) {
    auto ip = pkt.pdu()->find_pdu<Tins::IP>();
    auto tcp = pkt.pdu()->find_pdu<Tins::TCP>();
    if (!ip || !tcp) return;

    std::string key = extractConnectionKey(*ip, *tcp);
    auto& trans = transactions[key];

    trans.sameSrcDst = (ip->src_addr() == ip->dst_addr() && tcp->sport() == tcp->dport());

    if (tcp->get_flag(Tins::TCP::FIN) || tcp->get_flag(Tins::TCP::RST)) {
        transactions.erase(key);
        return;
    }

    if (auto raw = tcp->find_pdu<Tins::RawPDU>()) {
        std::string payload(raw->payload().begin(), raw->payload().end());
        static const std::regex httpMethodRegex("^(GET|POST|PUT|DELETE|HEAD|OPTIONS)\\s", std::regex_constants::icase);
        if (std::regex_search(payload, httpMethodRegex)) {
            trans.httpMethodCount++;
        }

        if (payload.find("HTTP") != std::string::npos) {
            size_t bodyPos = payload.find("\r\n\r\n");
            if (bodyPos != std::string::npos) {
                trans.responseBodyLengths.push_back(payload.length() - (bodyPos + 4));
            }
        }
    }
}

int HTTPTracker::getTransactionDepth(const std::string& connectionKey) {
    auto it = transactions.find(connectionKey);
    return it == transactions.end() ? 0 : it->second.transactionCount;
}

size_t HTTPTracker::getResponseBodyLength(const std::string& connectionKey) {
    auto it = transactions.find(connectionKey);
    if (it != transactions.end() && !it->second.responseBodyLengths.empty()) {
        return it->second.responseBodyLengths.back();
    }
    return 0;
}

int HTTPTracker::countHTTPMethods(const std::string& connectionKey) {
    auto it = transactions.find(connectionKey);
    return it == transactions.end() ? 0 : it->second.httpMethodCount;
}

bool HTTPTracker::areSourceAndDestinationSame(const std::string& connectionKey) {
    auto it = transactions.find(connectionKey);
    return it != transactions.end() && it->second.sameSrcDst;
}

std::string HTTPTracker::extractConnectionKey(const Tins::IP& ip, const Tins::TCP& tcp) {
    return ip.src_addr().to_string() + ":" + std::to_string(tcp.sport()) + "->"
           + ip.dst_addr().to_string() + ":" + std::to_string(tcp.dport());
}
