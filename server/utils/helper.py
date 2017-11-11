from functools import wraps


def print_exceptions(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except Exception as e:
            print(e)
    return wrapped
