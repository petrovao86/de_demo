import pytest
import pytest_asyncio

from de_demo.api.buffer import AsyncBuffer


class Buffer(AsyncBuffer[int]):
    def __init__(
        self,
        *,
        max_buffer_size: int = 1,
        max_queue_time: float = 10,
        max_batch_size: int = 2,
        **kwargs,
    ):
        super().__init__(
            max_buffer_size=max_buffer_size, max_queue_time=max_queue_time, max_batch_size=max_batch_size, **kwargs
        )
        self.buff = []

    async def process_batch(self, batch: list[int]):
        self.buff += batch


@pytest_asyncio.fixture()
async def buffer():
    b = Buffer()
    try:
        yield b
    finally:
        await b.stop()


@pytest.mark.asyncio()
async def test_buffer_append(buffer: Buffer):
    events_cnt = 30
    for i in range(events_cnt):
        await buffer.append(i)

    await buffer.empty(1.0)
    assert len(buffer.buff) == events_cnt


@pytest.mark.asyncio()
async def test_buffer_stop(buffer: Buffer):
    events_cnt = 30
    for i in range(events_cnt):
        await buffer.append(i)

    await buffer.stop()
    assert len(buffer.buff) == events_cnt
