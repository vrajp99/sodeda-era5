# sodeda-era5
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