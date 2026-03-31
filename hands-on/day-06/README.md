# Day 06 — Delta Advanced Features

## Duration

4 hours (matches items 17 and 18 in the course `README.md`).

## What to run

| Item | Subject | Time (guide) | Notebook |
|------|---------|--------------|----------|
| 17 | Time travel and table history | ~1.5 h | [01-Day6-Time-Travel-and-Table-History.ipynb](notebooks/01-Day6-Time-Travel-and-Table-History.ipynb) |
| 18 | Delta performance: small files, OPTIMIZE, ZORDER, liquid clustering, data skipping | ~2.5 h | [02-Day6-Delta-Performance-Optimization.ipynb](notebooks/02-Day6-Delta-Performance-Optimization.ipynb) |

Items 17 and 18 are covered with notebooks **01** and **02**.

## Other files

- [03-Day6-Optional-5min-Teaser.ipynb](notebooks/03-Day6-Optional-5min-Teaser.ipynb) — short Spark notes (AQE, broadcast hint). Not part of items 17–18.
- [notebooks/_archive/](notebooks/_archive/) — older notebooks (storage cost, AQE labs, joins, etc.). See [_archive/README.md](notebooks/_archive/README.md).

Notebook **01** includes a batch MERGE exercise (same family of operations as Day 5). Streaming and change data feed are on Day 7 (item 19).

## Prerequisites

- Day 5 notebook 01 completed so `P_BASIC` exists at `.../day5/delta/flight_summary_basic`.
- ABFS access as in earlier days (paths are set in the first code cell: `BASE_PATH`, `DAY6_PREFIX`).

## Checklist

- Time travel and history behave as expected on the lab path.
- OPTIMIZE (with ZORDER if you use it) completes.

Step-by-step notes: [labs.md](labs.md).

## Before you teach

Run **01** and **02** once on the workspace and cluster you will use in class, with your real `STUDENT_ID` and storage account.
