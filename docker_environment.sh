#!/bin/bash
image="python:3.9"

container_name="epfd"
docker stop $container_name
docker rm $container_name

docker pull $image
docker run -it --name $container_name -v $(pwd)/:/epfd/ $image bash
