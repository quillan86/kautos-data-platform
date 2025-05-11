from dagster_dlt import DagsterDltResource
from dagster_duckdb import DuckDBResource
import dagster as dg

dlt_resource = DagsterDltResource(
    destination="duckdb",  # Tells Dagster to use the "duckdb" resource defined below
    pipeline_name="kautos",
    dataset_name="worldanvil",
    progress="log"
)

duckdb_resource = DuckDBResource(database=dg.EnvVar("DUCKDB__KAUTOS__DATABASE"))
