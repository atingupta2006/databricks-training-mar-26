# DLT / Lakeflow — Gold layer (Python pipeline library)
#
# Depends on: silver_flights view from dlt_silver_flights.py.
# Gold: curated materialized table with stricter expectation (drop rows where count < 0).
# Matches course SQL pattern ON VIOLATION DROP ROW via @dlt.expect_or_drop.

from __future__ import annotations

import dlt
from pyspark.sql import DataFrame


@dlt.table(
    comment="Gold: curated flight rows from silver with data quality (drop invalid count).",
    table_properties={"quality": "gold", "layer": "curated"},
)
@dlt.expect_or_drop("count_non_negative", "count >= 0")
def gold_flights() -> DataFrame:
    return dlt.read("silver_flights")
