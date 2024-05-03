#include "dur.h"
#include <iostream>
#include <stdexcept>

void SessionDurationTracker::startSession(const std::string& key) {
    std::lock_guard<std::mutex> lock(mutex);  // Lock for thread safety
    auto now = getCurrentTime();
    // Insert the start time for the key, or reset if it already exists
    startTimes[key] = now;
    std::cout << "Session started for key: " << key << " at time: " << std::chrono::duration_cast<std::chrono::microseconds>(now.time_since_epoch()).count() << " microseconds" << std::endl;
}

double SessionDurationTracker::getSessionDuration(const std::string& key) {
    std::lock_guard<std::mutex> lock(mutex);  // Lock for thread safety
    auto it = startTimes.find(key);
    if (it != startTimes.end()) {
        auto now = getCurrentTime();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(now - it->second).count();
        std::cout << "Duration for key: " << key << " is " << duration << " microseconds" << std::endl;
        return static_cast<double>(duration);
    } else {
        // Log and handle the error if the key is not found
        std::cerr << "Error: No session found for key: " << key << std::endl;
        return 0.0;
    }
}

std::string SessionDurationTracker::extractKey(const Tins::Packet& pkt) {
    try {
        const Tins::IP& ip = pkt.pdu()->rfind_pdu<Tins::IP>();
        const Tins::TCP& tcp = pkt.pdu()->rfind_pdu<Tins::TCP>();
        std::string key = ip.src_addr().to_string() + ":" + std::to_string(tcp.sport()) + "->" +
                          ip.dst_addr().to_string() + ":" + std::to_string(tcp.dport());
        std::cout << "Extracted key: " << key << std::endl;
        return key;
    } catch (const std::exception& e) {
        // Exception handling if packet parsing fails
        std::cerr << "Failed to extract key from packet: " << e.what() << std::endl;
        return "";  // Return an empty string or handle differently as needed
    }
}
