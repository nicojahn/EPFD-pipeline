#!/bin/bash
image="python:3.8"

container_name="epfd"
docker stop $container_name

docker pull $image
wandb docker run -d --rm -it --name $container_name --dir "/app" $image
docker exec -it $container_name bash -c "apt update && apt install git jupyter jupyter-nbconvert python3-ipython ffmpeg libsm6 libxext6 -y"
docker exec -it $container_name bash -c "python3 -m pip install -q -U pip && python3 -m pip install -r requirements.txt && python3 -m pip install -q -U -r ./EPFD/requirements.txt && python3 -m pip install -q -e ./EPFD/PyEnsemble"
docker exec -it $container_name bash -c "bash convert_notebook_to_script.sh"

#tmux new-session -d 'docker exec -it epfd bash -c "wandb agent nicojahn/htcv/rwr1kwis"'
