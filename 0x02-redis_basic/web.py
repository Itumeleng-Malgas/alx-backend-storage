#!/usr/bin/env python3
"""A module with tools for request caching and tracking."""
import redis
import requests
from datetime import timedelta


def cache_and_track(func):
    """Decorator to cache function results and track URL accesses."""
    def wrapper(url):
        if url is None or len(url.strip()) == 0:
            return ''
        redis_store = redis.Redis()
        res_key = f"result:{url}"
        req_key = f"count:{url}"
        result = redis_store.get(res_key)
        if result is not None:
            redis_store.incr(req_key)
            return result.decode("utf-8")
        result = func(url)
        redis_store.setex(res_key, timedelta(seconds=10), result)
        return result
    return wrapper


@cache_and_track
def get_page(url):
    """Returns the content of a URL after caching the request's response,
    and tracking the request."""
    return requests.get(url).content.decode("utf-8")

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/https://www.example.com"
    print(get_page(url))
    print(get_page(url))
