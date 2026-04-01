# DLT / Lakeflow — Silver layer (Python pipeline library)
#
# Depends on: dlt_bronze_flights.py in the same pipeline (logical table bronze_flights).
# Silver: conform / cleanse — here filter rows with non-null count (matches course notebook 04).
# Downstream Gold reads this view.

from __future__ import annotations

import dlt
from pyspark.sql import DataFrame
from pyspark.sql.functions import col


@dlt.view()
def silver_flights() -> DataFrame:
    """View over bronze; recomputed when pipeline refreshes dependent tables."""
    return dlt.read("bronze_flights").filter(col("count").isNotNull())
