from dagster import Definitions


def get_defs() -> list[Definitions]:
    from .dbt import defs as dbt_defs
    return [dbt_defs]


defs = Definitions.merge(*get_defs())
