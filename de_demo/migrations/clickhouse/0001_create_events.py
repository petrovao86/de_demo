from infi.clickhouse_orm import migrations

from de_demo.apps.events.warehouse.models import (
    Events, EventsBuffer
)

operations = [
    migrations.CreateTable(Events),
    migrations.CreateTable(EventsBuffer),
]
