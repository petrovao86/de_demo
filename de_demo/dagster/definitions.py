from dagster import Definitions

from de_demo.dagster import dbt


defs = Definitions.merge(dbt.defs)
