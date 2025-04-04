from infi.clickhouse_orm.engines import TinyLog
from infi.clickhouse_orm.fields import StringField, Int8Field
from infi.clickhouse_orm.models import Model


from de_demo.warehouse.clickhouse import MapField


def test_map_field(ch_test_db):
    class Test(Model):
        str_str_map = MapField(StringField(), StringField())
        str_int_map = MapField(StringField(), Int8Field())

        engine = TinyLog()

    ch_test_db.create_table(Test)

    ch_test_db.insert([Test(
        str_str_map={"test_str_key": "test_str_value"},
        str_int_map={"test_str_key": 1},
    )])

    for row in Test.objects_in(ch_test_db):
        assert row.str_str_map == {"test_str_key": "test_str_value"}
        assert row.str_int_map == {"test_str_key": 1}
