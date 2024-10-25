mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
# Activate
source ~/miniconda3/bin/activate
conda create -y -c conda-forge --name runenv --file /scripts/requirements.txt && conda clean -afy