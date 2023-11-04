import os
import functools
from ilock import ILock


def uses_lock(f):
    """
    Wraps the entire call in a global lock.
    :param f: The wrapped function.
    :return: A wrapping function.
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        with ILock("semperland.cache"):
            return f(*args, **kwargs)

    return wrapper
