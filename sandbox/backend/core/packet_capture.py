import pcapy
from scapy.all import Ether, IP, TCP  # type: ignore
from core.logging import log_event, log_error
import uuid
import time
import json
import redis


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
        cap = pcapy.open_live(config["network_interface"], 65536, True, 0)
        log_event(
            traffic_logger, f"Started packet capture on {config['network_interface']}"
        )
        redis_client = connect_to_redis(
            config["redis_traffic_host"],
            config["redis_traffic_port"],
            config["redis_traffic_db_index"],
        )

        while True:
            (header, packet) = cap.next()
            if packet:
                handle_packet(packet, traffic_logger, error_logger, redis_client)
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
    try:
        scapy_packet = Ether(packet)
        if IP in scapy_packet and TCP in scapy_packet:
            flow_key = (
                scapy_packet[IP].src,
                scapy_packet[IP].dst,
                scapy_packet[TCP].sport,
                scapy_packet[TCP].dport,
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
            flow["bytes"] += len(scapy_packet)
            # Get and update flags
            current_flags = get_tcp_flag_descriptor(scapy_packet[TCP].flags)
            flow["flags"].update(current_flags)

            packet_data = {
                "id": generate_packet_id(),
                "Duration": time.time() - flow["start_time"],
                "Protocol": scapy_packet[IP].proto,
                "Source IP Address": scapy_packet[IP].src,
                "Source Port": scapy_packet[TCP].sport,
                "Destination IP Address": scapy_packet[IP].dst,
                "Destination Port": scapy_packet[TCP].dport,
                "Flags": list(flow["flags"]),
                "Packets": flow["packets"],
                "Bytes": flow["bytes"],
                "Flows": len(flows),
            }
            log_event(traffic_logger, json.dumps(packet_data))
            # Publish packet data to Redis
            redis_client.publish("packet_data", json.dumps(packet_data))
    except Exception as e:
        log_error(error_logger, f"Error processing packet: {e}")
