# sodeda-era5

A proof-of-concept software-defined dataset (sodeda) build in the context of the SDSC hackathon 2024.

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

## Quickstart
- Clone the repo and open its folder in a terminal
- [Install rye](https://rye.astral.sh/guide/installation/), then
- Install dependencies with:
```
rye sync --all-features
```

Try out loading directly from the ARCO data source
```
python -c "from sodeda_era5.loader import ARCO_ERA5; print(ARCO_ERA5()(time={'start': '2023-01-01', 'end':'2023-01-02'}, variable=['2m_temperature']))"
```


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

## Preload dataset
A simple example is given by the deskriptor set in `deskriptors.jsonl`. This dataset can be preloaded and stored on the previously configured S3 storage.

To preload run
```
rye run sodeda-era5 preload
```

## Dashboard
A gradio dashboard is available with 

```
rye run sodeda-era5 dashboard
```

Note: Don't try to load the full dataset. I can only display one timestep at a time anyway. Even the full globe for one timestep takes quite some time. I assume, that's mainly due to plotting and transfering to browser, and not the data fetching.