import aiohttp
import asyncio
import random
import time
from typing import Callable, Any
import functools


def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'Starting {func.__name__} with {args} {kwargs}')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'Finished {func.__name__} in {total:.4f} second(s).')

        return wrapped

    return wrapper


@async_timed()
async def fetch(session, url):
    try:
        async with session.get(url, timeout=6) as response:
            return response.status
    except asyncio.TimeoutError:
        print(f'Timeout error for URL: {url}')
        return None
    except Exception as e:
        print(f'Exception {e} for URL: {url}')
        return None


@async_timed()
async def main():
    urls = [f'https://httpbin.org/delay/{random.randint(0, 10)}' for _ in range(20)]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                print(f'Status: {result}')
            else:
                print('Failed to get status.')


asyncio.run(main())
