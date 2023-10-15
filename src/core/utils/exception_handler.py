from functools import wraps
from core.exceptions import CoreException


# this decorator will chain raising exceptions and pipe it
# to the global coreException handler which in return convert
# it to httpException


def exceptionHandler(exception_classes):
    exception_classes = (
        exception_classes
        if isinstance(exception_classes, tuple)
        else (exception_classes)
    )

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exception_classes as e:
                return e.handle_response()
            except ValueError as e:
                raise CoreException(
                    status_code=400,
                    message=str(e),
                    title="value_error",
                )
            except Exception as e:
                print("eto", e)
                raise CoreException(
                    status_code=400,
                    message=str(e),
                    title="value_error",
                )

        return wrapper

    return decorator
