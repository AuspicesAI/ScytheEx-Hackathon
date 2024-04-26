#ifndef FTP_TRACKER_H
#define FTP_TRACKER_H

#include <tins/tins.h>
#include <unordered_map>
#include <string>

class FTPTracker {
public:
    void processPacket(const Tins::Packet& pkt);
    bool isFTPLogin(const std::string& connectionKey);
    int countFTPCmds(const std::string& connectionKey);

private:
    struct FTPSession {
        bool loginAttempt = false;
        int commandCount = 0;
    };

    std::unordered_map<std::string, FTPSession> sessions;

    std::string extractConnectionKey(const Tins::IP& ip, const Tins::TCP& tcp);
};

#endif // FTP_TRACKER_H
