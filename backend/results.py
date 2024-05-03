import redis


def main():
    # Configure the Redis connection
    redis_host = "5.tcp.eu.ngrok.io"
    redis_port = 19779

    # Create a Redis connection
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

    # Create a pub/sub object
    pubsub = r.pubsub()

    # Subscribe to a test channel
    pubsub.subscribe("prediction_channel")

    # Listen for messages on the channel
    print("Listening for messages on 'prediction_channel'. Press Ctrl+C to exit.")
    try:
        for message in pubsub.listen():
            if message["type"] == "message":
                print(f"Received: {message['data']}")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Unsubscribe and close the connection
        pubsub.unsubscribe("prediction_channel")
        r.close()


if __name__ == "__main__":
    main()
