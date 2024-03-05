import os
import pickle

from data.models import Tx
from data.config import CACH_PATH


def read_cache_from_file(path: str = CACH_PATH) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data


def write_cache_to_file(data: object, path: str = CACH_PATH):
    with open(path, 'wb') as f:
        pickle.dump(data, f)


def my_cach(func):
    def wrapper(*args, **kwargs):
        data: dict[str, Tx] = read_cache_from_file()
        version = kwargs.get('version')
        if version in data:
            return data[version]
        tx: Tx = func(*args, **kwargs)
        data[tx.version] = tx
        write_cache_to_file(data=data)
        return tx
    return wrapper
