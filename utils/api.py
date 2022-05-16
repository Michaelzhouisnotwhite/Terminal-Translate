from .settings import REQUEST_URL
import requests


class RequestError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def get_trans(*args, params=None,  **kwargs):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    req = requests.post(REQUEST_URL, *args, params=params,  headers=headers, **kwargs)
    if req.status_code == requests.codes.ok:
        return req.json()
    raise RequestError
