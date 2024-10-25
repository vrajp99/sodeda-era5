#!/bin/bash
REPO_DIR="/home/vpatel/hackathon/sodeda-era5"
AWS_CRED_DIR="$HOME/.aws/"
docker run \
   -v $REPO_DIR:/repo \
   -v $AWS_CRED_DIR:$HOME/.aws/\
   -p 7860:7860\
   sodeda:v1\
   /bin/bash -c "source ~/miniconda3/bin/activate && conda activate runenv && cd /repo && python -c \"from src.sodeda_era5 import dashboard; dashboard()\""