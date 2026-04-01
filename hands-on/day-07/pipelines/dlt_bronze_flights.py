# DLT / Lakeflow — Bronze layer (Python pipeline library)
#
# Wire-up: add this file to a DLT pipeline together with dlt_silver_flights.py and dlt_gold_flights.py.
# Set Unity Catalog target (catalog + schema) in the pipeline UI — tables materialize as
# <catalog>.<schema>.<table_name>. Use abfss / Unity Catalog volumes; avoid DBFS for production data.
#
# Bronze purpose: land data with minimal change from the source Delta path so Silver can cleanse
# and Gold can apply business rules. DLT gives lineage, refresh semantics, and expectations.

from __future__ import annotations

import dlt
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

# Override via pipeline Configuration: bronze.source.delta.path=<abfss path>
_DEFAULT_SOURCE_DELTA = (
    "abfss://atininput@sadbtrng19032026.dfs.core.windows.net/data/day5/delta/flight_summary_basic"
)


def _source_delta_path() -> str:
    return spark.conf.get("bronze.source.delta.path", _DEFAULT_SOURCE_DELTA)  # noqa: F821


@dlt.table(
    comment="Bronze: batch read of Day 5 flight_summary_basic Delta (raw-aligned landing).",
    table_properties={"quality": "bronze", "layer": "ingest"},
)
@dlt.expect("count_not_null", "count IS NOT NULL")
@dlt.expect("dest_country_present", "DEST_COUNTRY_NAME IS NOT NULL")
@dlt.expect("origin_country_present", "ORIGIN_COUNTRY_NAME IS NOT NULL")
def bronze_flights() -> DataFrame:
    """Ingest from existing Delta; optional audit column only (no business transforms)."""
    path = _source_delta_path()
    df = spark.read.format("delta").load(path)  # noqa: F821
    return df.withColumn("_ingest_ts", F.current_timestamp())


# --- Optional: Auto Loader streaming bronze (attach only when inbox is ready; Continuous pipeline) ---
# @dlt.table(name="bronze_flights_stream", ...)
# def bronze_flights_stream() -> DataFrame:
#     return (
#         spark.readStream.format("cloudFiles")
#         .option("cloudFiles.format", "csv")
#         .option("header", "true")
#         .option("cloudFiles.schemaLocation", "<abfss path to schema dir>")
#         .load("<abfss inbox path>")
#     )
