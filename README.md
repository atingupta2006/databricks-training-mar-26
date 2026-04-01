# Databricks Training — Course Content

A structured 9-day Databricks training covering Lakehouse architecture, Spark, Medallion design, Unity Catalog, Delta Lake, streaming, and production workflows.

---

## Overview

| Day | Theme | Duration |
|-----|--------|----------|
| 1 | Foundations & Workspace | 5 hours |
| 2 | Spark Fundamentals & Transformations | 5 hours |
| 3 | Medallion Architecture & Ingestion | 5 hours |
| 4 | Unity Catalog Governance | 5 hours |
| 5 | Delta Lake Fundamentals | 4 hours |
| 6 | Delta Advanced Features | 4 hours |
| 7 | Streaming & Delta Live Tables | 4 hours |
| 8 | Workflows & Production Pipelines | 4 hours |
| 9 | Monitoring, SQL & Platform Integration | 4 hours |

---

## Platform documentation (setup)

* **[Unity Catalog–enabled Databricks workspace](docs/unity-catalog-enabled-workspace-setup.md)** — step-by-step guide (Azure-first): metastore, workspace assignment, external locations, grants, verification, troubleshooting.
* **[Documentation index](docs/README.md)** — what lives under `docs/`; notes for course maintainers.
* **[Hands-on folder — ADLS connection (`%run` mount notebook)](hands-on/README.md)** — every lesson notebook calls **`02-Mount-Azure-Data-Lake`** for `spark.conf` + `base_path`.

---

## Day 1 — Foundations & Workspace (5 Hours)

### 1. Introduction to Databricks & Lakehouse (1.5 hours)

**Topics**
- Data platform evolution
  - Traditional Data Warehouses
  - Data Lakes
- Limitations of each architecture
- Lakehouse architecture
- How Databricks implements Lakehouse

**Key Components**
- Workspace
- Compute
- Notebooks
- Delta Lake
- Unity Catalog

**Real-world example**
- Clickstream analytics pipeline
- BI dashboards
- ML integration

---

### 2. Databricks Platform Architecture (1 hour)

**Concepts**
- Account vs Workspace
- Metastore
- Unity Catalog overview
- Platform services

**Compute types**
- All-purpose clusters
- Job clusters
- Serverless compute

**Architecture flow**
- Data ingestion → Processing → Storage → Analytics

---

### 3. Databricks Workspace & UI Tour (1 hour)

**Navigation**
- Data Explorer
- Workspace
- Compute
- Jobs

**Hands-on**
- Create compute cluster
- Explore UI
- Run first notebook

---

### 4. Databricks Notebooks (1.5 hours)

**Notebook fundamentals**
- Cells
- Commands
- Markdown documentation

**Magic commands**
- `%sql`
- `%python`
- `%md`

**Notebook widgets**
- Parameterizing notebooks
- Use cases in workflows

**Hands-on**
- SQL notebook
- PySpark notebook
- Widgets

---

## Day 2 — Spark Fundamentals & Transformations (5 Hours)

### 5. Spark Architecture on Databricks (1 hour)

**Concepts**
- Driver
- Executors
- Cluster execution model

**SparkSession**
- Why Databricks uses Spark

---

### 6. DataFrames & Data Processing (2 hours)

**DataFrame basics**
- Creating DataFrames
- Reading files
- Writing files

**Transformations vs actions**

**Core operations**
- `select`
- `filter`
- `withColumn`
- `drop`

**Hands-on**
- Load CSV dataset
- Transform dataset

---

### 7. Spark Transformations for Data Engineering (2 hours)

**Joins**
- inner
- left
- right

**Aggregations**
- `groupBy`
- `count`
- `sum`
- `avg`

**Handling null values**

**Complex data types**
- struct
- array
- map

**Flattening nested data**
- `explode()`

**Window functions (basic)**

**UDF overview**

---

## Day 3 — Medallion Architecture & Ingestion (5 Hours)

### 8. Medallion Architecture (1.5 hours)

**Layers**
- Bronze
- Silver
- Gold

**Example pipeline**
- Raw data → cleaned data → business aggregates

**Hands-on**
- Bronze → Silver transformation

---

### 9. Data Ingestion Patterns (2 hours)

**Batch ingestion**

**Semi-structured data**

**Schema inference vs schema enforcement**

**File formats**
- CSV
- JSON
- Parquet

**COPY INTO**
```sql
COPY INTO table_name
FROM 'cloud_path'
FILEFORMAT = CSV
```

**Auto Loader (conceptual)**

**COPY INTO vs Auto Loader comparison**

**Hands-on**
- Ingest JSON dataset

---

### 10. Table Creation Techniques (1.5 hours)

**CTAS**
```sql
CREATE TABLE sales_gold
AS SELECT * FROM sales_silver
```

**Cloning**
- Deep Clone
- Shallow Clone

**Use cases**
- backup
- testing
- migration

---

## Day 4 — Unity Catalog Governance (5 Hours)

**Hands-on:** `hands-on/day-04/` — notebooks, `README.md`, `labs.md`. Regenerate notebooks: `python internal/build_day04_notebooks.py`.

### 11. Unity Catalog Fundamentals (2 hours)

**What is Unity Catalog**

**Benefits**
- Central governance
- Lineage
- Auditing

**Three-level namespace**
- `catalog.schema.table`

**Hands-on**
- Create catalog
- Create schema
- Create table

---

### 12. Security & Access Control (1.5 hours)

**Privilege model**
- GRANT
- REVOKE

**Securable objects**
- catalogs
- schemas
- tables
- functions

**Roles**
- admin
- data engineer
- analyst

**Hands-on**
- Grant table access

---

### 13. Storage & External Locations (1 hour)

- Storage credentials
- External locations
- Volumes
- Managed vs external tables

---

### 14. Data Lineage in Unity Catalog (0.5 hour)

- Automatic lineage
- Table dependencies
- Column lineage
- Impact analysis demo

---

## Day 5 — Delta Lake Fundamentals (4 Hours)

**Hands-on:** `hands-on/day-05/` — notebooks, `README.md`, `labs.md`. Regenerate notebooks: `python internal/build_day05_notebooks.py`.

### 15. Delta Lake Architecture (1.5 hours)

**Problems with raw Parquet**

**Delta Lake features**
- ACID transactions
- Transaction log
- Schema enforcement
- Schema evolution

**Hands-on**
- Create Delta table

---

### 16. Delta Table Operations (2.5 hours)

**Core commands**
- CREATE TABLE
- MERGE
- UPDATE
- DELETE

**Managed vs external tables**

**Slowly Changing Dimensions**
- SCD Type 1
- SCD Type 2

**Hands-on**
- MERGE example

---

## Day 6 — Delta Advanced Features (4 Hours)

**Hands-on:** `hands-on/day-06/` — notebooks **01** and **02** for items 17–18 below; details in that folder’s `README.md`.

### 17. Time Travel & Table History (1.5 hours)

- Transaction history
- `DESCRIBE HISTORY`
- Query previous versions
- `VERSION AS OF`
- `TIMESTAMP AS OF`

**Hands-on**
- Query historical data

---

### 18. Delta Performance Optimization (2.5 hours)

- Small files problem
- OPTIMIZE
- ZORDER
- Liquid clustering
- Data skipping

**Hands-on**
- Optimize tables

---

## Day 7 — Streaming & Delta Live Tables (4 Hours)

**Hands-on:** `hands-on/day-07/` — `README.md`, `labs.md`, and notebooks `01-Day7-Structured-Streaming-Delta.ipynb` / `02-Day7-Delta-Live-Tables.ipynb` under `hands-on/day-07/notebooks/` (item 19 then 20).

### 19. Structured Streaming with Delta (2.5 hours)

**Streaming basics**
- Streaming read
- Streaming write
- Checkpointing
- Change Data Feed

**Hands-on**
- Streaming ingestion pipeline

---

### 20. Delta Live Tables (DLT) (1.5 hours)

**What is DLT**

**Declarative pipelines**
- LIVE TABLE
- STREAMING LIVE TABLE

**Expectations**
```sql
CONSTRAINT valid_amount
EXPECT (amount > 0)
ON VIOLATION DROP ROW
```

**Continuous vs Triggered mode**

**Short demo**

---

## Day 8 — Workflows & Production Pipelines (4 Hours)

**Hands-on:** `hands-on/day-08/` — `README.md`, `labs.md`, and notebooks `01-Day8-Databricks-Workflows-Jobs.ipynb` / `02-Day8-Medallion-MultiTask-Workflow.ipynb` under `hands-on/day-08/notebooks/` (item 21 then 22).

### 21. Databricks Workflows (2 hours)

**Jobs concepts**
- tasks
- runs
- clusters

**Hands-on**
- Create job pipeline

---

### 22. Workflow Orchestration (2 hours)

- Multi-task jobs
- Task dependencies
- Error handling
- Scheduling

**Hands-on**
- Bronze → Silver → Gold workflow

---

## Day 9 — Monitoring, SQL & Platform Integration (4 Hours)

**Hands-on:** `hands-on/day-09/` — `README.md`, `labs.md`, and notebooks `01-Day9-Monitoring-Automation-System-Tables.ipynb`, `02-Day9-Databricks-SQL-Warehouses-Dashboards.ipynb`, plus supplement `03-Day9-Extras-Course-Review-and-Extensions.ipynb` when the schedule allows.

### 23. Monitoring & Automation (1.5 hours)

- Job monitoring
- System tables
- Alerts
- Jobs API
- CI/CD overview

---

### 24. Databricks SQL (1.5 hours)

**SQL Warehouses**
- Serverless
- Pro

**Cost optimization**
- Auto-stop

**Dashboards & Alerts**

**Hands-on**
- Create SQL dashboard

---

## Quick Reference

- **Total duration:** ~41 hours over 9 days  
- **Focus areas:** Lakehouse, Spark, Medallion, Unity Catalog, Delta Lake, Streaming, Workflows, SQL  
- **Hands-on:** Notebooks, clusters, ingestion, MERGE, optimization, streaming, jobs, dashboards  

---

*Course content for Databricks training — Vinsys.*
