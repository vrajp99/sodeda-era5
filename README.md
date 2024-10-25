# sodeda-era5

A proof-of-concept software-defined dataset (sdd) build in the context of the SDSC hackathon 2024.

The sodeda consists of these components
- A set of deskriptors
    - Each deskriptor describes an element of the dataset. 
    - In this case, hourly temperature measurements in the area of Zürich.
- A flow
    - A flow is a processing pipeline which loads data from a data source and optionally it into the desired representation 
    - In this case, we load ERA5 data from ARCO-ERA5 and convert it into a xarray DataArray.
- A storage
    - The storage is used to cache individual data samples close to the user's compute environment for faster access during tasks such as ML training.
    - In this case, we use an S3 storage but local cache could be used as well

## Setup S3 storage
First add your S3 credentials to your `~/.aws/credentials` under a new profile. For example

```
[your-profile-name]
aws_access_key_id = your-key
aws_secret_access_key = your-secret
```

Create a `.env` file by copying the template

```
cp .env.example .env
```

Then modify the content to fit your S3 bucket.
```
# Name of the bucket
S3_BUCKET_NAME=
# anything that should be prefixed to the keys created by this sodeda
S3_KEY_PREFIX=sodeda-era5
# Optional: Name of the custom endpoint
S3_ENDPOINT_URL=
# The name of the profile in ~/.aws/credentials
S3_PROFILE=your-profile-name
# Optional: Path to local cache
LOCAL_CACHE=./.cache
```

## Setup the pipeline:
Run the `setup.py` script with `python3 setup.py`

## Build the container image:
Go to the docker directory and then run the build script:
```bash
cd ./docker
sudo ./build.sh
```

## Run and access the Gradio pipeline:
1. In the docker directory, run `sudo ./run-gradio.sh`
2. Now, in your browser open [localhost:7860](https://localhost:7860)