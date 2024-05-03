#!/usr/bin/env python3
""" Writing strings to Redis """

from typing import Union
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
