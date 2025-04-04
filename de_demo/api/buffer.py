import abc
import asyncio
import logging
from typing import Generic, TypeVar

logger = logging.getLogger('uvicorn.asgi')

T = TypeVar("T")


class AsyncBuffer(Generic[T], abc.ABC):
    def __init__(
        self,
        *,
        max_buffer_size: int = 1000000,
        max_queue_time: float = 10.0,
        max_batch_size: int = 100000,
        **_,
    ):
        super().__init__()
        if max_buffer_size < 1:
            raise ValueError("max_buffer_size must be gte 1")
        if max_batch_size < 1:
            raise ValueError("max_batch_size must be gte 1")

        self._queue = asyncio.Queue(max_buffer_size)

        self.max_queue_time = max_queue_time
        self.max_batch_size = max_batch_size
        self._stop = asyncio.Event()
        self._is_running = asyncio.Event()
        self._current_task: asyncio.Task | None = None

    @abc.abstractmethod
    async def process_batch(self, batch: list[T]):
        raise NotImplementedError

    async def append(self, item: T):
        if self._stop.is_set():
            raise RuntimeError("Batcher is stopped")

        if self._current_task is None:
            self._current_task = asyncio.create_task(self.run())

        await self._queue.put(item)

    async def _fill_batch_from_stream(self) -> list[T]:
        started_at = asyncio.get_running_loop().time()
        try:
            batch = [await asyncio.wait_for(self._queue.get(), timeout=self.max_queue_time)]
        except asyncio.TimeoutError:
            return []
        while self.max_queue_time - (asyncio.get_running_loop().time() - started_at) > 0:
            try:
                batch.append(await asyncio.wait_for(
                    self._queue.get(),
                    timeout=self.max_queue_time - (asyncio.get_running_loop().time() - started_at)
                ))
            except asyncio.TimeoutError:
                break
            if 0 < self.max_batch_size <= len(batch):
                break
        return batch

    async def run(self):
        self._is_running.set()

        done, pending = set(), set()

        while not self._should_stop():
            batch = await self._fill_batch_from_stream()

            if batch:
                task = asyncio.create_task(self.process_batch(batch))
                logger.info(f"{self.__class__.__name__} sending batch {len(batch)} with task {task.get_name()}")
                pending.add(task)

            if len(pending) > 0:
                done, pending = await asyncio.wait(
                    pending,
                    timeout=1,
                    return_when=asyncio.FIRST_COMPLETED
                )
            for t in done:
                if t.exception():
                    logger.info(f"{self.__class__.__name__} task {t.get_name()} exception {t.exception()}")
                else:
                    logger.info(f"{self.__class__.__name__} task {t.get_name()} completed")
            done = set()

        if len(pending) > 0:
            await asyncio.wait(pending, timeout=5, return_when=asyncio.ALL_COMPLETED)
        self._is_running.clear()

    def _should_stop(self):
        return self._stop.is_set() and self._queue.empty()

    async def empty(self, timeout: float) -> bool:
        return await asyncio.wait_for(
            asyncio.create_task(self._is_empty()),
            timeout
        )

    async def _is_empty(self) -> bool:
        while not self._queue.empty():
            pass
        return True

    async def is_running(self):
        return self._is_running.is_set()

    async def stop(self):
        logger.info(f"stop buffer {self.__class__.__name__}")
        self._stop.set()
        if (
                self._current_task
                and not self._current_task.done()
                and not self._current_task.get_loop().is_closed()
        ):
            await asyncio.wait_for(self._current_task, timeout=self.max_queue_time)
