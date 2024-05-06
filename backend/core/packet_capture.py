# Copyright (c) 2024 AuspicesAI
#
# This file is part of ScytheEx.
#
# ScytheEx is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3.0 as
# published by the Free Software Foundation.
#
# ScytheEx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ScytheEx. If not, see <https://www.gnu.org/licenses/>.

from scapy.all import sniff, Ether, IP, TCP  # type: ignore
from core.logging import log_event, log_error
import uuid
import time
import json
import redis
import random

# Mapping from protocol numbers to names
protocol_mapping = {
    1: "ICMP",
    6: "TCP",
    17: "UDP",
    2: "IGMP",
    47: "GRE",
    50: "ESP",
    58: "IPV6-ICMP",
    88: "IGRP",
    89: "OSPFIGP",
    103: "PIM",
    112: "VRRP",
    113: "PGM",
    115: "L2TP",
    118: "STP",
    121: "SMP",
    132: "SCTP",
    137: "MPLS-in-IP",
}


def generate_packet_id():
    """Generate a unique packet identifier based on the current timestamp and a UUID."""
    return f"{int(time.time()*1000)}-{uuid.uuid4()}"


# Dictionary to keep track of flows
flows = {}


# Function to connect to Redis
def connect_to_redis(host, port, db_index):
    return redis.Redis(host=host, port=port, db=db_index, decode_responses=True)


def start_capture(config, traffic_logger, error_logger):
    try:
        redis_client = connect_to_redis("3.84.243.99", 6379, 0)
        sniff(
            iface=config["network_interface"],
            # filter="tcp port 80",
            prn=lambda x: handle_packet(x, traffic_logger, error_logger, redis_client),
            store=False,
        )
    except Exception as e:
        log_error(error_logger, f"Error in packet capture: {e}")


def get_tcp_flag_descriptor(flag_value):
    """Convert numeric TCP flag value to descriptive string based on custom mapping."""
    flags = [
        ("FIN", 0x01, "FPA_"),
        ("SYN", 0x02, "S_"),
        ("RST", 0x04, "R_"),
        ("PSH", 0x08, "PA_"),
        ("ACK", 0x10, "A_"),
        ("URG", 0x20, "URP"),
        ("ECE", 0x40, "ECO"),
        ("CWR", 0x80, "CWR"),
    ]
    result = []
    for desc, mask, custom_desc in flags:
        if flag_value & mask:
            result.append(custom_desc)
    return result


def handle_packet(packet, traffic_logger, error_logger, redis_client):
    sample_rate = 10  # Process 1 out of every 10 packets
    if random.randint(1, sample_rate) != 1:
        return  # Skip this packet based on sampling rate

    try:
        if IP in packet:
            protocol_name = protocol_mapping.get(packet[IP].proto, "Unknown")
            if TCP in packet:
                flow_key = (
                    packet[IP].src,
                    packet[IP].dst,
                    packet[TCP].sport,
                    packet[TCP].dport,
                )
                if flow_key not in flows:
                    flows[flow_key] = {
                        "start_time": time.time(),
                        "packets": 0,
                        "bytes": 0,
                        "flags": set(),
                    }

                flow = flows[flow_key]
                flow["packets"] += 1
                flow["bytes"] += len(packet)
                current_flags = get_tcp_flag_descriptor(packet[TCP].flags)
                flow["flags"].update(current_flags)

                packet_data = {
                    "id": generate_packet_id(),
                    "Duration": time.time() - flow["start_time"],
                    "Protocol": protocol_name,
                    "Source IP": packet[IP].src,
                    "Source Port": packet[TCP].sport,
                    "Destination IP": packet[IP].dst,
                    "Destination Port": packet[TCP].dport,
                    "Flags": list(flow["flags"]),
                    "Packets": flow["packets"],
                    "Bytes": flow["bytes"],
                    "Flows": len(flows),
                }
                log_event(traffic_logger, json.dumps(packet_data))
                redis_client.publish("packet_data", json.dumps(packet_data))
    except Exception as e:
        log_error(error_logger, f"Error processing packet: {e}")
