from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import APIRouter, Depends

from de_demo.api.buffer import AsyncBuffer

from .buffer import ClickhouseEventsBuffer
from .models import EventRequest
from ..settings import settings

buff: AsyncBuffer[EventRequest] | None = None


@asynccontextmanager
async def lifespan(_):
    global buff
    buff = ClickhouseEventsBuffer(
        db=settings.db.name,
        addr=settings.db.addr,
        user=settings.db.user,
        passwd=settings.db.passwd.get_secret_value(),
        buffer_size=settings.api_buffer_size,
        queue_time=settings.api_queue_time,
        batch_size=settings.api_batch_size,
    )
    yield
    await buff.stop()


async def get_buffer():
    return buff


router = APIRouter(
    prefix="/events",
    tags=["events"],
    lifespan=lifespan,
)


@router.post("/")
async def create_event(
        event: EventRequest, buffer: Annotated[AsyncBuffer[EventRequest], Depends(get_buffer)]
):
    await buffer.append(event)
