# Lakeflow ETL Pipeline — bronze layer
#
# Unity Catalog: do not hardcode destination catalog.schema in code; the ETL Pipeline UI selects
# the target. Use Unity Catalog as the pipeline storage format (not legacy Hive-only metastore).
#
# Add this file with lakeflow_silver_flights.py and lakeflow_gold_flights.py as pipeline libraries.
# Source paths use abfss (external to the UC target).
#
# Batch read from an existing Delta table. For raw files, optionally add
# lakeflow_bronze_cloudfiles_ingestion.py or land files upstream into Delta and set bronze.source.delta.path.

from __future__ import annotations

from pyspark import pipelines as dp
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

CONF_SOURCE_DELTA = "bronze.source.delta.path"
_DEFAULT_SOURCE_DELTA = (
    "abfss://atininput@sadbtrng19032026.dfs.core.windows.net/data/day5/delta/flight_summary_basic"
)


def _source_delta_path() -> str:
    return spark.conf.get(CONF_SOURCE_DELTA, _DEFAULT_SOURCE_DELTA)  # noqa: F821


@dp.materialized_view(
    comment="Bronze: batch read of upstream Delta (raw-aligned landing for medallion).",
    table_properties={"quality": "bronze", "layer": "ingest"},
)
@dp.expect("count_not_null", "count IS NOT NULL")
@dp.expect("dest_country_present", "DEST_COUNTRY_NAME IS NOT NULL")
@dp.expect("origin_country_present", "ORIGIN_COUNTRY_NAME IS NOT NULL")
def bronze_flights() -> DataFrame:
    path = _source_delta_path()
    df = spark.read.format("delta").load(path)  # noqa: F821
    return df.withColumn("_ingest_ts", F.current_timestamp())
