#ifndef SERVICE_H
#define SERVICE_H

#include <tins/tins.h>
#include <string>

std::string identifyService(const Tins::Packet& pkt);

#endif // SERVICE_H
