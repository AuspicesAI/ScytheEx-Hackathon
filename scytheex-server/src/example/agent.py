import socket
import json
import time


def generate_data():
    # Simulate data generation (e.g., logs, events)
    data = {
        "timestamp": time.time(),
        "event": "user_login",
        "user": "example_user",
        "status": "success",
    }
    return json.dumps(data)


def send_data_to_server(data, server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, server_port))
        s.sendall(data.encode("utf-8"))
        response = s.recv(1024)
        print("Received", response.decode("utf-8"))


if __name__ == "__main__":
    server_ip = "127.0.0.1"
    server_port = 8080

    while True:
        data = generate_data()
        send_data_to_server(data, server_ip, server_port)
        time.sleep(5)  # Send data every 5 seconds