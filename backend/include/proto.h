#ifndef PROTO_H
#define PROTO_H

#include <tins/tins.h>
#include <string>

std::string extractProtocol(const Tins::Packet& pkt);

#endif // PROTO_H
