* sudo apt install git-lfs python3-pip
* git submodule update --init --recursive
* python3 -m pip install -q -U pip wandb
* wandb login
* bash docker_environment.sh
* docker exec -it epfd bash
* bash convert_notebook_to_script.sh
* ipython wandb_data.py
* wandb agent nicojahn/htcv/2pwlb1oe