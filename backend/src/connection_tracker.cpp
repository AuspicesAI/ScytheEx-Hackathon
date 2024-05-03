#include "connection_tracker.h"


void ConnectionTracker::processConnection(const std::string& srcAddress, int dstPort, const std::string& dstAddress, int srcPort) {
    std::lock_guard<std::mutex> lock(mtx); // Ensure thread safety

    // Construct keys for source-destination and destination-source
    std::string srcDstKey = srcAddress + ":" + std::to_string(dstPort);
    std::string dstSrcKey = dstAddress + ":" + std::to_string(srcPort);

    // Push connection details onto queues
    srcDstPortQueue.push({srcAddress, dstPort});
    dstSrcPortQueue.push({dstAddress, srcPort});

    // Increment counts for each key
    srcDstPortCounts[srcDstKey]++;
    dstSrcPortCounts[dstSrcKey]++;

    // Maintain size limits on the queues and maps
    maintainWindowSize(srcDstPortQueue, srcDstPortCounts);
    maintainWindowSize(dstSrcPortQueue, dstSrcPortCounts);
}

int ConnectionTracker::countSrcDstPort(const std::string& srcAddress, int dstPort) {
    std::lock_guard<std::mutex> lock(mtx); // Lock for thread safety
    std::string key = srcAddress + ":" + std::to_string(dstPort);
    auto it = srcDstPortCounts.find(key);
    return it != srcDstPortCounts.end() ? it->second : 0; // Return the count, or 0 if not found
}

int ConnectionTracker::countDstSrcPort(const std::string& dstAddress, int srcPort) {
    std::lock_guard<std::mutex> lock(mtx); // Lock for thread safety
    std::string key = dstAddress + ":" + std::to_string(srcPort);
    auto it = dstSrcPortCounts.find(key);
    return it != dstSrcPortCounts.end() ? it->second : 0; // Return the count, or 0 if not found
}

void ConnectionTracker::maintainWindowSize(std::queue<std::pair<std::string, int>>& queue, std::unordered_map<std::string, int>& counts) {
    while (queue.size() > WINDOW_SIZE) { // Ensure the queue does not exceed the predefined size
        auto old = queue.front();
        queue.pop();
        std::string oldKey = old.first + ":" + std::to_string(old.second);
        if (--counts[oldKey] == 0) { // Decrement the count and remove the key if the count is zero
            counts.erase(oldKey);
        }
    }
}
