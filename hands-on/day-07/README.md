# Day 07 — Streaming & Delta Live Tables

## Duration

4 hours (items **19** and **20** in the course root `README.md`).

## Outline

| Item | Subject | Time (guide) | Focus |
|------|---------|--------------|--------|
| 19 | Structured Streaming with Delta | ~2.5 h | Read/write streams, checkpoints, change data feed |
| 20 | Delta Live Tables | ~1.5 h | Pipelines, `LIVE` / `STREAMING LIVE` tables, expectations, triggered vs continuous |

Do item **19** before item **20**.

## Where syllabus items appear

| Outline item | Where it is covered |
|---------------|---------------------|
| **19** Streaming read | Notebook `01`: `readStream` (rate source); optional Auto Loader pattern in `labs.md` |
| **19** Streaming write | Notebook `01`: `writeStream` → Delta, `outputMode("append")` |
| **19** Checkpointing | Notebook `01`: `checkpointLocation` under `day07-{STUDENT_ID}`; reuse + optional clean-up |
| **19** Change Data Feed | Notebook `01`: `ALTER TABLE` enable CDF, `readChangeFeed`, optional `table_changes` |
| **19** Hands-on: streaming ingestion pipeline | Notebook `01`: end-to-end micro-batch pipeline; file/Auto Loader called out in `labs.md` as optional extension |
| **20** What is DLT / declarative pipelines | Notebook `02` intro + `labs.md` Part B |
| **20** `LIVE TABLE` / `STREAMING LIVE TABLE` | Notebook `02`: Python `@dlt.table` (= batch live table); markdown maps to SQL `LIVE TABLE` / `STREAMING LIVE TABLE` |
| **20** Expectations (`EXPECT` … `ON VIOLATION DROP ROW`) | Notebook `02`: `@dlt.expect_or_drop` (same policy as drop row) + SQL reference in markdown |
| **20** Continuous vs triggered | Notebook `02` + `labs.md` (pipeline UI settings; demo is usually **triggered**) |
| **20** Short demo | Run notebook `02` as a DLT pipeline |

## Materials here

- [labs.md](labs.md)
- Notebooks under `hands-on/day-07/notebooks/`:
  - [01-Day7-Structured-Streaming-Delta.ipynb](notebooks/01-Day7-Structured-Streaming-Delta.ipynb) — item **19**
  - [02-Day7-Delta-Live-Tables.ipynb](notebooks/02-Day7-Delta-Live-Tables.ipynb) — item **20**

## Prerequisites

- Earlier days through Delta on ABFS (paths as in Days 4–6).
- Cluster can write checkpoint locations you choose.
- DLT notebook requires a **Delta Live Tables pipeline** run (not only a classic job).

## Outcomes

Learners should be able to:

- Run a streaming read/write to Delta with a durable checkpoint.
- Explain why CDF needs a `startingVersion` after the first pre-CDF write, and read the change feed.
- Create a small DLT pipeline with bronze → silver → gold and an expectation with a **drop row** policy.
- Choose **triggered** vs **continuous** in the pipeline UI and know when each is appropriate.

## Extra reference material (local)

Optional deeper examples (streaming / DLT concepts) may be copied from the separate bundle:  
`C:\25-Trainings\2-Confirmed\260317-Vinsys-Databricks\databricks`  
(e.g. Apache Spark / Tata / DE associate labs under `**/Labs/*streaming*`, and `**/Working_with_Delta_Live_Tables.md`). Keep anything added on-topic for items 19–20.

## Related days

Workflows and medallion jobs: `hands-on/day-08/`. Monitoring, SQL, and dashboards: `hands-on/day-09/`.
