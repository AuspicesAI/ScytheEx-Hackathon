import redis
import json

def main():
    # Setup Redis connection
    r = redis.Redis(host="2.tcp.eu.ngrok.io", port=11272, db=0)

    # Subscribe to the channel
    pubsub = r.pubsub()
    pubsub.subscribe('processed_data_channel')

    print("Subscribed to 'processed_data_channel'. Waiting for data...")
    # Listen for new messages
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            print("Received data:", data)
            # Further processing can be done here

if __name__ == "__main__":
    main()
