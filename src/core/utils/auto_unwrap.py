from functools import wraps


def exceptionHandler(args):
    args_inner = args
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(args,kwargs)

        return wrapper

    return decorator
