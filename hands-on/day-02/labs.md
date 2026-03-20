# Day 02 — Labs (labs.md)

## Theme

Spark Fundamentals & Transformations

## Duration

5 Hours

---

## Databricks Account — Use Your Student ID

All students use the **same Databricks account**. To avoid conflicts, use your **student ID** as a suffix in folder and cluster names.

* **Student IDs:** `u01` through `u16` (your instructor will assign your ID).
* **Folder name:** `day02-uXX` (e.g. if your ID is u03, use `day02-u03`).
* **Cluster name:** `day02-cluster-uXX` (e.g. `day02-cluster-u03`).

Use your assigned ID everywhere you create a folder or cluster for Day 2.

---

# Lab 1 — Workspace and Data Path (Day 2)

## Objective

Create Day 2 folder and cluster, and set up the data path using **ADLS Gen2 over ABFS** (OAuth via `spark.conf`, same pattern as Day 1 — notebook **02-Mount-Azure-Data-Lake**).

---

## Task 1 — Create Folder and Notebook

1. In **Workspace**, create folder: `day02-uXX` (replace **XX** with your student ID).
2. Inside it, create a notebook:
   * Name: `01-Day2-Spark-DataFrames-Transformations`
   * Default Language: Python

---

## Task 2 — Create Cluster

1. Go to **Compute → Create Cluster**
2. Configure:
   * Cluster Name: `day02-cluster-uXX`
   * Runtime: Latest LTS (Spark + Delta)
   * Worker Type: Small/Standard
   * Number of Workers: 1–2
3. Create and wait until **Running**. Attach the notebook to this cluster.

---

## Task 3 — Set Data Path (ABFS + `%run`)

1. Upload or sync lab data to your ADLS container under **`data/`** (same layout as Day 1): `data/json/2015-summary.json`, `data/2010-summary.csv`.
2. In **02-Mount-Azure-Data-Lake**, set **adlsAccountName**, **containerName**, **tenant_id**, **client_id**, and **client_secret** (or secrets), then run all cells to configure OAuth and `base_path`.
3. Open **01-Day2-Spark-DataFrames-Transformations**, run **`%run ./02-Mount-Azure-Data-Lake`**, then run the **paths** cell (`BASE_PATH`, `OUTPUT_PATH`, and file variables). Writes go to `.../data/OUTPUT/...` on ADLS.
4. Work through the notebook in order (Structured APIs, DataFrames, schema, select/filter/withColumn/drop, expressions, and optional partitioning/repartition/caching sections).

---

## Success Criteria

* Folder `day02-uXX` and cluster `day02-cluster-uXX` created.
* Mount created (02-Mount-Azure-Data-Lake); notebook attached; **student_id** and first code cell run so BASE_PATH points to your mount.

---

# Lab 2 — DataFrames: Read, Select, Filter, withColumn, Drop

## Objective

Load CSV data and apply core transformations: select, filter, withColumn, drop.

---

## Task 1 — Load CSV

In a new cell:

```python
csv_path = BASE_PATH + "/2010-summary.csv"
df = spark.read.option("header", True).option("inferSchema", True).csv(csv_path)
df.printSchema()
df.show(5)
```

Run the cell.

---

## Task 2 — Select Columns

```python
df.select("DEST_COUNTRY_NAME", "ORIGIN_COUNTRY_NAME", "count").show(5)
```

---

## Task 3 — Filter Rows

```python
from pyspark.sql.functions import col
df.filter(col("count") > 100).show(10)
```

---

## Task 4 — withColumn

```python
df.withColumn("double_count", col("count") * 2).select("DEST_COUNTRY_NAME", "count", "double_count").show(5)
```

---

## Task 5 — Drop Column

```python
df.drop("ORIGIN_COUNTRY_NAME").show(3)
```

---

## Task 6 — Lazy Evaluation (explain)

```python
transformed = df.filter(col("count") > 50).select("DEST_COUNTRY_NAME", "count")
transformed.explain(True)
transformed.show(5)
```

---

## Success Criteria

* CSV loaded; schema and sample rows visible.
* select, filter, withColumn, drop run without error.
* explain() shows logical/physical plan; show() returns expected rows.

---

# Lab 3 — Aggregations and groupBy

## Objective

Use groupBy with count, sum, and avg.

---

## Task 1 — groupBy and count

```python
df.groupBy("DEST_COUNTRY_NAME").count().orderBy(col("count").desc()).show(10)
```

---

## Task 2 — groupBy with sum and avg

```python
from pyspark.sql.functions import sum as spark_sum, avg
df.groupBy("DEST_COUNTRY_NAME").agg(
  spark_sum("count").alias("total_flights"),
  avg("count").alias("avg_per_route")
).orderBy(col("total_flights").desc()).show(10)
```

---

## Success Criteria

* groupBy and aggregations return correct totals and averages.

---

# Lab 4 — Joins

## Objective

Join two DataFrames (inner and left).

---

## Task 1 — Prepare Two DataFrames

Use the same CSV as “left” and create a small “right” table (e.g. a subset or aggregated view):

```python
# Left: full flight data
left_df = df

# Right: top 5 destination countries by total count
from pyspark.sql.functions import sum as spark_sum
right_df = df.groupBy("DEST_COUNTRY_NAME").agg(spark_sum("count").alias("total")).limit(5)
right_df.show()
```

---

## Task 2 — Inner Join

```python
joined = left_df.join(right_df, left_df.DEST_COUNTRY_NAME == right_df.DEST_COUNTRY_NAME, "inner")
joined.select(left_df["*"]).show(10)
```

---

## Task 3 — Left Join

```python
left_joined = left_df.join(right_df, left_df.DEST_COUNTRY_NAME == right_df.DEST_COUNTRY_NAME, "left")
left_joined.count()
```

---

## Success Criteria

* Inner join returns only matching destinations; left join returns all left rows with right columns where they match.

---

# Lab 5 — Handling Nulls (Optional)

## Objective

Use dropna and fillna.

---

## Task 1 — dropna

```python
# If any nulls exist in subset columns, they are dropped
df_clean = df.dropna(subset=["count"])
df_clean.count()
```

---

## Task 2 — fillna

```python
df.fillna(0, subset=["count"]).show(3)
```

---

## Success Criteria

* dropna and fillna run without error; row counts or values are as expected.

---

# Lab 6 — Azure Data Lake via ABFS (OAuth on `spark.conf`)

## Objective

Configure **Spark** to read/write **Azure Data Lake Storage Gen2** using **ABFSS** URIs and **OAuth** (Service Principal) on **`spark.conf`**. **No `dbutils.fs.mount`** — same approach as Day 1.

---

## Tasks

1. Open **02-Mount-Azure-Data-Lake** in `notebooks/`.
2. Set **adlsAccountName**, **containerName**, **tenant_id**, **client_id**, and **client_secret** (use Databricks **secrets** in production).
3. Run all cells: OAuth keys on `spark.conf`, **`base_path`** = `abfss://<container>@<account>.dfs.core.windows.net/data`, optional CSV smoke read.
4. In **01-Day2-Spark-DataFrames-Transformations**, use **`%run ./02-Mount-Azure-Data-Lake`** so every session picks up the same configuration.
5. Use paths like **`BASE_PATH + "/json/2015-summary.json"`** and **`OUTPUT_PATH + "/..."`** for writes under `data/OUTPUT/`.

---

## Success Criteria

* OAuth cells run without error; **`base_path`** prints a valid **abfss://** URI.
* Optional verify read shows rows from **`2010-summary.csv`**.
* Main Day 2 notebook reads JSON/CSV/Parquet from **ABFS** and can write examples to **OUTPUT** on ADLS.

---

# End of Day 02 Labs
