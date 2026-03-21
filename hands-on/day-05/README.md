# Day 05 — Delta Lake Fundamentals

## Duration

About 4 hours in class; notebook work can run longer if you complete every optional section.

## Notebooks (`notebooks/`)

Run in this order:

1. `02-Mount-Azure-Data-Lake.ipynb` — OAuth and `base_path` (ABFS), same as other days.
2. `01-Day5-Delta-Lake-Architecture-and-Basics.ipynb` — Parquet vs Delta, loads from CSV/JSON, schema and partition patterns, SQL on `delta.` paths, quality checks, practice cells and challenges.
3. `03-Day5-Delta-History-Optimize-Advanced.ipynb` — History, time travel, OPTIMIZE/ZORDER, optional CDF and CHECK demos, drills, short quiz.
4. `04-Day5-Delta-DML-MERGE-SCD.ipynb` — MERGE, UPDATE, DELETE, staging pattern, SCD discussion, optional SQL MERGE and challenges.

Notebooks 01, 03, and 04 begin with `%run ./02-Mount-Azure-Data-Lake`.

ADLS access for the course: `hands-on/README.md`.

Writes use `BASE_PATH + "/day5/..."`. You need `2010-summary.csv` and `json/2015-summary.json` on the storage account (same layout as Day 1). The topics align with common Delta training labs (reads/writes, versioning, schema evolution, optimizations), using ABFS and `_metadata.file_path` where UC discourages `input_file_name()`.

Hands-on steps: `labs.md`.

Maintainers rebuilding from source:

```bash
python internal/build_day05_notebooks.py
```

---

# 15. Delta Lake Architecture (theory + practice)

## 15.1 Why not “just Parquet”?

* Partial writes and lack of a single **transaction log** make concurrent reads/writes risky.
* **Schema drift** across files is hard to govern.

## 15.2 Delta Lake building blocks

* **`_delta_log`** — ordered commits, checkpoints.
* **ACID** table semantics at the storage path.
* **Schema enforcement** and **`mergeSchema` / `overwriteSchema`**.
* **Time travel**, **DML**, **OPTIMIZE** (Databricks), **CDF** (later / Day 6).

---

# 16. Delta table operations

## 16.1 Reads and writes

* **DataFrame:** `spark.read.format("delta").load(path)` / `.write.format("delta")...save(path)`
* **SQL:** `SELECT ... FROM delta.\`abfss://.../path\``

## 16.2 DML patterns

* **`MERGE`** — upsert / sync from staging.
* **`UPDATE` / `DELETE`** — predicates; **`DeltaTable`** API avoids some SQL dialect differences.

## 16.3 SCD

* **Type 1** — overwrite current attributes (no history).
* **Type 2** — preserve history (`effective_*`, `is_current`); production merges close old rows in one transaction.

---

## Databricks workspace — suggested folder

* **`day05-uXX`** — copy **`02-Mount-...`** plus **`01-Day5-...`**, **`03-Day5-...`**, **`04-Day5-...`** into the same folder.
