import traceback
from functools import wraps


def print_exceptions(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except Exception as e:
            print(traceback.format_exc())
    return wrapped
