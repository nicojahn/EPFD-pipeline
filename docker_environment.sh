#!/bin/bash
image="python:3.8"

container_name="epfd"
docker stop $container_name

docker pull $image
wandb docker run -d --rm -it --name $container_name --dir "/app" $image
docker exec -it $container_name bash -c "apt update && apt install git jupyter jupyter-nbconvert python3-ipython ffmpeg libsm6 libxext6 -y && cd /app && python3 -m pip install -r requirements.txt"

#tmux new-session -d 'docker exec -it epfd bash -c "wandb agent nicojahn/htcv/rwr1kwis"'
