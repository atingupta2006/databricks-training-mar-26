# Day 05 — Labs (labs.md)

## Theme

Delta Lake fundamentals — extended ABFS labs (architecture, history, optimize, MERGE/SCD)

## Duration

4 Hours (minimum); extra sections optional for depth

---

## Lab 0 — Workspace, mount, ADLS paths

### Objective

Confirm **`%run ./02-Mount-Azure-Data-Lake`** and **`BASE_PATH`** for Day 5.

### Tasks

1. Create folder **`day05-uXX`**; attach a cluster with **Delta** enabled.
2. Copy **`02-Mount-Azure-Data-Lake.ipynb`** and all **`01-Day5-...`**, **`03-Day5-...`**, **`04-Day5-...`** notebooks into the same folder.
3. Run mount (or **`%run`** from notebook **01**).
4. Confirm **`BASE_PATH`** prints **`abfss://.../data`**.

### Success criteria

* OAuth works; **`BASE_PATH + "/day5"`** is a valid prefix for writes.

---

## Lab 1 — Notebook 01 (architecture & schema)

### Objective

Build **multiple Delta tables** under **`day5/delta/`** and practice **append**, **`mergeSchema`**, **partitioning**, **`replaceWhere`**, **strict vs evolution**, **SQL reads** on Delta paths, and **EXPLAIN** / partition pruning.

### Tasks

1. Run **Part A–G** (connect, first Delta, append, JSON partition, history/detail).
2. Complete **Part F2** (five **`delta.\\`path\\``** SQL queries on **`P_BASIC`**).
3. Run **Parts H–I2** (read patterns, **`replaceWhere`** on **`P_PART`**).
4. Run **Parts K–P** (analytics, quality, **P1–P12** skill builders — includes scratch **`p9_schema_demo`** and **`EXPLAIN`** cells).
5. Attempt **Part J** challenges **J1–J6**; compare notes with others or review in a follow-up session if stuck.

### Success criteria

* **`P_BASIC`**, **`P_PART`**, **`P_JSON`**, **`P_STRICT`** exist; optional **`p9_schema_demo`** after **P9**.
* **`DESCRIBE HISTORY`** shows multiple operations on **`P_BASIC`** and **`P_PART`**.
* You can run at least **one** SQL aggregate via **`delta.\\`P_BASIC\\``** without using a temp view.

---

## Lab 2 — Notebook 03 (history & optimize)

### Objective

Use time travel, compare versions, run OPTIMIZE / ZORDER, optional CDF and CHECK cells, and interpret DESCRIBE DETAIL.

### Tasks

1. Complete Sections 1–2c (history, versionAsOf, timestampAsOf, subtract, DeltaTable.history).
2. Read Sections 3–7 (RESTORE, VACUUM, CDF, constraints — mostly conceptual).
3. Run Section 6b and 7b if your runtime supports them (CDF and CHECK demos use try/except).
4. Run OPTIMIZE on P_PART and P_BASIC; run Section 10d drills as time allows.
5. Complete Section 11 quiz in your own notes or discuss in class.

### Success criteria

* Can explain the difference between version-based and timestamp-based time travel.
* DESCRIBE DETAIL shows numFiles before and after OPTIMIZE (values may change).

---

## Lab 3 — Notebook 04 (MERGE & SCD)

### Objective

Build **`dim_routes`**, run **MERGE** from **Python API** and **SQL**, read **`operationMetrics`**, use **staging**, **`UPDATE`** / **`DELETE`**, and review **SCD2** toy layout.

### Tasks

1. Run **S1–S2** (build dimension, first merge).
2. Run **S2b–S2c** (conditional merge + **staging path** merge).
3. Run **S3–S5b** (verify, update, deletes).
4. Read **S6–S10** (SCD theory, patterns, idempotent loads).
5. Run **S12–S12b** (**SQL MERGE** + metrics from **`DeltaTable.history`**).
6. Complete at least **two** drills from **S11** and **two** items from **S13** challenges.

### Success criteria

* **`P_DIM`** and **`P_STAGE`** exist under **`day5/delta/`**; **`DESCRIBE HISTORY`** on **`P_DIM`** shows **MERGE** / **WRITE** / **UPDATE** as applicable.
* You attempted **S12** (SQL **MERGE**) — if SQL dialect differs, note the **Python** merge equivalent.

---

## Lab 4 — Stretch (optional)

1. Enable **CDF** on a **personal** path under your own `day5` prefix (only if your workspace policy allows) and read **`table_changes`**.
2. Prototype **`CHECK`** constraint SQL on a scratch Delta table.
3. Draft a **Job** notebook that runs **OPTIMIZE** then **VACUUM** (retention per policy) on a **non-shared** path.

---

*Aligned with external labs under `.../databricks/` — all paths use **ABFS** + course **`data/`** layout.*
