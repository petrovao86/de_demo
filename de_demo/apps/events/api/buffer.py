from infi.clickhouse_orm.database import Database

from de_demo.api.buffer import AsyncBuffer

from .models import EventRequest
from ..warehouse.models import EventsBuffer


class ClickhouseEventsBuffer(AsyncBuffer[EventRequest]):
    def __init__(
        self,
        *,
        db: str = "default",
        addr: str = "http://127.0.0.1:18123",
        user: str = "user",
        passwd: str = "pass",
        buffer_size: int = 100000,
        queue_time: float = 10.0,
        batch_size: int = 10000,
        **kwargs,
    ):
        super().__init__(
            max_buffer_size=buffer_size, max_queue_time=queue_time, max_batch_size=batch_size, **kwargs
        )
        self._db = Database(db, addr, user, passwd)

    async def process_batch(self, batch: list[EventRequest]):
        self._db.insert((EventsBuffer(**event.model_dump(mode="json")) for event in batch))
