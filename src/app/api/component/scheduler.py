import logging
import asyncio
from asyncio import ensure_future
from functools import wraps
from typing import Callable, Optional

from fastapi.concurrency import run_in_threadpool

logger = logging.getLogger(__name__)


def scheduled(
    *,
    seconds: float,
    wait_first: bool = False,
    raise_exceptions: bool = False,
    max_repetitions: Optional[int] = None,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func) is True:
            raise ValueError("Input function should be non-asynchronous")

        @wraps(func)
        async def wrapped(*args, **kwargs) -> None:
            repetitions = 0

            async def loop() -> None:
                nonlocal repetitions

                if wait_first is True:
                    await asyncio.sleep(seconds)

                while max_repetitions is None or repetitions < max_repetitions:
                    try:
                        if repetitions == 0:
                            # Block API at the first time
                            func(*args, **kwargs)
                        else:
                            await run_in_threadpool(func, *args, **kwargs)

                        repetitions += 1
                    except Exception as exc:
                        if raise_exceptions is True:
                            raise exc

                    await asyncio.sleep(seconds)

            ensure_future(loop())

        return wrapped

    return decorator
