from datetime import datetime, timezone

from infi.clickhouse_orm.fields import DateTimeField, StringField
from infi.clickhouse_orm.funcs import F
from pytz import UTC

from de_demo.warehouse.clickhouse.fields import MapField


def test_map_get_sql(ch_db):
    f = MapField(StringField(), StringField())
    assert f.get_sql(with_default_expression=False,
                     db=ch_db) == "Map(String, String)"
    assert f.get_sql(with_default_expression=True,
                     db=ch_db) == "Map(String, String) DEFAULT map()"

    f = MapField(StringField(), StringField(default="1"))

    assert f.get_sql(
        with_default_expression=False, db=ch_db
    ) == "Map(String, String)"
    assert f.get_sql(
        with_default_expression=True, db=ch_db
    ) == "Map(String, String) DEFAULT map()"

    f = MapField(StringField(), DateTimeField(default=F.now()))

    assert f.get_sql(
        with_default_expression=False, db=ch_db
    ) == "Map(String, DateTime)"
    assert f.get_sql(
        with_default_expression=True, db=ch_db
    ) == "Map(String, DateTime) DEFAULT map()"


def test_map_to_db_string():
    f = MapField(StringField(), StringField())
    assert f.to_db_string({"test_key": "test_val"}, quote=True) == "{'test_key': 'test_val'}"
    assert f.to_db_string({"test_key": "test_val"}, quote=False) == "{'test_key': 'test_val'}"
    assert f.to_db_string({"test_key": 1}, quote=True) == "{'test_key': 1}"
    assert f.to_db_string({"test_key": 1}, quote=False) == "{'test_key': 1}"

    f = MapField(StringField(), DateTimeField())
    assert f.to_db_string(
        {"test_key": datetime(2000, 1, 1)}, quote=True
    ) == "{'test_key': '0946684800'}"
    assert f.to_db_string(
        {"test_key": datetime(2000, 1, 1)}, quote=False
    ) == "{'test_key': '0946684800'}"


def test_map_to_python():
    f = MapField(StringField(), StringField())
    assert f.to_python({"test_key": "test_val"}, timezone_in_use=UTC) == {"test_key": "test_val"}
    assert f.to_python("{'test_key': 'test_val'}", timezone_in_use=UTC) == {"test_key": "test_val"}
    assert f.to_python(None, timezone_in_use=UTC) == {}

    f = MapField(StringField(), DateTimeField())
    assert f.to_python(
        {"test_key": "2000-01-01"}, timezone_in_use=UTC
    ) == {"test_key": datetime(2000, 1, 1, tzinfo=timezone.utc)}
    assert f.to_python(
        "{'test_key': '2000-01-01'}", timezone_in_use=UTC
    ) == {"test_key": datetime(2000, 1, 1, tzinfo=timezone.utc)}
    assert f.to_python(None, timezone_in_use=UTC) == {}
