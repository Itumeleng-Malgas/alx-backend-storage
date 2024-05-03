#!/usr/bin/env python3
"""  Implementing an expiring web cache and tracker """
import requests
import redis
import time
from functools import wraps
from typing import Callable


def cache_with_expiry(expiration: int) -> Callable:
    """Decorator to cache function results with expiration time"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"cache:{func.__name__}:{args}"
            redis_client = redis.Redis()
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return cached_result.decode("utf-8")
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, result)
            return result
        return wrapper
    return decorator


def track_access(func: Callable) -> Callable:
    """Decorator to track the number of accesses to a URL"""

    @wraps(func)
    def wrapper(url: str) -> str:
        redis_client = redis.Redis()
        count_key = f"count:{url}"
        count = redis_client.incr(count_key)
        return func(url)
    return wrapper


@cache_with_expiry(10)
@track_access
def get_page(url: str) -> str:
    """Fetches HTML content from a URL"""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/"
    "https://www.example.com"
    print(get_page(url))
    time.sleep(5)  # Wait for cache expiry
    print(get_page(url))  # Cache should still be valid
