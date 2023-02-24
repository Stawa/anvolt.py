import asyncio
from typing import Any, Callable, Coroutine, TypeVar

coroutine = TypeVar("coroutine", bound=Callable[..., Coroutine[Any, Any, Any]])


class Event:
    def __init__(self):
        self.callbacks = {}

    async def call_event(self, event_type, **kwargs) -> None:
        if event_type in self.callbacks:
            for callback in self.callbacks[event_type]:
                await callback(**kwargs)

    def event(self, coro: coroutine, /) -> coroutine:
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError("The registered event must be a coroutine function.")

        event_type = coro.__name__
        if event_type not in self.callbacks:
            self.callbacks[event_type] = []
        self.callbacks[event_type].append(coro)

        return coro

    def handle_coroutine_exception(self, task: asyncio.Task) -> None:
        try:
            task.result()
        except (asyncio.CancelledError, Exception) as e:
            pass

    def task_loop(self, loop: asyncio.AbstractEventLoop, coro: coroutine):
        try:
            loop.create_task(coro).add_done_callback(self.handle_coroutine_exception)
        except RuntimeError:
            pass
