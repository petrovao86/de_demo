from infi.clickhouse_orm.database import Database
from pydantic import SecretStr

from .settings import settings


class MigrateCli:
    """Миграции баз данных."""

    @staticmethod
    def clickhouse(
            package: str = settings.clickhouse.package,
            addr: str = str(settings.clickhouse.db.addr),
            db: str = settings.clickhouse.db.name,
            user: str = settings.clickhouse.db.user,
            passwd: str | SecretStr = settings.clickhouse.db.passwd,

    ):
        passwd = passwd.get_secret_value() if isinstance(passwd, SecretStr) else passwd
        ch_db = Database(
            db,
            db_url=addr,
            username=user,
            password=passwd
        )
        ch_db.migrate(package)
