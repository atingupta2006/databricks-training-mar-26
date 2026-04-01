# Day 07 — Streaming & Delta Live Tables — Labs

Follows items **19** and **20** in the course outline. Part A before Part B.

**Notebooks:** [01-Day7-Structured-Streaming-Delta.ipynb](notebooks/01-Day7-Structured-Streaming-Delta.ipynb) (Part A). Part B: [02-Day7-DLT-Guide-UI-and-Troubleshooting.ipynb](notebooks/02-Day7-DLT-Guide-UI-and-Troubleshooting.ipynb) (guide), then pipeline libraries [03-Day7-DLT-Bronze-Layer.ipynb](notebooks/03-Day7-DLT-Bronze-Layer.ipynb), [04-Day7-DLT-Silver-Layer.ipynb](notebooks/04-Day7-DLT-Silver-Layer.ipynb), [05-Day7-DLT-Gold-Layer.ipynb](notebooks/05-Day7-DLT-Gold-Layer.ipynb).

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

Run a DLT pipeline split by medallion layer: bronze (`03`), silver (`04`), gold (`05`), with UI setup and troubleshooting documented in `02`.

### Tasks

1. **Read the guide** — On an interactive cluster, open `02-Day7-DLT-Guide-UI-and-Troubleshooting.ipynb`, run the prerequisite cell, and read the UI and troubleshooting sections.

2. **Create one pipeline** — **Workflows → Pipelines → Create pipeline**. Add **three** notebook libraries: `03-Day7-DLT-Bronze-Layer.ipynb`, `04-Day7-DLT-Silver-Layer.ipynb`, `05-Day7-DLT-Gold-Layer.ipynb`. Set **target schema** (catalog + schema) per instructor.

3. **Bronze** — Notebook `03` defines `bronze_flights` (`@dlt.table`) reading Day 5 Delta at `P_BASIC`.

4. **Silver** — Notebook `04` defines `silver_flights` (`@dlt.view`) with `dlt.read("bronze_flights")` and a null filter on `count`.

5. **Gold** — Notebook `05` defines `gold_flights` with `@dlt.expect_or_drop` (drop row policy, same idea as SQL `ON VIOLATION DROP ROW`).

6. **Run and verify** — **Start** the pipeline; open **Lineage**; confirm tables in the target schema; if something fails, use the troubleshooting table in `02` and **Events** in the UI.

7. **Triggered vs continuous** — Keep **Triggered** for this lab; use **Continuous** only if the instructor enables it and you are using streaming sources.

8. **Demo** — Walk through **Full refresh** vs incremental **Refresh** when the instructor asks (full refresh is slower but clears stale materialized state after logic changes).

---

## Optional

Watermarking, arbitrary aggregations in streaming, or extra Tata/Apache Spark lab notebooks from the local `databricks` reference bundle — only if time allows and still on-topic for items 19–20.

---

## References

- [Structured Streaming + Delta](https://docs.databricks.com/structured-streaming/delta-lake.html)
- [Change Data Feed](https://docs.databricks.com/delta/delta-change-data-feed.html)
- [Delta Live Tables](https://docs.databricks.com/delta-live-tables/index.html)
- [DLT expectations](https://docs.databricks.com/delta-live-tables/expectations.html)
