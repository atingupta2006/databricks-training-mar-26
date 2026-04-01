# Day 07 — Streaming & Delta Live Tables — Labs

Follows items **19** and **20** in the course outline. Part A before Part B.

**Notebooks:** [01-Day7-Structured-Streaming-Delta.ipynb](notebooks/01-Day7-Structured-Streaming-Delta.ipynb) (Part A), [02-Day7-Delta-Live-Tables.ipynb](notebooks/02-Day7-Delta-Live-Tables.ipynb) (Part B).

---

## Part A — Structured streaming (item 19)

### Objective

Work through streaming read and write, checkpointing, Change Data Feed, and a small end-to-end streaming pipeline.

### Tasks

1. **Streaming read** — Run notebook `01` (`readStream` from the rate source). Optionally repeat with **Auto Loader** (`readStream.format("cloudFiles")`) on a folder under your ADLS base path if the instructor provides landing files (CSV/JSON/Parquet). Use a **separate** checkpoint path per source.

2. **Streaming write** — `writeStream` to Delta (`append`).

3. **Checkpointing** — Set `checkpointLocation` on durable storage (`day07-{STUDENT_ID}/checkpoints/...`). In `01`, the same checkpoint is reused across micro-batches (restart semantics).

4. **Stop and restart** — After Lab 1, confirm the table and history. After enabling CDF (Lab 3), run further micro-batches (Lab 4). Optional: delete only the **checkpoint** folder (not the Delta table) and discuss what happens on next start (at your own risk in shared environments).

5. **Change Data Feed** — Enable on the sink, then **append / delete / update** to create multiple versions; read with `readChangeFeed` (and `table_changes` if available).

### Optional extension (file ingestion)

If you have a directory of files on ABFS, a minimal Auto Loader pattern is:

```python
# Example only: set INBOX and CP to your paths; instructor must provide files.
# INBOX = f"{BASE_PATH}landing/your-inbox/"
# CP = f"{DAY7_PREFIX}/checkpoints/autoloader_demo"
# df = spark.readStream.format("cloudFiles").option("cloudFiles.format", "csv").option("header", "true").load(INBOX)
# df.writeStream.format("delta").option("checkpointLocation", CP).trigger(availableNow=True).start(f"{DAY7_PREFIX}/autoloader_sink")
```

---

## Part B — Delta Live Tables (item 20)

### Objective

Run a DLT-style pipeline: declarative layers, live tables, expectations, and triggered vs continuous runs.

### Tasks

1. **Pipeline** — Create a DLT pipeline from notebook `02` (target schema per instructor).

2. **LIVE tables** — Bronze (read Delta path), silver (view), gold (materialized). In SQL pipelines you would declare `CREATE LIVE TABLE` / `CREATE STREAMING LIVE TABLE`; in Python, `@dlt.table` with batch `spark.read` or `readStream` maps to those concepts (see notebook markdown).

3. **Expectations** — Notebook `02` uses `@dlt.expect_or_drop` to mirror `ON VIOLATION DROP ROW` from the course SQL example.

4. **Triggered vs continuous** — In the pipeline UI: run **Triggered** for class demos (full refresh / scheduled); try **Continuous** only if your workspace policy allows and you need near real-time (higher compute use).

5. **Short demo** — Show pipeline run, lineage/expectations in the DLT UI.

---

## Optional

Watermarking, arbitrary aggregations in streaming, or extra Tata/Apache Spark lab notebooks from the local `databricks` reference bundle — only if time allows and still on-topic for items 19–20.

---

## References

- [Structured Streaming + Delta](https://docs.databricks.com/structured-streaming/delta-lake.html)
- [Change Data Feed](https://docs.databricks.com/delta/delta-change-data-feed.html)
- [Delta Live Tables](https://docs.databricks.com/delta-live-tables/index.html)
- [DLT expectations](https://docs.databricks.com/delta-live-tables/expectations.html)
