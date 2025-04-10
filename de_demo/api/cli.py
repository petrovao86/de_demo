from .main import app
from .settings import settings


class ApiCli:
    """Запуск API."""
    def __call__(
            self,
            host: str = settings.host,
            port: int = settings.port,
            log_level: str = settings.log_level,
            access_log: bool = settings.access_log,
            workers: int = settings.workers,
            enable_metrics: bool = settings.enable_metrics
    ):
        """Запуск API.

        Args:
            host (str): IP адрес сервера.
            port (PositiveInt): Порт сервера.
            log_level (str): Уровень логирования: critical/error/warning/info/debug/trace.
            access_log (bool): Включить/выключить логирование обращений к APIs.
            workers (PositiveInt): Колличество процессов.
        """
        try:
            import uvicorn
            from prometheus_fastapi_instrumentator import Instrumentator
        except ImportError:
            raise ValueError("api extras not installed, try install de-demo[api]")

        if enable_metrics:
            Instrumentator().instrument(
                app, metric_namespace="de_demo", metric_subsystem="api"
            ).expose(app, include_in_schema=False)

        uvicorn.run(
            'de_demo.api.main:app',
            host=host,
            port=port,
            log_level=log_level,
            access_log=access_log,
            workers=workers
        )
