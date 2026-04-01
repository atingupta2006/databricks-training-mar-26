# Day 7 — Labs (streaming & Lakeflow ETL)

Work **Part A**, then **Part B**.

**Files:** [01-Day7-Structured-Streaming-Delta.ipynb](notebooks/01-Day7-Structured-Streaming-Delta.ipynb) · [pipelines/](pipelines/) · [pipelines/DEPLOY.md](pipelines/DEPLOY.md)

---

## Part A — Structured streaming (item 19)

### Goal

Practice streaming read and write, checkpoints, change data feed, and a short end-to-end stream.

### Steps

1. Open notebook `01`. Run it top to bottom with your assigned `STUDENT_ID` and paths.
2. Optional: repeat with **Auto Loader** (`cloudFiles`) on a landing folder; use a **dedicated** checkpoint path per source.
3. Confirm checkpoint behavior and CDF steps as described in the notebook.

---

## Part B — Lakeflow ETL Pipeline (item 20)

### Goal

Create one **ETL Pipeline** that loads three Python libraries and writes **bronze_flights**, **silver_flights**, and **gold_flights** into your UC target schema.

### Steps

1. Confirm the Day 5 Delta source used by the default path in `lakeflow_bronze_flights.py`, or set `bronze.source.delta.path` in pipeline configuration (see [DEPLOY.md](pipelines/DEPLOY.md)).
2. Follow [pipelines/DEPLOY.md](pipelines/DEPLOY.md): use **Create → ETL Pipeline**, keep **Lakeflow Pipelines Editor** on, choose **Add existing assets**, then complete **Add existing source code** (set **Pipeline root folder** to `hands-on/day-07/pipelines` under your Repo/Workspace, and add the three `lakeflow_*.py` files under **Source code paths**). Then set **Advanced** edition if available, **Unity Catalog** storage, **Triggered** mode.
3. Start the pipeline; verify lineage and tables under your catalog and schema.
4. Optional: add `lakeflow_bronze_cloudfiles_ingestion.py` and **Continuous** mode when using file landing (same doc).

---

## References

- [Structured streaming with Delta Lake](https://docs.databricks.com/structured-streaming/delta-lake.html)
- [Change Data Feed](https://docs.databricks.com/delta/delta-change-data-feed.html)
- [Databricks documentation — pipelines & Lakeflow](https://docs.databricks.com/en/index.html)
