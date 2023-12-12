import logging
import functools

logging.basicConfig(level = logging.INFO)

def log_args(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logging.info(f"Calling {func.__name__}({signature})")
        return func(*args, **kwargs)
    return wrapper