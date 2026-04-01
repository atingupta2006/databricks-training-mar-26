# Lakeflow ETL Pipeline — gold layer
#
# Materialized table; UC destination is set in the ETL Pipeline UI.
#
# Expectation behavior (decorators on table functions):
#   expect — log violations
#   expect_or_drop — remove failing rows from the materialized update
#   expect_or_fail — fail the whole pipeline update if any row violates

from __future__ import annotations

from pyspark import pipelines as dp
from pyspark.sql import DataFrame


@dp.materialized_view(
    comment="Gold: curated table from silver; invalid counts dropped via expect_or_drop.",
    table_properties={"quality": "gold", "layer": "curated"},
)
@dp.expect_or_drop("count_non_negative", "count >= 0")
# Swap to expect_or_fail on the same rule if the pipeline must abort entirely on any bad row.
def gold_flights() -> DataFrame:
    return spark.read.table("silver_flights")  # noqa: F821
