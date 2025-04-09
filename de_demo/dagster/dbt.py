from pathlib import Path

from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

import dagster as dg

dbt_project_directory = Path(__file__).absolute().parent.parent / "dbt"
dbt_project = DbtProject(project_dir="./dbt")

dbt_resource = DbtCliResource(project_dir=dbt_project)

dbt_project.prepare_if_dev()


@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


defs = dg.Definitions(
    assets=[dbt_models],
    resources={"dbt": dbt_resource}
)
