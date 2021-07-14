# Description
    * This work represents the progress of a TU Berlin class during my master studies
    * It is based on the paper and implementation of "Ensemble pruning based on objection maximization with a general distributed framework" by Bian, Yijun, et al. from 2019 (Visit their repo: https://github.com/eustomaqua/EPFD)
    * I've build a wrapper around their implementation to tackle the proposed task (ensemble pruning on already trained sematic segmentation decision tree classifiers)
    * This code is not intended to be used as a module (clearly just a pipeline for using EPFD)
    * The segmentation was done with the data from the 2018 IEEE GRSS Data Fusion Challenge: https://hyperspectral.ee.uh.edu/?page_id=1075
    * We actually compare multiple pruning methods together. Check the parent repo with the other implementations: https://github.com/ThomSab/HTCV
    * I use Weights&Biases to track and launch my experiments (therefore it has limitations as described in the FAQ)
    * I publish the pipeline code under BSD 3-Clause License (Note: EPFD itself is published under MIT)

# Prerequisites and commands
### Having python3, pip and Git LFS installed
    * sudo apt install git-lfs python3-pip
### Installed docker for runs: https://docs.docker.com/engine/install/ubuntu/
### Cloned this repo and checked out all submodules
    * git submodule update --init --recursive
### Installed and upgraded pip and W&B
    * python3 -m pip install -q -U pip wandb
### Logged in to your W&B account
    * wandb login
### Prepared environment
    * bash docker_environment.sh
### Logged into the container and executed data preparation once (sending artifacts to W&B)
    * docker exec -it epfd bash
    * ipython wandb_data.py
    * exit
### Started a sweep (e.g. '2pwlb1oe') with your account and project (e.g. 'nicojahn/htcv')
    * wandb agent nicojahn/htcv/2pwlb1oe
### Evaluated after all experiments have finished
    * docker exec -it epfd bash
    * jupyter nbconvert --to script evaluation.ipynb
    * ipython evaluation.py
    * exit

# Conclusion
    * The methods 'COMEP' and 'DOMEP' as presented by Bian, Yijun, et al. are great(ish)
    * They have approximation factors, which can guarantee you at least 50% (for COMEP) of the optimal solution (with respect to the first randomly chosen ensemble member)
    * BUT: This method takes a lot of computations (quadratic increase with the input classifier sizes and ensemble size) and was therefore not feasible to prune from 140 classifiers in a reasonable amount of time on a CPU (5 out of 140 ~= 3.5 hours and 7 out of 140 ~= 8 hours)

# FAQ
## The data is not directly accessible?
    * It isn't, because i do not own the data we optimized on (needs a LICENSE) and i don't want to expose the test API
    * Train your own classifiers and structure them in a similar fashion as shown in 'data_tree.txt'
## It doesn't run out-of-the-box!
    * Sure, as i performed my experiments with Weights&Biases (wandb.ai)
    * You probably need an account to perform the same actions as i did (the free tier is enough)
## Have you any experimental results?
    * I've added a JSON file ('experiment_output.json') to give you the opportunity to have a look into the quality etc.
    * Also the notebook 'evaluation.ipynb' was left uncleared, to give you a perspective on more parameters/behaviours and to keep the latex output for me to copy later on if necessary