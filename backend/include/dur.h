#ifndef DUR_H
#define DUR_H

#include <chrono>
#include <unordered_map>
#include <string>
#include <mutex>
#include <tins/tins.h>

class SessionDurationTracker {
    using Clock = std::chrono::high_resolution_clock;  // High resolution clock for better accuracy
    using TimePoint = std::chrono::time_point<Clock>;  // Alias for readability
    using Duration = std::chrono::microseconds;  // Use microseconds for precision

public:
    SessionDurationTracker() = default;
    ~SessionDurationTracker() = default;

    // Prevent copy operations for safety
    SessionDurationTracker(const SessionDurationTracker&) = delete;
    SessionDurationTracker& operator=(const SessionDurationTracker&) = delete;

    // Allow move operations
    SessionDurationTracker(SessionDurationTracker&&) noexcept = default;
    SessionDurationTracker& operator=(SessionDurationTracker&&) noexcept = default;

    // Starts a session for a given key
    void startSession(const std::string& key);

    // Returns the duration of a session in microseconds, returns 0 if the session is not found
    double getSessionDuration(const std::string& key);

    // Extracts a unique session key from a packet, based on IP and TCP header data
    std::string extractKey(const Tins::Packet& pkt);

private:
    std::unordered_map<std::string, TimePoint> startTimes;  // Map to store start times of sessions
    std::mutex mutex;  // Mutex to protect access to startTimes

    // Helper function to safely get the current time point
    inline TimePoint getCurrentTime() const {
        return Clock::now();
    }
};

#endif // DUR_H
