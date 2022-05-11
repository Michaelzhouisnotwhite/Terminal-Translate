from .settings import REQUEST_URL
import requests


def get_trans(*args, **kwargs):
    result = requests.post(REQUEST_URL, *args, **kwargs)
    rjson = result.json()
    return rjson
