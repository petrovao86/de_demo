from dbt.cli.main import dbtRunner


class DbtCli:
    """Запуск dbt."""
    def __call__(self, *args, project_dir: str = "dbt", **kwargs):
        dbt = dbtRunner()
        kwargs["project_dir"] = project_dir
        result = dbt.invoke(list(args), **kwargs)

        if not result.success:
            raise result.exception
