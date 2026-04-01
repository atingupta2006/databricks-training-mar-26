# Optional Lakeflow library — bronze from Auto Loader (CSV via cloudFiles)
#
# Attach only with a CSV landing path and usually Continuous pipeline mode.
# Configuration (ETL Pipeline → Settings → Configuration):
#   bronze.cloudfiles.inbox
#   bronze.cloudfiles.schemaLocation
#
# Table name bronze_flights_files avoids clashing with batch bronze_flights.

from __future__ import annotations

from pyspark import pipelines as dp
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import LongType, StringType, StructField, StructType

CONF_INBOX = "bronze.cloudfiles.inbox"
CONF_SCHEMA = "bronze.cloudfiles.schemaLocation"

_DEFAULT_BASE = "abfss://atininput@sadbtrng19032026.dfs.core.windows.net/data"


def _conf(key: str, default: str) -> str:
    return spark.conf.get(key, default)  # noqa: F821


_FLIGHT_CSV_SCHEMA = StructType(
    [
        StructField("DEST_COUNTRY_NAME", StringType(), True),
        StructField("ORIGIN_COUNTRY_NAME", StringType(), True),
        StructField("count", LongType(), True),
    ]
)


@dp.table(
    name="bronze_flights_files",
    comment="Bronze: Auto Loader CSV; _source_path from file metadata.",
    table_properties={"quality": "bronze", "layer": "ingest", "ingestion": "cloudFiles"},
)
@dp.expect("dest_country_present", "DEST_COUNTRY_NAME IS NOT NULL")
def bronze_flights_files() -> DataFrame:
    inbox = _conf(CONF_INBOX, f"{_DEFAULT_BASE}/landing/flight_summary_csv/")
    schema_loc = _conf(CONF_SCHEMA, f"{_DEFAULT_BASE}/day07-lakeflow/schemas/bronze_cloudfiles")
    return (
        spark.readStream.format("cloudFiles")  # noqa: F821
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("cloudFiles.inferColumnTypes", "true")
        .option("cloudFiles.schemaLocation", schema_loc)
        .schema(_FLIGHT_CSV_SCHEMA)
        .load(inbox)
        .withColumn("_ingest_ts", F.current_timestamp())
        .withColumn("_source_path", F.col("_metadata.file_path"))
    )
