# Day 03 — Labs (labs.md)

## Theme

Medallion Architecture & Delta Lake on ADLS (ABFS)

## Duration

5 Hours

---

## Databricks Account — Use Your Student ID

* **Student IDs:** `u01` through `u16` (instructor assigns).
* **Folder name:** `day03-uXX` (e.g. `day03-u03`).
* **Cluster name:** `day03-cluster-uXX` (e.g. `day03-cluster-u03`).

---

# Lab 1 — Workspace, cluster, and ABFS setup

## Objective

Create Day 3 resources and confirm **ABFS** access using the shared **mount helper** pattern (same as Day 1 / Day 2).

## Tasks

1. In **Workspace**, create folder **`day03-uXX`**.
2. Create cluster **`day03-cluster-uXX`** (runtime with **Delta Lake** enabled — standard on Databricks).
3. Upload or confirm in ADLS: **`data/2010-summary.csv`** under your container (same layout as earlier days).
4. Open **`02-Mount-Azure-Data-Lake.ipynb`**, set **tenant / client / secret**, run all cells; confirm **`base_path`** prints **`abfss://.../data`**.
5. Optional: open **`01-Day3-Medallion-Bronze-Silver-Gold.ipynb`** and run **`%run ./02-Mount-Azure-Data-Lake`** + paths cell instead of step 4.

## Success criteria

* Folder and cluster exist with correct naming.
* **`base_path`** is valid and CSV read smoke test in mount notebook succeeds (if you run that cell).

---

# Lab 2 — Bronze layer (raw + metadata)

## Objective

Ingest CSV into a **Bronze** Delta table with **audit columns**.

## Tasks

1. In **`01-Day3-Medallion-Bronze-Silver-Gold.ipynb`**, run through the **Bronze** section.
2. Verify **`ingestion_ts`**, **`source_file`**, **`source_system`** exist in the schema.
3. In Azure Storage (or `dbutils.fs.ls` on ABFS if you use utilities), confirm folder **`data/day03/bronze/flights_raw`** contains Delta files (`_delta_log`, part files).

## Success criteria

* Bronze write completes with **`overwrite`** (or your instructor’s chosen mode).
* `show()` displays expected flight columns plus metadata.

---

# Lab 3 — Silver layer (clean + dedupe + route key)

## Objective

Build **Silver** Delta: types, null filters, **`dropDuplicates`**, and **`route_key`** for later **MERGE**.

## Tasks

1. Run the **Silver** cells in notebook **01**.
2. Compare **row counts** Bronze vs Silver (`Silver ≤ Bronze`).
3. Inspect **`route_key`**: stable hash from destination + origin.

## Success criteria

* Silver Delta written to **`data/day03/silver/flights_clean`**.
* No nulls in key columns used for filtering.

---

# Lab 4 — Gold layer (aggregates)

## Objective

Create a **Gold** Delta table: **total flights by destination**.

## Tasks

1. Run the **Gold** section in notebook **01**.
2. Run the **validation** cell (counts + `DESCRIBE DETAIL`).
3. Run the optional **SQL** cell using `createOrReplaceTempView`.

## Success criteria

* Gold table at **`data/day03/gold/flights_by_destination`**.
* Top destinations look reasonable vs Silver.

---

# Lab 5 — Delta history & time travel

## Objective

Inspect **version history** and read a **prior snapshot** of Silver.

## Tasks

1. Open **`03-Day3-Delta-Lake-Advanced.ipynb`**, run **`%run`** + paths (or complete Lab 1–4 first).
2. Run **history** (`DeltaTable.forPath(...).history()`).
3. Run **time travel** read using **`versionAsOf`**.

## Success criteria

* History shows multiple **versions** after prior writes/merges.
* Time-travel query returns data without errors.

---

# Lab 6 — MERGE (upsert) into Silver

## Objective

Apply a **`MERGE`** that **updates** existing **`route_key`** rows (simulated correction feed).

## Tasks

1. Run the **MERGE** section in notebook **03**.
2. Re-run **history** and compare **version** increments.
3. Discuss **idempotency** and when **`MERGE`** beats blind **`append`**.

## Success criteria

* Merge completes; updated rows reflect incremented **`count`** for the filtered slice.

---

# Lab 7 — Schema evolution & OPTIMIZE (optional)

## Objective

* Append to Bronze with a **new column** (`batch_id`) using **`mergeSchema`**.
* Run **`OPTIMIZE`** on Silver (Databricks).

## Tasks

1. Run **schema evolution** cell in notebook **03**; `printSchema()` shows **`batch_id`**.
2. Run **`OPTIMIZE`** cell.
3. Read **`VACUUM`** section only — do **not** run **`VACUUM`** unless instructor approves.

## Success criteria

* Bronze schema includes **`batch_id`**.
* **`OPTIMIZE`** command succeeds on your cluster.

---

# End of Day 03 Labs
