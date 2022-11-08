import requests

from utils.misc.run_blocking_io import run_blocking_io


async def make_request_post(url, headers, data):
    response = await run_blocking_io(requests.post, url, headers, data)
    return response


async def make_request_get(url, headers):
    response = await run_blocking_io(requests.get, url, headers)
    return response
