#!/bin/bash

dagster job execute -m "de_demo.dagster.definitions" -j update_dbt
dagster-daemon run -m "de_demo.dagster.definitions" --empty-workspace
