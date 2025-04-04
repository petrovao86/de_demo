import pytest
import pytz
from infi.clickhouse_orm.database import Database


@pytest.fixture
def ch_db(monkeypatch):
    def patched_is_connection_readonly(*_, **__):
        return False

    def patched_is_existing_database(*_, **__):
        return True

    def patched_get_server_version(*_, **__):
        return 20, 10, 2, 20

    def patched_get_server_timezone(*_, **__):
        return pytz.utc

    with monkeypatch.context() as m:
        m.setattr(Database, '_is_connection_readonly', patched_is_connection_readonly)
        m.setattr(Database, '_is_existing_database', patched_is_existing_database)
        m.setattr(Database, '_get_server_version', patched_get_server_version)
        m.setattr(Database, '_get_server_timezone', patched_get_server_timezone)
        test_db = Database('test_db', db_url="http://test/", autocreate=False)
        yield test_db
