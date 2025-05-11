"""Ingestion via `dlt`.

The `dlt` pipeline and source secrets can be extracted "auto-magically" from environment variables, as defined below:

    THINKIFIC_API_KEY
    THINKIFIC_SUBDOMAIN
    SOURCES__HUBSPOT__API_KEY
    DESTINATION__SNOWFLAKE__CREDENTIALS__DATABASE
    DESTINATION__SNOWFLAKE__CREDENTIALS__PASSWORD
    DESTINATION__SNOWFLAKE__CREDENTIALS__USERNAME
    DESTINATION__SNOWFLAKE__CREDENTIALS__HOST
    DESTINATION__SNOWFLAKE__CREDENTIALS__WAREHOUSE
    DESTINATION__SNOWFLAKE__CREDENTIALS__ROLE

see: https://dlthub.com/docs/tutorial/grouping-resources#handle-secrets

"""

from dagster import Definitions, load_assets_from_modules
from kautos_data_platform.defs.ingestion.dlt import assets
from kautos_data_platform.defs.ingestion.dlt.resources import dlt_resource, duckdb_resource

defs = Definitions(
    assets=load_assets_from_modules([assets]),
    resources={
        "dlt": dlt_resource,  # Use your defined dlt_resource
        "duckdb": duckdb_resource  # Use your defined duckdb_resource
    },
)
