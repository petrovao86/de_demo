import pytest

from infi.clickhouse_orm.database import Database

from tests.utils.environment import TestEnvironment


env = TestEnvironment()


@pytest.fixture(scope='session')
def test_env(monkeysession):
    global env
    try:
        env.up()
        with monkeysession.context() as m:
            m.setenv('CH_DB_URL', env.ch_url)
            yield env
    finally:
        env.down()


@pytest.fixture(scope='function')
def ch_test_db(test_env: TestEnvironment):
    ch_db = Database(
        "default", db_url=test_env.ch_url, username=test_env.ch_user, password=test_env.ch_pass
    )
    try:
        yield ch_db
    finally:
        if ch_db.db_exists:
            ch_db.drop_database()


@pytest.fixture(scope='function')
def ch_migrated_test_db(test_env: TestEnvironment):
    ch_db = Database(
        "default", db_url=test_env.ch_url, username=test_env.ch_user, password=test_env.ch_pass
    )
    ch_db.migrate('de_demo.migrations.clickhouse')
    try:
        yield ch_db
    finally:
        if ch_db.db_exists:
            ch_db.drop_database()
