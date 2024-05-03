#include "ftp_tracker.h"
#include <iostream>  // For debug output
#include <regex>     // For sophisticated pattern matching

void FTPTracker::processPacket(const Tins::Packet& pkt) {
    auto ip = pkt.pdu()->find_pdu<Tins::IP>();
    auto tcp = pkt.pdu()->find_pdu<Tins::TCP>();
    if (!ip || !tcp) {
        std::cerr << "Failed to find necessary IP/TCP layer in packet." << std::endl;
        return;  // Early exit if IP or TCP layer is not found
    }

    std::string key = extractConnectionKey(*ip, *tcp);
    auto& session = sessions[key];  // Using reference to directly modify the session

    if (auto raw = tcp->find_pdu<Tins::RawPDU>()) {
        std::string payload(raw->payload().begin(), raw->payload().end());
        std::cout << "Processing payload: " << payload << std::endl;  // Debug output

        // Use regex to detect FTP commands more accurately
        static const std::regex ftpCmdRegex(R"(\bUSER\b|\bPASS\b|\bSTOR\b|\bRETR\b|\bLIST\b)");
        std::smatch matches;
        if (std::regex_search(payload, matches, ftpCmdRegex)) {
            std::cout << "FTP command detected: " << matches[0].str() << std::endl;  // Debug output
            if (matches[0].str() == "USER" || matches[0].str() == "PASS") {
                session.loginAttempt = true;
            }
            session.commandCount++;  // Increment for every command found
        }
    }
}

bool FTPTracker::isFTPLogin(const std::string& connectionKey) {
    auto it = sessions.find(connectionKey);
    if (it != sessions.end()) {
        return it->second.loginAttempt;
    }
    std::cerr << "No session found for key: " << connectionKey << std::endl;
    return false;
}

int FTPTracker::countFTPCmds(const std::string& connectionKey) {
    auto it = sessions.find(connectionKey);
    if (it != sessions.end()) {
        return it->second.commandCount;
    }
    return 0;  // Consider whether to handle this scenario differently
}

std::string FTPTracker::extractConnectionKey(const Tins::IP& ip, const Tins::TCP& tcp) {
    return ip.src_addr().to_string() + ":" + std::to_string(tcp.sport()) + "->" +
           ip.dst_addr().to_string() + ":" + std::to_string(tcp.dport());
}
