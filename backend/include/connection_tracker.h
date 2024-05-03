#ifndef CONNECTION_TRACKER_H
#define CONNECTION_TRACKER_H

#include <string>
#include <unordered_map>
#include <queue>
#include <mutex>

class ConnectionTracker {
private:
    static const int WINDOW_SIZE = 1000;
    std::unordered_map<std::string, int> srcDstPortCounts;
    std::unordered_map<std::string, int> dstSrcPortCounts;
    std::queue<std::pair<std::string, int>> srcDstPortQueue;
    std::queue<std::pair<std::string, int>> dstSrcPortQueue;
    std::mutex mtx;

public:
    void processConnection(const std::string& srcAddress, int dstPort, const std::string& dstAddress, int srcPort);
    int countSrcDstPort(const std::string& srcAddress, int dstPort);
    int countDstSrcPort(const std::string& dstAddress, int srcPort);
    void maintainWindowSize(std::queue<std::pair<std::string, int>>& queue, std::unordered_map<std::string, int>& counts);
};

#endif // CONNECTION_TRACKER_H
