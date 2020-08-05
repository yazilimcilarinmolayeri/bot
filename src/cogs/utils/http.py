# -*- coding: utf-8 -*-
#
# Kaynak: https://github.com/AlexFlipnote/discord_bot.py/blob/master/utils/http.py
# aiohttp docs: https://docs.aiohttp.org/en/stable/

import asyncio
import aiohttp
from functools import wraps


def async_cache(maxsize=128):
    cache = {}

    def decorator(func):
        @wraps(func)
        async def inner(*args, no_cache=False, **kwargs):
            if no_cache:
                return await func(*args, **kwargs)

            key_base = "_".join(str(x) for x in args)
            key_end = "_".join(f"{k}:{v}" for k, v in kwargs.items())
            key = f"{key_base}-{key_end}"

            if key in cache:
                return cache[key]

            res = await func(*args, **kwargs)

            if len(cache) > maxsize:
                del cache[list(cache.keys())[0]]
                cache[key] = res

            return res

        return inner

    return decorator


class HTTPSession(aiohttp.ClientSession):
    """Abstract class for aiohttp."""

    def __init__(self, loop=None):
        super().__init__(loop=loop or asyncio.get_event_loop())

    def __del__(self):
        if not self.closed:
            await self.close()


session = HTTPSession()


@async_cache()
async def query(url, method="get", res_method="text", *args, **kwargs):
    async with getattr(session, method.lower())(url, *args, **kwargs) as res:
        return await getattr(res, res_method)()


async def get(url, *args, **kwargs):
    return await query(url, "get", *args, **kwargs)


async def post(url, *args, **kwargs):
    return await query(url, "post", *args, **kwargs)
