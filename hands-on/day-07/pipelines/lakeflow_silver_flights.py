# Lakeflow ETL Pipeline — silver layer
#
# Unity Catalog outputs come from the pipeline target in the UI.
# Upstream dataset: bronze_flights (defined in lakeflow_bronze_flights.py).

from __future__ import annotations

from pyspark import pipelines as dp
from pyspark.sql import DataFrame
from pyspark.sql.functions import col


@dp.temporary_view()
@dp.expect("count_not_null", "count IS NOT NULL")
def silver_flights() -> DataFrame:
    return spark.read.table("bronze_flights").filter(col("count").isNotNull())  # noqa: F821
