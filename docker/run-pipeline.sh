#!/bin/bash
docker run \
   -v ../:/repo \
   sodeda:v1\
   /bin/bash -c "conda activate runenv && cd /repo && python -c \"from src.sodeda_era5 import dashboard; dashboard()\""