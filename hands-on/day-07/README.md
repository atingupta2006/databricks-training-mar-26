# Day 07 — Streaming & Delta Live Tables

## Duration

4 hours (items 19 and 20 in the course `README.md`).

## Outline

| Item | Subject | Time (guide) | Focus |
|------|---------|--------------|--------|
| 19 | Structured Streaming with Delta | ~2.5 h | Read/write streams, checkpoints, change data feed |
| 20 | Delta Live Tables | ~1.5 h | Pipelines, `LIVE` / `STREAMING LIVE` tables, expectations, triggered vs continuous |

Do item 19 before item 20.

## Materials here

- [labs.md](labs.md)
- Notebooks under `hands-on/day-07/notebooks/`:
  - [01-Day7-Structured-Streaming-Delta.ipynb](notebooks/01-Day7-Structured-Streaming-Delta.ipynb) — item 19: rate source → Delta, checkpoint, CDF read
  - [02-Day7-Delta-Live-Tables.ipynb](notebooks/02-Day7-Delta-Live-Tables.ipynb) — item 20: DLT pipeline (bronze/silver/gold + expectation)

## Prerequisites

- Earlier days through Delta on ABFS (paths as in Days 4–6).
- Cluster can write checkpoint locations you choose.

## Outcomes

- One streaming write to Delta with a checkpoint path.
- Either a batch change-data read or a small DLT pipeline with an expectation (match what your notebooks do).
