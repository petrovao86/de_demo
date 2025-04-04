from infi.clickhouse_orm.engines import Buffer, MergeTree
from infi.clickhouse_orm.fields import (
    DateTimeField, Float32Field, LowCardinalityField, StringField, UInt64Field
)
from infi.clickhouse_orm.models import BufferModel, Model
from infi.clickhouse_orm.funcs import F

from de_demo.warehouse.clickhouse.fields import MapField


class Events(Model):
    """События сайта.

    Attributes:
         dt (datetime.datetime): Время события. Обязательное.
         name (str): Название события. Обязательное. Например: "click", "view".
         user_id (int): Идентификатор пользователя. Обязательное.
         url (str): Страница на которой произошло событие. Обязательное.
         obj (str): Объект с которым произошло событие. Например: "page", "button", "url".
         obj_id (str): Название объекта. Например: "checkout", "product" для страниц, "add_to_cart" для кнопки.
         product_id (int): Идентификатор товара, если событие связано с товаром.
         amount (float): Cумма события, если событие связано с оплатой или стоимостью чего-либо.
         exp (dict[str, str]): Эксперименты в рамках которых произошло событие {Эксперимент: Вариант}.
    """

    dt = DateTimeField()
    name = LowCardinalityField(StringField())
    user_id = UInt64Field()
    url = StringField()
    obj = LowCardinalityField(StringField())
    obj_id = StringField()
    product_id = UInt64Field()
    amount = Float32Field()
    exp = MapField(StringField(), StringField())

    engine = MergeTree(
        order_by=(dt, name, obj, obj_id),
        partition_key=(F.toYYYYMM(dt, timezone=None),),
    )

    @classmethod
    def table_name(cls):
        return "events"


class EventsBuffer(BufferModel, Events):
    engine = Buffer(Events, num_layers=1,
                    min_time=10, min_rows=10000, min_bytes=10000000,
                    max_time=60, max_rows=1000000, max_bytes=100000000)

    @classmethod
    def table_name(cls):
        return "events_buffer"
