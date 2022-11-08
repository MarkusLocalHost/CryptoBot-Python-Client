import asyncio
import concurrent.futures
from functools import partial


async def run_blocking_io(func, url, headers, data=None):
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, partial(func, url=url, data=data, headers=headers)
        )

    return result
