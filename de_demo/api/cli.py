from .settings import settings


class ApiCli:
    """Запуск API."""
    def __call__(
            self,
            host: str = settings.host,
            port: int = settings.port,
            log_level: str = settings.log_level,
            access_log: bool = settings.access_log,
            enable_metrics: bool = settings.enable_metrics
    ):
        """Запуск API.

        Args:
            host (str): IP адрес сервера.
            port (PositiveInt): Порт сервера.
            log_level (str): Уровень логирования: critical/error/warning/info/debug/trace.
            access_log (bool): Включить/выключить логирование обращений к APIs.
        """
        try:
            import uvicorn
            from fastapi import APIRouter, FastAPI
            from prometheus_fastapi_instrumentator import Instrumentator

            from .routes import add_routes
        except ImportError:
            raise ValueError("api extras not installed, try install de-demo[api]")

        app = FastAPI(title="de-demo")

        api_router = APIRouter()
        add_routes(api_router)

        app.include_router(api_router)

        if enable_metrics:
            Instrumentator().instrument(
                app, metric_namespace="de_demo", metric_subsystem="api"
            ).expose(app, include_in_schema=False)

        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level=log_level,
            access_log=access_log,
        )
