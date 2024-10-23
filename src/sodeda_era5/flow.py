import json
import fsspec 
import os 
import io
import hashlib
from .loader import ARCO_ERA5
from compress_pickle import dump, load
from dotenv import load_dotenv, find_dotenv
import pandas as pd 

load_dotenv(find_dotenv())

class Era5Flow():
    def __init__(self,store_samples=True):
        cache_storage = os.environ.get("LOCAL_CACHE",None)
        fs = fsspec.filesystem(
            "s3", endpoint_url=os.environ.get("S3_ENDPOINT_URL",None), profile=os.environ["S3_PROFILE"]
        )
        if cache_storage is not None:
            fs = fsspec.filesystem("filecache", fs=fs, cache_storage=cache_storage)
        self.store = fs.get_mapper(f'{os.environ["S3_BUCKET_NAME"]}/f"{os.environ["S3_BASE_KEYNAME"]}/')
        self.loader = ARCO_ERA5()
        self.store_samples = store_samples

    def scope(self):
        return self.loader.scope()
    
    def __call__(self, **deskriptor):
        deskriptor_hash = hash_dict(deskriptor)
        if deskriptor_hash in self.store and self.store_samples:
            return read_pickle_with_store(self.store,deskriptor_hash)
        
        data = self.loader(**deskriptor)

        if self.store_samples:
            to_pickle_with_store(self.store,deskriptor_hash,data)

        return data


def convert(object):
    if isinstance(object,pd.Timestamp):
        return object.isoformat()
    return object


def hash_dict(d):
    dict_string = json.dumps(d, sort_keys=True, default=convert).encode("utf-8")
    filehash = hashlib.md5(dict_string).hexdigest()
    return filehash

def to_pickle_with_store(store, filename, object, compression="gzip"):
    bytes_buffer = io.BytesIO()
    dump(object, bytes_buffer, compression=compression)
    store[filename] = bytes_buffer.getvalue()


def read_pickle_with_store(store, filename, compression="gzip"):
    bytes_buffer = io.BytesIO(store[str(filename)])
    return load(bytes_buffer, compression=compression)

        