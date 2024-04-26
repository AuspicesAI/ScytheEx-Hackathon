#include "connection_tracker.h"

void ConnectionTracker::processConnection(const std::string& srcAddress, int dstPort, const std::string& dstAddress, int srcPort) {
    std::string srcDstKey = srcAddress + ":" + std::to_string(dstPort);
    std::string dstSrcKey = dstAddress + ":" + std::to_string(srcPort);

    srcDstPortQueue.push({srcAddress, dstPort});
    dstSrcPortQueue.push({dstAddress, srcPort});

    srcDstPortCounts[srcDstKey]++;
    dstSrcPortCounts[dstSrcKey]++;

    maintainWindowSize(srcDstPortQueue, srcDstPortCounts);
    maintainWindowSize(dstSrcPortQueue, dstSrcPortCounts);
}

int ConnectionTracker::countSrcDstPort(const std::string& srcAddress, int dstPort) {
    std::string key = srcAddress + ":" + std::to_string(dstPort);
    return srcDstPortCounts[key];
}

int ConnectionTracker::countDstSrcPort(const std::string& dstAddress, int srcPort) {
    std::string key = dstAddress + ":" + std::to_string(srcPort);
    return dstSrcPortCounts[key];
}

void ConnectionTracker::maintainWindowSize(std::queue<std::pair<std::string, int>>& queue, std::unordered_map<std::string, int>& counts) {
    if (queue.size() > WINDOW_SIZE) {
        auto old = queue.front();
        queue.pop();
        std::string oldKey = old.first + ":" + std::to_string(old.second);
        if (--counts[oldKey] == 0) {
            counts.erase(oldKey);
        }
    }
}
