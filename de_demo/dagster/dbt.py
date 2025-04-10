def add_dbt_defs(defs: list):
    try:
        import dagster as dg
        import dagster_dbt as dg_dbt
    except ImportError:
        return

    dbt_project = dg_dbt.DbtProject(project_dir="./dbt", target="prod")

    dbt_resource = dg_dbt.DbtCliResource(project_dir=dbt_project)

    dbt_project.prepare_if_dev()

    @dg_dbt.dbt_assets(manifest=dbt_project.manifest_path)
    def dbt_models(context: dg.AssetExecutionContext, dbt: dg_dbt.DbtCliResource):
        yield from dbt.cli(["build"], context=context).stream()

    schedules = dg_dbt.build_schedule_from_dbt_selection(
        dbt_assets=[dbt_models], # noqa
        job_name="update_dbt",
        cron_schedule="*/5 * * * *",
        default_status=dg.DefaultScheduleStatus.RUNNING,
    )

    defs.append(dg.Definitions(
        assets=[dbt_models], # noqa
        resources={"dbt": dbt_resource},
        schedules=[schedules],
    ))
