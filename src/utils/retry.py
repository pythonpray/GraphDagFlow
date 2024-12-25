import asyncio
import logging
from typing import Callable, Optional, Tuple, Any
from functools import wraps


class RetryStrategy:
    """the base class of the retry policy"""

    def get_delay(self, attempt: int, base_delay: float) -> float:
        raise NotImplementedError


class ExponentialBackoff(RetryStrategy):
    """exponential fallback strategy"""

    def __init__(self, max_delay: float = 60.0):
        self.max_delay = max_delay

    def get_delay(self, attempt: int, base_delay: float) -> float:
        delay = min(base_delay * (2 ** (attempt - 1)), self.max_delay)
        return delay


class LinearBackoff(RetryStrategy):
    """linear fallback strategy"""

    def get_delay(self, attempt: int, base_delay: float) -> float:
        return base_delay * attempt


def retry(
        attempts: int = 3,
        delay: float = 1.0,
        retry_exceptions: Optional[Tuple[type]] = None,
        strategy: RetryStrategy = LinearBackoff(),
        logger: Optional[logging.Logger] = None,
        log_level: int = logging.WARNING,
) -> Callable:
    """
    asynchronous retry decorators

    Args:
        attempts (int): maximum number of retries
        delay (float): base delay time seconds
        retry_exceptions (Optional[Tuple[type]]): Retries are performed only for the specified exception type
        strategy (RetryStrategy): retryDelayPolicy
        logger (Optional[logging.Logger]): custom loggers
        log_level (int): logLevel

    Example:
        @retry(attempts=3, delay=1.0)
        async def my_function():
            pass
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            log = logger or logging.getLogger(func.__module__)

            for attempt in range(1, attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if retry_exceptions and not isinstance(e, retry_exceptions):
                        raise

                    last_exception = e
                    remaining = attempts - attempt

                    error_msg = (
                        f"Attempt {attempt}/{attempts} failed for {func.__name__}. "
                        f"Remaining attempts: {remaining}. Error: {str(e)}"
                    )

                    log.log(log_level, error_msg)

                    if remaining > 0:
                        delay_time = strategy.get_delay(attempt, delay)
                        await asyncio.sleep(delay_time)
                    else:
                        log.error(
                            f"All {attempts} attempts failed for {func.__name__}. "
                            f"Final error: {str(last_exception)}"
                        )
                        raise last_exception

        return wrapper
    return decorator
