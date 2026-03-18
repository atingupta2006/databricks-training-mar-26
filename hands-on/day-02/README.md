# Day 02 — Spark Fundamentals & Transformations

## Duration

5 Hours

---

## Databricks Account — Student ID

All students use the **same Databricks account**. Use your **student ID** (u01–u16) as a suffix so resources do not conflict:

* **Folder:** `day02-uXX` (e.g. `day02-u07`)
* **Cluster:** `day02-cluster-uXX` (e.g. `day02-cluster-u07`)

Your instructor will assign your ID. Use it in every folder and cluster name for Day 2.

---

# 5. Spark Architecture on Databricks

## 5.1 Driver and Executors

### Driver

* Single process that runs your application (e.g. notebook).
* Responsibilities:
  * Parses and plans the job (logical and physical plans).
  * Schedules tasks and sends them to executors.
  * Collects results (e.g. for `show()`, `collect()`).
* Runs on the driver node of the cluster.

### Executors

* Worker processes on the cluster.
* Run tasks sent by the driver.
* Store cached data (e.g. `.cache()`) and shuffle data.
* One executor per worker node (typically multiple tasks per executor).

### Cluster Execution Model

```
   Notebook / Job (Driver)
            |
            v
   +------------------+
   |  Driver Node     |
   |  - SparkSession  |
   |  - DAG / Plan    |
   +------------------+
            |
     tasks |  tasks
            v
   +--------+--------+--------+
   | Executor|Executor|Executor|
   | (Worker)|(Worker)|(Worker)|
   +--------+--------+--------+
```

---

## 5.2 SparkSession

* In Databricks, a **SparkSession** (`spark`) is created automatically for each notebook.
* Entry point for reading data, creating DataFrames, and running SQL.
* Why Databricks uses Spark: unified engine for batch, SQL, and (later) streaming; scales out across the cluster.

---

## 5.3 Lazy Evaluation

* **Transformations** (e.g. `select`, `filter`, `withColumn`) are **lazy**: they build a logical plan and do not run until an **action** (e.g. `show()`, `count()`, `write`) is called.
* Benefits: optimizer can combine and optimize the full plan; only necessary work is executed.

---

# 6. DataFrames & Data Processing

## 6.1 DataFrame Basics

* **DataFrame:** Distributed collection of rows with a named schema (like a table).
* **Creating:** From files (CSV, JSON, Parquet), from existing RDDs, or with `spark.createDataFrame()` from local data.

### Reading Files

```python
# CSV
df = spark.read.option("header", True).option("inferSchema", True).csv(path)

# JSON
df = spark.read.json(path)

# Parquet
df = spark.read.parquet(path)
```

### Writing Files

```python
df.write.mode("overwrite").format("parquet").save(path)
df.write.mode("append").format("csv").option("header", True).save(path)
```

---

## 6.2 Transformations vs Actions

| Transformations (lazy) | Actions (eager) |
|------------------------|-----------------|
| `select`, `filter`, `withColumn`, `drop` | `show()`, `count()`, `collect()` |
| `groupBy`, `join`, `orderBy` | `write`, `first()`, `take(n)` |

---

## 6.3 Core Operations

### select

* Pick or derive columns.

```python
df.select("col1", "col2")
df.select(df.col1, (df.col2 + 1).alias("col2_plus_one"))
```

### filter / where

* Keep rows that satisfy a condition.

```python
df.filter(df.amount > 0)
df.where(col("category") == "A")
```

### withColumn

* Add or replace a column.

```python
from pyspark.sql.functions import col
df.withColumn("double_count", col("count") * 2)
```

### drop

* Remove columns.

```python
df.drop("col1").drop("col2")
df.drop("col1", "col2")
```

---

## 6.4 What You Will Do

* Load a CSV dataset from your **mounted Azure Data Lake** (per-student mount, e.g. `/mnt/data-u05`; run 02-Mount-Azure-Data-Lake first).
* Apply `select`, `filter`, `withColumn`, `drop`.
* Inspect schema and run actions (`show()`, `count()`).

Refer to labs and notebook **01-Day2-Spark-DataFrames-Transformations** in `notebooks/`.

---

# 7. Spark Transformations for Data Engineering

## 7.1 Joins

* **Inner join:** Only rows with matching keys in both DataFrames.
* **Left (left_outer):** All rows from left; match from right or null.
* **Right (right_outer):** All rows from right; match from left or null.

```python
df1.join(df2, df1.id == df2.id, "inner")
df1.join(df2, "id", "left")
```

---

## 7.2 Aggregations

* **groupBy:** Group rows by one or more columns, then apply aggregate functions.

```python
from pyspark.sql.functions import count, sum, avg
df.groupBy("category").agg(count("*").alias("cnt"), sum("amount").alias("total"))
```

* **count, sum, avg, min, max** are commonly used.

---

## 7.3 Handling Null Values

* **dropna():** Drop rows with nulls (optionally by subset of columns).
* **fillna():** Replace nulls with a value.
* **coalesce():** Pick first non-null from a list of columns.

```python
df.dropna(subset=["col1"])
df.fillna(0, subset=["amount"])
```

---

## 7.4 Complex Data Types

* **struct:** Nested object (e.g. `struct<name string, age int>`).
* **array:** List of values (e.g. `array<string>`).
* **map:** Key-value pairs (e.g. `map<string, int>`).

Access: `col("struct_col").getField("name")`, `col("arr")[0]`, `col("map_col")["key"]`.

---

## 7.5 Flattening Nested Data — explode()

* **explode(array_col):** One row per element of the array.
* **explode_outer:** Same but keeps rows where the array is null or empty.

```python
from pyspark.sql.functions import explode
df.withColumn("item", explode(col("items")))
```

---

## 7.6 Window Functions (Basic)

* Compute values over a **window** of rows (e.g. partition by key, order by date).
* Examples: `row_number()`, `rank()`, `dense_rank()`, `lag()`, `lead()`, `sum(...).over(window)`.

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number
w = Window.partitionBy("category").orderBy(col("amount").desc())
df.withColumn("rank", row_number().over(w))
```

---

## 7.7 UDF Overview

* **User-Defined Functions:** Custom logic (Python or Scala) applied row-by-row or as aggregate.
* Use Spark built-ins and SQL functions when possible; UDFs are less optimized than native Spark operations.

---

## 7.8 What You Will Do

* Join two DataFrames (e.g. flight data with different keys).
* Use `groupBy` and aggregations.
* Handle nulls; optionally use window functions or explode on nested data.

Refer to labs and notebook **01-Day2-Spark-DataFrames-Transformations** in `notebooks/`.

---

# Mount Azure Data Lake (for use in later days)

Notebook **02-Mount-Azure-Data-Lake** in `notebooks/` is required for Day 2: it mounts Azure Data Lake Storage Gen2 to a **per-student** path (e.g. `/mnt/data-u05`). Day 2 data paths use only this mount; run it before 01-Day2-Spark-DataFrames-Transformations.

* **Prerequisites:** ADLS Gen2 account, container, Service Principal with access to the container.
* **Notebook:** Step-by-step cells for account details, SP credentials (or secrets), mount config, and verify. See Lab 6 in labs.md.

---

# End of Day 02
