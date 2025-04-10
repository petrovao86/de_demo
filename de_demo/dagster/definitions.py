from .dbt import add_dbt_defs

defs = None

try:
    from dagster import Definitions

    def get_defs() -> list[Definitions]:
        result = []
        add_dbt_defs(result)
        return result

    defs = Definitions.merge(*get_defs())
except ImportError:
    pass
