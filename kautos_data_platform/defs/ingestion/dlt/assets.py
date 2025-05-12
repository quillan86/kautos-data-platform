import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
from dlt import pipeline

from kautos_data_platform.defs.ingestion.dlt.sources.wa import wa_source

kautos_wa_source = wa_source("kautos")

@dlt_assets(
    dlt_source=kautos_wa_source,
    dlt_pipeline= pipeline(
        pipeline_name="kautos",
        dataset_name="worldanvil",
        destination="duckdb",
        progress="log",
    ),
    name="worldanvil",
    group_name="bronze"
)
def worldanvil_assets(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)


worldanvil_source_assets = [
    dg.SourceAsset(key, group_name="worldanvil") for key in worldanvil_assets.dependency_keys
]
