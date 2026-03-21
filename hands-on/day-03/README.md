# Day 03 — Medallion Architecture & Ingestion

## Duration

5 Hours

---

## Notebooks (`notebooks/`)

Run in this order:

1. **`02-Mount-Azure-Data-Lake.ipynb`** — Sets **`spark.conf` OAuth** and **`base_path`** (ABFS). Same notebook as Day 1 / Day 2.
2. **`01-Day3-Medallion-Bronze-Silver-Gold.ipynb`** — Main lab: **Bronze → Silver → Gold** Delta pipeline, validation, SQL over Delta.
3. **`03-Day3-Delta-Lake-Advanced.ipynb`** — **Table history**, **time travel**, **`MERGE`**, **schema evolution**, **`OPTIMIZE`**, **`VACUUM`** discussion.

Tip: Notebook **01** starts with **`%run ./02-Mount-Azure-Data-Lake`** so you can skip opening **02** separately if you prefer.

**Course-wide rule:** See **`hands-on/README.md`** — every ADLS lesson notebook uses **`%run ./02-Mount-Azure-Data-Lake`** (same folder as **`02-Mount-...ipynb`**) so **`spark.conf`** and **`base_path`** are always loaded before reads.

Hands-on steps are also broken down in **`labs.md`**. Instructor pacing: **`instructor-README.md`**.

### Courseware alignment (external reference)

Under **`C:\25-Trainings\2-Confirmed\260317-Vinsys-Databricks\databricks\`**, the Day 3 notebooks mirror patterns from these **top matches** (paths adapted to **ABFS**):

1. **`azure-databricks-tata-technologies-main\Labs\08-Reading Writing to Delta Tables.ipynb`** — Delta I/O, `DeltaTable`, `partitionBy`, MERGE/SQL.
2. **`azure-databricks-tata-technologies-main\Labs\09-DeltaTableVersioning.ipynb`** — history, `versionAsOf` / `timestampAsOf`, delete/restore ideas.
3. **`azure-databricks-tata-technologies-main\Labs\01-Databricks-datalake-spark.ipynb`** — lake-style reads, SQL vs DataFrame, `explain()`.

---

## Databricks Account — Student ID

All students use the **same Databricks account**. Use your **student ID** (u01–u16) as a suffix so resources do not conflict:

* **Folder:** `day03-uXX` (e.g. `day03-u07`)
* **Cluster:** `day03-cluster-uXX` (e.g. `day03-cluster-u07`)

Your instructor will assign your ID. Use it in every folder and cluster name for Day 3.

---

# 8. Medallion Architecture

## 8.1 Why Medallion?

Medallion architecture organizes data into quality layers so pipelines are easier to build, test, and maintain:

* **Bronze:** Raw ingested data (minimal transformation, append-only where possible).
* **Silver:** Cleaned, validated, deduplicated, standardized data.
* **Gold:** Business-ready, curated datasets for BI/analytics/ML.

This separation improves:

* Traceability (you can go back to raw records).
* Reprocessing and debugging.
* Team collaboration (clear ownership per layer).

---

## 8.2 Typical Folder/Table Layout

Use a consistent structure under your Day 3 data root:

```text
data/
  day03/
    bronze/
      flights_raw/
    silver/
      flights_clean/
    gold/
      flights_kpis/
```

For Delta tables, each folder is usually the physical storage location for one logical table.

---

## 8.3 Batch vs Incremental Ingestion

### Batch

* Read all available files at once.
* Good for initial loads and small datasets.

### Incremental (micro-batch / streaming style)

* Process only new files/records since last run.
* Better for scale and near-real-time needs.
* Requires checkpointing and idempotent logic.

---

# 9. Delta Lake Foundations for Medallion

## 9.1 Why Delta Lake?

Delta provides reliability and performance for Bronze/Silver/Gold layers:

* **ACID transactions**
* **Schema enforcement and evolution**
* **Time travel**
* **MERGE/UPSERT**
* Better metadata handling than plain Parquet-only layouts

---

## 9.2 Core Delta Operations

### Create / Write

```python
df.write.format("delta").mode("overwrite").save(path)
```

### Read

```python
df = spark.read.format("delta").load(path)
```

### Append

```python
df.write.format("delta").mode("append").save(path)
```

### Merge (upsert pattern)

```python
from delta.tables import DeltaTable

target = DeltaTable.forPath(spark, silver_path)
(target.alias("t")
 .merge(source_df.alias("s"), "t.id = s.id")
 .whenMatchedUpdateAll()
 .whenNotMatchedInsertAll()
 .execute())
```

---

# 10. Bronze → Silver → Gold Pipeline Pattern

## 10.1 Bronze (Ingest Raw)

Goals:

* Keep source columns as-is (plus ingestion metadata).
* Preserve data for audit/replay.

Recommended metadata columns:

* `ingestion_ts`
* `source_file`
* `load_date`

Example:

```python
from pyspark.sql.functions import current_timestamp, input_file_name

bronze_df = (spark.read.format("csv")
             .option("header", True)
             .option("inferSchema", True)
             .load(input_path)
             .withColumn("ingestion_ts", current_timestamp())
             .withColumn("source_file", input_file_name()))

bronze_df.write.format("delta").mode("append").save(bronze_path)
```

---

## 10.2 Silver (Clean and Conform)

Typical Silver tasks:

* Cast data types correctly.
* Remove duplicates.
* Handle null/invalid rows.
* Apply business-friendly column names.

Example:

```python
from pyspark.sql.functions import col

silver_df = (spark.read.format("delta").load(bronze_path)
             .dropDuplicates(["flight_id"])
             .filter(col("count").isNotNull())
             .withColumn("count", col("count").cast("long")))

silver_df.write.format("delta").mode("overwrite").save(silver_path)
```

---

## 10.3 Gold (Business Aggregates)

Gold focuses on consumption-ready outputs:

* KPIs
* Aggregated facts by date/region/category
* Dimensional marts for BI tools

Example:

```python
from pyspark.sql.functions import sum as spark_sum

gold_df = (spark.read.format("delta").load(silver_path)
           .groupBy("DEST_COUNTRY_NAME")
           .agg(spark_sum("count").alias("total_flights")))

gold_df.write.format("delta").mode("overwrite").save(gold_path)
```

---

# 11. Data Quality Essentials in Day 3

Apply checks before promoting data to Silver/Gold:

* **Not-null checks** on mandatory columns.
* **Uniqueness checks** on business keys.
* **Range/domain checks** (e.g. count >= 0).
* **Schema checks** for expected columns/types.

Common strategy:

* Keep valid records in Silver.
* Route invalid records to a quarantine/error table for review.

---

# 12. Orchestration and Operational Best Practices

## 12.1 Idempotency

Pipelines should be safe to rerun:

* Avoid duplicate inserts on retries.
* Prefer merge/upsert or dedupe keys.

## 12.2 Checkpointing (for incremental loads)

* Use checkpoint locations in ABFS.
* Keep one stable checkpoint path per streaming query.

## 12.3 Monitoring

Track:

* Input row count
* Output row count
* Reject/error count
* Pipeline runtime

---

# 13. Day 3 Practical Scope

## 13.1 What You Will Build

By end of Day 3, you should complete:

1. **Bronze ingestion** from ABFS input files into Delta.
2. **Silver transformation** with schema cleanup and quality checks.
3. **Gold aggregation** for reporting-friendly analytics.
4. Validation queries for row counts and quality.

---

## 13.2 Suggested Validation Checklist

* Bronze has raw + metadata columns.
* Silver has cleaned schema and no duplicate keys.
* Gold aggregates match expected totals.
* Re-running the pipeline does not create duplicates.

---

# 14. Azure Data Lake Access Pattern (ABFS only)

Day 3 follows the same storage approach as Day 1 and Day 2:

* Use **ABFS (`abfss://...`)** paths.
* Configure OAuth via **`spark.conf`** (Service Principal).
* Use `%run ./02-Mount-Azure-Data-Lake` style helper notebook if provided.
* **Do not use `dbutils.fs.mount`** or File Store for these labs.

---

# End of Day 03
