#!/usr/bin/env python3
""" Writing strings to Redis """

from typing import Union, Optional, Callable
import redis
import uuid


class Cache:
    """ A class for caching data using Redis. """

    def __init__(self):
        """
        Creates a Redis client and flush the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
            """ Stores data in the cache and returns the generated key. """
            key = str(uuid.uuid4())
            self._redis.set(key, data)
            return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float, None]:
                """ Retrieves data from the cache using the specified key and
                optionally applies a conversion function.
                """
                data = self._redis.get(key)
                if data is not None and fn is not None:
                    return fn(data)
                return data

    def get_str(self, key: str) -> str:
        """ Retrieves a string value from the cache. """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """ Retrieves an integer value from the cache. """
        return self.get(key, int)
