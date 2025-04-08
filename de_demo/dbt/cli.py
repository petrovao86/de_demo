from dbt.cli.main import dbtRunner


class DbtCli:
    """Запуск dbt."""
    def __call__(self, *args, log_path: str = "dbt/logs", target_path: str = "dbt/target", **kwargs):
        dbt = dbtRunner()
        kwargs["log_path"] = log_path
        kwargs["target_path"] = target_path
        result = dbt.invoke(list(args), **kwargs)

        if not result.success:
            raise result.exception
