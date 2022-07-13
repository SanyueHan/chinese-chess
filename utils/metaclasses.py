import sys
from collections import defaultdict


class CacheMeta(type):
    """
    A metaclass that reload __call__ to add a cache for instances.
    """

    _instances = {}
    _miss = defaultdict(int)
    _hit = defaultdict(int)

    def __call__(cls, *args, **kwargs):
        key = (cls, str(args), str(kwargs))
        if key not in cls._instances:
            cls._miss[cls] += 1
            cls._instances[key] = super(CacheMeta, cls).__call__(*args, **kwargs)
        else:
            cls._hit[cls] += 1
        return cls._instances[key]

    def debug_cache(cls):
        print(f"cache hit: {cls._hit[cls]}")
        print(f"cache miss: {cls._miss[cls]}")
        print(f"cache size (KB): {cls._instances.__sizeof__() // 1000}")
        print(f"cache size (KB): {sys.getsizeof(cls._instances) // 1000}")
