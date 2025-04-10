from de_demo.dbt.cli import DbtCli


def test_dbt_cli():
    cli = DbtCli()
    cli("list", project_dir="../../../dbt", logs_path="../../../dbt/logs")
