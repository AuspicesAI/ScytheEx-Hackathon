import sys
import uuid
import redis
import json

# Setup Redis connection
r = redis.Redis(
    host="2.tcp.eu.ngrok.io", port=11272, db=0
)  # Update with your Redis server details


def process_data(data):
    # Split the incoming data string into key-value pairs
    data_pairs = data.split(", ")
    data_dict = {}

    # Extract values based on the key
    for pair in data_pairs:
        key, val = pair.split(": ")
        data_dict[key.strip()] = val.strip()

    # Map the extracted values to the titles
    processed_data = {
        "dur": data_dict.get("Duration", "").split()[0],
        "proto": data_dict.get("Protocol", ""),
        "service": data_dict.get("Service", ""),
        "state": data_dict.get("State", ""),
        "stcpb": data_dict.get("TCP Sequence Number", ""),
        "dtcpb": data_dict.get("Destination TCP Acknowledgement Number", ""),
        "synack": data_dict.get("SYN to SYN_ACK Time", "").split()[0],
        "ackdat": data_dict.get("SYN_ACK to ACK Time", "").split()[0],
        "trans_depth": data_dict.get("HTTP Transaction Depth", ""),
        "response_body_len": data_dict.get("Last HTTP Response Body Length", ""),
        "ct_src_dport_ltm": data_dict.get(
            "Number of connections for the same src address and dst port", ""
        ),
        "ct_dst_sport_ltm": data_dict.get(
            "Number of connections for the same dst address and src port", ""
        ),
        "is_ftp_login": "1" if data_dict.get("Is FTP Login", "") == "Yes" else "0",
        "ct_ftp_cmd": data_dict.get("FTP Command Count", ""),
        "ct_flw_http_mthd": data_dict.get("HTTP Methods Count", ""),
        "is_sm_ips_ports": (
            "1"
            if data_dict.get("Are Source and Destination Same", "") == "Yes"
            else "0"
        ),
    }

    # Convert the dictionary to JSON string
    return json.dumps(processed_data)


def main():
    for line in sys.stdin:
        data = line.strip()
        processed_data = process_data(data)

        # Generate a unique key for each piece of data
        unique_key = str(uuid.uuid4())

        # Publish the data to a specific channel (optional)
        r.publish("processed_data_channel", processed_data)

        # Store the data with an expiration time
        r.set(unique_key, processed_data, ex=60)

        # print(processed_data)  # Optionally print the processed data for verification


if __name__ == "__main__":
    main()
