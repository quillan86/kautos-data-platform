from dagster import AssetExecutionContext, SourceAsset
from dagster_dlt import DagsterDltResource, dlt_assets
from dlt import pipeline

from kautos_data_platform.defs.ingestion.dlt.sources.wa import wa_history_source

@dlt_assets(
    dlt_source=wa_history_source("kautos"),
    dlt_pipeline= pipeline(
        pipeline_name="kautos",
        dataset_name="worldanvil",
        destination="duckdb",
        progress="log",
    ),
    name="worldanvil",
    group_name="worldanvil"
)
def worldanvil_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)

worldanvil_source_assets = [
    SourceAsset(key, group_name="worldanvil") for key in worldanvil_assets.dependency_keys
]
