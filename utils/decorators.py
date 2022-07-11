from time import time
from functools import wraps

from config import DEVELOPER_MODE


def time_debugger(func):
    if DEVELOPER_MODE:
        @wraps(func)
        def wrapper(*args, **kwargs):
            time_s = time()
            res = func(*args, **kwargs)
            time_e = time()
            print(f"{func.__qualname__}: {time_e - time_s}s")
            return res
        return wrapper
    else:
        return func
