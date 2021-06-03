#!/bin/bash
image="python:3.9"

container_name="epfd"
docker stop $container_name

docker pull $image
docker run -d --rm -it --name $container_name -v $(pwd)/:/epfd/ $image bash
docker exec -it $container_name bash -c "cd epfd/EPFD/ && python3 -m pip install -r requirements.txt && python3 -m pip install -e ./PyEnsemble"
