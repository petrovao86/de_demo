class DbtCli:
    """Запуск dbt."""
    def __call__(self, *args, project_dir: str = "dbt", profiles_dir: str = "dbt", **kwargs):
        try:
            from dbt.cli.main import dbtRunner
        except ImportError:
            raise ValueError("dbt extras not installed, try install de-demo[dbt]")
        dbt = dbtRunner()
        kwargs["project_dir"] = project_dir
        kwargs["profiles_dir"] = profiles_dir
        result = dbt.invoke(list(args), **kwargs)

        if not result.success:
            raise result.exception
