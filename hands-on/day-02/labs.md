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

Create Day 2 folder and cluster, and set up the data path using your **mounted Azure Data Lake** (per-student mount from 02-Mount-Azure-Data-Lake).

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

## Task 3 — Set Data Path (mount only)

1. Data for Day 2 comes from your **mounted Azure Data Lake**. Complete **02-Mount-Azure-Data-Lake** first so your per-student mount (e.g. `/mnt/data-u05`) exists. Ensure flight data is available under that mount (e.g. `.../data/flight-data/json/2015-summary.json`).
2. In **01-Day2-Spark-DataFrames-Transformations**, set **student_id** to match 02-Mount-Azure-Data-Lake (e.g. `"u05"`), then run the first **code cell** (BASE_PATH and flightDataJson2015 use your mount path).
3. Work through the notebook in order (Structured APIs, DataFrames, schema, select/filter/withColumn/drop, expressions, and optional RDD/repartition/caching sections).

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
csv_path = BASE_PATH + "/csv/2010-summary.csv"
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

# Lab 6 — Mount Azure Data Lake (Optional — for using DBFS mount going forward)

## Objective

Mount an Azure Data Lake Storage Gen2 container so you can use DBFS paths in later days. **Each student uses a separate mount point** (e.g. `/mnt/data-u05`).

---

## Tasks

1. Open the notebook **02-Mount-Azure-Data-Lake** in `notebooks/`.
2. In **Step 1**, set **student_id** to your assigned ID (e.g. `"u05"`). Your mount point will be `/mnt/data-<student_id>`.
3. Set **adlsAccountName**, **adlsContainerName**; set **applicationId**, **authenticationKey**, **tenandId** (prefer Databricks secrets — see notebook).
4. Run all cells: build endpoint and source, configs, mount to `/mnt/data-<student_id>`, then verify (the notebook lists your mount point).
5. In later notebooks use **your** path, e.g. `dbfs:/mnt/data-u05/your-folder/` (replace `u05` with your student_id).

---

## Success Criteria

* Mount completes without error.
* Verify step shows the contents of your container at your mount point (e.g. `/mnt/data-u05`).
* You can use your mount path in other notebooks (on the same cluster).

---

# End of Day 02 Labs
