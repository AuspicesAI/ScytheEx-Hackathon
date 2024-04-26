#ifndef HTTP_TRACKER_H
#define HTTP_TRACKER_H

#include <tins/tins.h>
#include <unordered_map>
#include <string>
#include <vector>
#include <regex>

class HTTPTracker {
public:
    void processPacket(const Tins::Packet& pkt);
    int getTransactionDepth(const std::string& connectionKey);
    size_t getResponseBodyLength(const std::string& connectionKey);
    int countHTTPMethods(const std::string& connectionKey);
    bool areSourceAndDestinationSame(const std::string& connectionKey);

private:
    struct HTTPTransaction {
        int transactionCount = 0;
        std::vector<size_t> responseBodyLengths;
        int httpMethodCount = 0;
        bool sameSrcDst = false;
    };

    std::unordered_map<std::string, HTTPTransaction> transactions;

    std::string extractConnectionKey(const Tins::IP& ip, const Tins::TCP& tcp);
};

#endif // HTTP_TRACKER_H
