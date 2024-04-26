#ifndef TCP_UTILS_H
#define TCP_UTILS_H

#include <tins/tins.h>
#include <string>

std::string getTCPSequenceNumber(const Tins::Packet& pkt); // stcpb	(Source TCP sequence number)
std::string getTCPAcknowledgementNumber(const Tins::Packet& pkt); // stcpb	(Source TCP acknowledgement number)

#endif // TCP_UTILS_H
