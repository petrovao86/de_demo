from datetime import datetime, timezone

from pydantic import SecretStr

from .generator.main import Generator, generate_load
from .settings import settings


class GeneratorCli:
    @staticmethod
    def load(addr: str, rps: float = 30):
        """Генератор нагрузки для de_demo.apps.events"""
        generate_load(addr=addr, rps=rps)

    @staticmethod
    def data(
            start_dt: str,
            end_dt: str,
            dau: int = 30,
            user_rps: float = 0.02,
            user_age: int = 13 * 60 * 60,
            visits_per_day: float = 0.85,
            db_addr: str = str(settings.db.addr),
            db_name: str = settings.db.name,
            db_user: str = settings.db.user,
            db_passwd: str | SecretStr = settings.db.passwd,
    ):
        """Генератор демонстрационных данных для de_demo.apps.events

        Вставляет демонстрационные данные в базу от from_dt до to_dt, если указано,
        или по сейчас. Если to_dt не указано, после генерации истории переключается в режим отправки
        событий через API. При отсутствии from_dt, переключается в режим отправки событий через API
        немедленно."""
        from_dt = datetime.fromisoformat(start_dt)
        if from_dt and from_dt.tzinfo is None:
            from_dt = from_dt.astimezone(timezone.utc)

        to_dt = datetime.fromisoformat(end_dt)
        if to_dt and to_dt.tzinfo is None:
            to_dt = to_dt.astimezone(timezone.utc)

        generator = Generator(
            dau=dau,
            user_rps=user_rps,
            user_age=user_age,
            visits_per_day=visits_per_day,
        )
        db_passwd = db_passwd.get_secret_value() if isinstance(db_passwd, SecretStr) else db_passwd

        generator.run(
            from_dt=from_dt,
            to_dt=to_dt,
            db_addr=db_addr,
            db_name=db_name,
            db_user=db_user,
            db_passwd=db_passwd,
        )
