#ifndef DUR_H
#define DUR_H

#include <chrono>
#include <unordered_map>
#include <string>
#include <tins/tins.h>

class SessionDurationTracker {
    using Clock = std::chrono::high_resolution_clock;
    using TimePoint = std::chrono::time_point<Clock>;

public:
    // Changed to take a session key directly
    void startSession(const std::string& key);
    double getSessionDuration(const std::string& key);

    // Extracts a session key from a packet
    std::string extractKey(const Tins::Packet& pkt);

private:
    std::unordered_map<std::string, TimePoint> startTimes;
};

#endif // DUR_H
