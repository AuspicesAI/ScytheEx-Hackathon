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

import redis


def main():
    # Configure the Redis connection
    redis_host = "0.tcp.eu.ngrok.io"
    redis_port = 16959

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
