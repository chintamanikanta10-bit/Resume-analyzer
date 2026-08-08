import time
from functools import wraps
from core.logger import logger


def retry(max_attempts=3, delay=2):
    """
    Retry decorator for temporary failures.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            last_exception = None

            for attempt in range(1, max_attempts + 1):

                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    last_exception = e

                    logger.warning(
                      f"Attempt {attempt} failed. "
                      f"Retrying in {delay} seconds..."
                    )

                    time.sleep(delay)

            raise last_exception

        return wrapper

    return decorator