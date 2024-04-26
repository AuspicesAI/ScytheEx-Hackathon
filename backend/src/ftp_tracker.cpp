#include "ftp_tracker.h"

void FTPTracker::processPacket(const Tins::Packet& pkt) {
    auto ip = pkt.pdu()->find_pdu<Tins::IP>();
    auto tcp = pkt.pdu()->find_pdu<Tins::TCP>();
    if (!ip || !tcp) return;

    std::string key = extractConnectionKey(*ip, *tcp);
    auto& session = sessions[key];

    if (auto raw = tcp->find_pdu<Tins::RawPDU>()) {
        std::string payload(raw->payload().begin(), raw->payload().end());
        // Check for FTP commands
        if (payload.find("USER") != std::string::npos || payload.find("PASS") != std::string::npos) {
            session.loginAttempt = true;
        }
        // Increment command count if any FTP command is detected
        if (payload.find("FTP") != std::string::npos) {  // Simplified check; refine to actual FTP commands
            session.commandCount++;
        }
    }
}

bool FTPTracker::isFTPLogin(const std::string& connectionKey) {
    auto it = sessions.find(connectionKey);
    return it != sessions.end() && it->second.loginAttempt;
}

int FTPTracker::countFTPCmds(const std::string& connectionKey) {
    auto it = sessions.find(connectionKey);
    if (it != sessions.end()) {
        return it->second.commandCount;
    }
    return 0;
}

std::string FTPTracker::extractConnectionKey(const Tins::IP& ip, const Tins::TCP& tcp) {
    return ip.src_addr().to_string() + ":" + std::to_string(tcp.sport()) + "->" +
           ip.dst_addr().to_string() + ":" + std::to_string(tcp.dport());
}
