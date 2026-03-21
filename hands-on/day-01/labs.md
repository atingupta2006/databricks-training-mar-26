# Day 01 — Labs (labs.md)

## Theme

Foundations & Workspace

## Duration

5 Hours

---

## Databricks Account — Use Your Student ID

All students use the **same Databricks account**. To avoid conflicts, use your **student ID** as a suffix in folder and cluster names.

* **Student IDs:** `u01` through `u16` (your instructor will assign your ID).
* **Folder name:** `day01-uXX` (e.g. if your ID is u03, use `day01-u03`).
* **Cluster name:** `day01-cluster-uXX` (e.g. `day01-cluster-u03`).

Use your assigned ID everywhere you create a folder or cluster in this course.

---

# Lab 1 — Workspace Setup and Cluster Creation

## Objective

Create a cluster, explore the workspace UI, and attach a notebook.

---

## Task 1 — Navigate Workspace

1. Log in to Databricks workspace.
2. Observe left sidebar:

   * Workspace
   * Recents
   * Compute
   * Jobs
   * Data

---

## Task 2 — Create Folder

1. Go to **Workspace**
2. Navigate to your user folder
3. Create new folder:

   * Name: `day01-uXX` (replace **XX** with your student ID, e.g. `day01-u05` for student u05)

---

## Task 3 — Create Notebook

1. Open your `day01-uXX` folder
2. Click **Create → Notebook**
3. Configure:

   * Name: `01-Day1-Foundations-PySpark-SQL-Widgets`
   * Default Language: Python
4. Click **Create**

---

## Task 4 — Create Cluster

1. Go to **Compute → Create Cluster**
2. Configure:

   * Cluster Name: `day01-cluster-uXX` (replace **XX** with your student ID, e.g. `day01-cluster-u05`)
   * Runtime: Latest LTS (Spark + Delta)
   * Worker Type: Small/Standard
   * Number of Workers: 1–2
3. Click **Create Cluster**
4. Wait until status shows **Running**

---

## Task 5 — Attach Notebook to Cluster

1. Open your notebook
2. Select **your** cluster (`day01-cluster-uXX`) from the dropdown (top-right)
3. Ensure cluster status shows attached

---

## Task 6 — Load data from ADLS (ABFS — same pattern as Days 2–3)

1. Get the course data from the repo folder **`data/flight-data/`**. It contains:
   * `csv/2010-summary.csv` and `csv/2015-summary.csv`
   * `json/2015-summary.json`
2. Upload into **ADLS Gen2** under your container’s **`data/`** folder so the layout matches the notebooks:
   * **`data/2010-summary.csv`** (copy from `csv/2010-summary.csv` if you use the Day 1–3 standard layout)
   * **`data/json/2015-summary.json`**
3. Open **`02-Mount-Azure-Data-Lake.ipynb`**, set **Service Principal** / storage details, run all cells (or use **`%run ./02-Mount-Azure-Data-Lake`** from the main notebook).

---

## Task 7 — Run First Commands in the Notebook

1. Open the notebook **01-Day1-Foundations-PySpark-SQL-Widgets** (or import it from the course `notebooks/` folder).
2. Attach it to your cluster `day01-cluster-uXX`.
3. Run **`%run ./02-Mount-Azure-Data-Lake`**, then the **paths** cell (`BASE_PATH`, `OUTPUT_PATH`, `flight_data_json`). Run the cell that **creates Parquet from CSV** (under `BASE_PATH`) when you reach that section.
4. Run the **DataFrames** section cells (schema, JSON/Parquet/CSV read/write, infer schema, explicit schema).

---

## Success Criteria

* Cluster is in **Running** state
* Notebook is attached to cluster
* Intro and data path cells run
* DataFrames section runs (load data, printSchema, file formats)

---

# Lab 2 — Spark SQL (same notebook)

## Objective

Work through the **Spark SQL** section of **01-Day1-Foundations-PySpark-SQL-Widgets**: temp views, global temp views, managed tables, Catalyst optimizer (caching), and SQL queries.

---

## Tasks

1. In the same notebook, continue to the **Spark SQL** section.
2. Run cells that register the DataFrame as a SQL view and run `spark.sql(...)` queries.
3. Create temporary and global temporary views; create a managed table and query it.
4. Run the caching example and the final SQL query on `managed_table`.

---

## Success Criteria

* Temp view and global temp view created and queried
* Managed table created and data inserted
* Caching and SQL query on managed table run successfully

---

# Lab 3 — Widgets (same notebook)

## Objective

Work through the **Widgets** section at the end of **01-Day1-Foundations-PySpark-SQL-Widgets**: create a widget, read its value, use it in PySpark and in SQL.

---

## Tasks

1. In the same notebook, scroll to the **Widgets** section.
2. Create a text widget, read it with `dbutils.widgets.get(...)`.
3. Use the widget value in a filter (PySpark) and in a SQL cell with `${widget_name}`.

---

## Success Criteria

* Widget created and visible in notebook UI
* Value retrieved; data filtered by widget
* SQL cell works with widget parameter

---

# End of Day 01 Labs
