* sudo apt install git-lfs python3-pip
* git submodule update --init --recursive
* python3 -m pip install -q -U pip wandb
* wandb login
* bash docker_environment.sh
* docker exec -it epfd bash
* convert_notebook_to_script_and_execute.sh
* ipython wandb_data.py
* wandb agent nicojahn/htcv/5u9mgel7
