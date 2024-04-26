#!/bin/bash

echo "Starting redis using docker at port 6379..."

docker run --name my-redis -p 6379:6379 -d redis
docker exec -it my-redis redis-cli
