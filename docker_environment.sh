#!/bin/bash
image="python:3.8"

container_name="epfd"
docker stop $container_name

docker pull $image
wandb docker run -d --rm -it --name $container_name --dir "/code/" -v $(pwd)/:/code/ $image bash
docker exec -it $container_name bash -c "apt update && apt install git jupyter-nbconvert -y"
