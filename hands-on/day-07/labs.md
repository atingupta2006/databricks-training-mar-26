# Day 07 — Streaming & Delta Live Tables — Labs

Follows items 19 and 20 in the course outline. Part A before Part B.

**Notebooks:** [01-Day7-Structured-Streaming-Delta.ipynb](notebooks/01-Day7-Structured-Streaming-Delta.ipynb) (Part A), [02-Day7-Delta-Live-Tables.ipynb](notebooks/02-Day7-Delta-Live-Tables.ipynb) (Part B).

## Prerequisites

- Delta data on ABFS from earlier days.
- Writable path for streaming checkpoints.

---

## Part A — Structured streaming (item 19)

### Objective

Stream to Delta, use checkpoints, and optionally read the change feed.

### Tasks

1. Configure a streaming source (Auto Loader, files, or another source you use in class). Set a checkpoint path on durable storage.

2. Write the stream to Delta (`writeStream` / `toTable` or equivalent).

3. Stop and restart; confirm behavior with your checkpoint settings.

4. If you use it: enable change data feed on the sink and run a batch read of changes (`readChangeFeed` / `table_changes` per your runtime).

---

## Part B — Delta Live Tables (item 20)

### Objective

Define a small pipeline with at least one expectation.

### Tasks

1. Add `LIVE TABLE` or `STREAMING LIVE TABLE` steps (e.g. bronze → silver).

2. Add an expectation with a clear policy (`DROP ROW`, `FAIL`, etc.).

3. Show triggered vs continuous if your setup supports both.

---

## Optional

Extra aggregations or watermark examples only if time allows.

---

## References

- [Structured Streaming + Delta](https://docs.databricks.com/structured-streaming/delta-lake.html)
- [Change Data Feed](https://docs.databricks.com/delta/delta-change-data-feed.html)
- [Delta Live Tables](https://docs.databricks.com/delta-live-tables/index.html)
