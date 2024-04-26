#ifndef CONNECTION_TRACKER_H
#define CONNECTION_TRACKER_H

#include <unordered_map>
#include <queue>
#include <string>
#include <utility>

class ConnectionTracker {
public:
    void processConnection(const std::string& srcAddress, int dstPort, const std::string& dstAddress, int srcPort);
    int countSrcDstPort(const std::string& srcAddress, int dstPort);
    int countDstSrcPort(const std::string& dstAddress, int srcPort);

private:
    static const int WINDOW_SIZE = 100;  // Maintain only the last 100 connections
    std::queue<std::pair<std::string, int>> srcDstPortQueue;
    std::queue<std::pair<std::string, int>> dstSrcPortQueue;
    std::unordered_map<std::string, int> srcDstPortCounts;
    std::unordered_map<std::string, int> dstSrcPortCounts;

    void maintainWindowSize(std::queue<std::pair<std::string, int>>& queue, std::unordered_map<std::string, int>& counts);
};

#endif // CONNECTION_TRACKER_H
