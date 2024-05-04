#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from datetime import timedelta

def cache_with_expiry(expiration: int):
    '''Decorator to cache function results with expiration time'''
    def decorator(func):
        def wrapper(url):
            redis_store = redis.Redis()
            res_key = f'result:{url}'
            req_key = f'count:{url}'
            result = redis_store.get(res_key)
            if result is not None:
                redis_store.incr(req_key)
                return result.decode('utf-8')
            result = func(url)
            redis_store.setex(res_key, timedelta(seconds=expiration), result)
            return result
        return wrapper
    return decorator

@cache_with_expiry(10)
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    if url is None or not url.strip():
        return ''
    return requests.get(url).content.decode('utf-8')
