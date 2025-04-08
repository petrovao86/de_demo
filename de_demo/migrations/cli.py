from infi.clickhouse_orm.database import Database
from pydantic import AnyHttpUrl, EmailStr, SecretStr

from .metabase.main import migrate
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

    @staticmethod
    def metabase(
            addr: str = str(settings.metabase.addr),
            user: str = settings.metabase.user,
            email: str = settings.metabase.email,
            passwd: str | SecretStr = settings.metabase.passwd,
            locale: str = settings.metabase.locale,
            site_name: str = settings.metabase.site_name,
            engine: str = settings.metabase.db_engine,
            name: str = settings.metabase.db_name,
            db_host: str = settings.metabase.db.addr.host,
            db_port: int = settings.metabase.db.addr.port,
            db_user: str = settings.metabase.db.user,
            db_passwd: str | SecretStr = settings.metabase.db.passwd,
            db_name: str = settings.metabase.db.name


    ):
        passwd = passwd.get_secret_value() if isinstance(passwd, SecretStr) else passwd
        db_passwd = db_passwd.get_secret_value() if isinstance(db_passwd, SecretStr) else db_passwd
        migrate(
            addr=addr, email=email, user_name=user, passwd=passwd, locale=locale, site_name=site_name,
            name=name, engine=engine,
            db_host=db_host, db_port=db_port, db_user=db_user, db_passwd=db_passwd, db_name=db_name
        )


