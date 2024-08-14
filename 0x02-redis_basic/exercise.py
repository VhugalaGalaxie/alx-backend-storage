#!/usr/bin/env python3
"""
Redis module, Writing strings to Redis
Reading from Redis and recovering original type
Incrementing values, storing lists, Retrieving lists
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Prototype: def count_calls(method: Caallable) -> Callable:
    Returns a Callable
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        Prototype: def wrapper(self, *args, **kwds):
        Returns wrapper
        """
        key_m = method.__qualname__
        self._redis.incr(key_m)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Prototype: def call_history(method: Callable) -> Callable:
    Returns a Callable
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        Prototype: def wrapper(self, *args, **kwds):
        Returns wrapper
        """
        key_m = method.__qualname__
        inp_m = key_m + ':inputs'
        outp_m = key_m + ":outputs"
        data = str(args)
        self._redis.rpush(inp_m, data)
        fin = method(self, *args, **kwds)
        self._redis.rpush(outp_m, str(fin))
        return fin
    return wrapper


def replay(func: Callable):
    """
    Prototype: def replay(func: Callable):
    Displays history of calls of a particular function
    """
    r = redis.Redis()
    key_m = func.__qualname__
    inp_m = r.lrange("{}:inputs".format(key_m), 0, -1)
    outp_m = r.lrange("{}:outputs".format(key_m), 0, -1)
    calls_number = len(inp_m)
    times_str = 'times'
    if calls_number == 1:
        times_str = 'time'
    fin = '{} was called {} {}:'.format(key_m, calls_number, times_str)
    print(fin)
    for k, v in zip(inp_m, outp_m):
        fin = '{}(*{}) -> {}'.format(
            key_m, k.decode('utf-8'), v.decode('utf-8'))
        print(fin)


class Cache:
    '''Represents an object for storing data in a Redis data storage.
    '''
    def __init__(self) -> None:
        '''Initializes a Cache instance.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores a value in a Redis data storage and returns the key.
        '''
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        '''Retrieves a value from a Redis data storage.
        '''
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        '''Retrieves a string value from a Redis data storage.
        '''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''Retrieves an integer value from a Redis data storage.
        '''
        return self.get(key, lambda x: int(x))
