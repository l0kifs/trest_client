import functools
import inspect
import logging


def log(logger: logging.Logger = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_logger = logger if logger is not None else logging.getLogger(func.__name__)

            try:
                args_names = inspect.signature(func).parameters.keys()
                args_dict = dict(zip(args_names, args))
                args_repr = [f"{k}={v}" for k, v in args_dict.items()]
                kwargs_repr = [f"{k}={v}" for k, v in kwargs.items()]
                signature = ", ".join(args_repr + kwargs_repr)
                func_logger.debug(f"function {func.__name__} called with args {signature}")
            except:
                func_logger.debug(f"function {func.__name__} called")

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                func_logger.exception(f"Exception raised in {func.__name__}", exc_info=True)
                raise e

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        wrapper.__qualname__ = func.__qualname__

        return wrapper
    return decorator


# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
# @log()
# def my_func(qwer):
#     print("hello world")
# my_func("qqq")
