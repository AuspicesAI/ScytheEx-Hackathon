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

import requests
import redis
import json
import time

# Setting up the Redis connection
redis_host = "localhost"
redis_port = 6381
redis_channel = "ioc_updates"
r = redis.Redis(host=redis_host, port=redis_port, db=0)


def fetch_iocs():
    url = "https://threatfox-api.abuse.ch/api/v1/"
    payload = {"query": "get_iocs", "days": 1}  # Fetch the most recent day's IOCs
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        iocs = response.json().get("data", [])
        return iocs[:1]  # Return only the first IOC
    else:
        print(f"Failed to fetch IOCs, status code: {response.status_code}")
        return []


def store_and_publish_iocs():
    iocs = fetch_iocs()
    for ioc in iocs:
        ioc_key = f"ioc:{ioc['id']}"
        ioc_value = json.dumps(ioc)
        r.set(ioc_key, ioc_value)
        r.expire(ioc_key, 60)  # Set TTL for 60 seconds
        r.publish(redis_channel, ioc_value)  # Publish IOC to Redis channel
    print(f"Published {len(iocs)} IOCs to Redis.")


if __name__ == "__main__":
    while True:
        store_and_publish_iocs()
        time.sleep(1)
