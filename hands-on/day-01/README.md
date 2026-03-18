# Day 01 — Foundations & Workspace

## Duration

5 Hours

---

## Databricks Account — Student ID

All students use the **same Databricks account**. Use your **student ID** (u01–u16) as a suffix so resources do not conflict:

* **Folder:** `day01-uXX` (e.g. `day01-u07`)
* **Cluster:** `day01-cluster-uXX` (e.g. `day01-cluster-u07`)

Your instructor will assign your ID. Use it in every folder and cluster name in this course.

---

# 1. Introduction to Databricks & Lakehouse

## 1.1 Data Platform Evolution

### Traditional Data Warehouse

* Designed for structured data (tables, schemas fixed)
* Optimized for reporting and BI dashboards
* Data must be cleaned before loading (ETL)

#### Architecture

```
        +-------------+
        |  Source DBs |
        +-------------+
               |
               v
        +-------------+
        |   ETL Tool  |
        +-------------+
               |
               v
        +------------------+
        | Data Warehouse   |
        +------------------+
               |
               v
        +-------------+
        | BI Reports  |
        +-------------+
```

#### Limitations

* Expensive storage and compute
* Not flexible for schema changes
* Poor support for:

  * JSON, logs, images, streaming data
* Separate systems required for ML

---

### Data Lake

* Stores raw data in cloud storage
* Supports structured, semi-structured, unstructured data

#### Architecture

```
        +-------------+
        | Data Sources|
        +-------------+
               |
               v
        +------------------+
        |   Data Lake      |
        | (Raw Storage)    |
        +------------------+
               |
        +------+------++
        |             |
        v             v
   +--------+    +----------+
   |  BI    |    |   ML     |
   +--------+    +----------+
```

#### Limitations

* No ACID transactions
* Data inconsistency (duplicate, corrupt data)
* No schema enforcement
* Difficult querying (slow, unreliable)

---

## 1.2 Lakehouse Architecture

### Concept

Lakehouse combines:

* Data Lake → storage layer
* Data Warehouse → reliability + performance

#### Unified Architecture

```
        +---------------------+
        |    Data Sources     |
        +---------------------+
                  |
                  v
        +---------------------+
        |    Data Lake        |
        |  (Cloud Storage)    |
        +---------------------+
                  |
        +---------------------+
        |    Delta Lake       |
        | (ACID + Metadata)   |
        +---------------------+
                  |
        +---------------------+
        |    Processing       |
        |   (Apache Spark)    |
        +---------------------+
                  |
        +---------------------+
        | BI | ML | Streaming |
        +---------------------+
```

---

## 1.3 Why Lakehouse Matters

* Single system for:

  * Data Engineering
  * Analytics
  * Machine Learning
* Eliminates duplication
* Enables real-time + batch processing together

---

## 1.4 Databricks Lakehouse Implementation

### Components Mapping

| Layer       | Technology              |
| ----------- | ----------------------- |
| Storage     | Cloud (ADLS / S3 / GCS) |
| Reliability | Delta Lake              |
| Processing  | Apache Spark            |
| Governance  | Unity Catalog           |
| Interface   | Workspace               |

---

## 1.5 Real-World Example — Clickstream Pipeline

```
 Users → Click Events → Streaming / Batch Ingestion
                     |
                     v
             +------------------+
             |   Raw Storage    |
             +------------------+
                     |
                     v
             +------------------+
             |   Processing     |
             |   (Spark Jobs)   |
             +------------------+
                     |
                     v
             +------------------+
             |   Delta Tables   |
             +------------------+
                     |
          +----------+----------+
          |                     |
          v                     v
     +--------+          +------------+
     |  BI    |          |    ML      |
     +--------+          +------------+
```

---

# 2. Databricks Platform Architecture

## 2.1 Account vs Workspace and Metastore

* **Metastore:** Central catalog for table and schema metadata. In Databricks, Unity Catalog provides the metastore (governance and discovery across workspaces).

```
        +--------------------------+
        |       Account Level      |
        |--------------------------|
        | Users                    |
        | Workspaces               |
        | Billing                  |
        +--------------------------+
                    |
                    v
        +--------------------------+
        |      Workspace Level     |
        |--------------------------|
        | Notebooks                |
        | Clusters                 |
        | Jobs                     |
        +--------------------------+
```

---

## 2.2 Control Plane vs Data Plane

### Concept

* Control Plane → Managed by Databricks
* Data Plane → Runs in your cloud

```
        +------------------------------+
        |        Control Plane         |
        |------------------------------|
        | UI (Workspace)               |
        | Job Scheduler                |
        | Notebook Commands            |
        +------------------------------+
                    |
                    v
        +------------------------------+
        |        Data Plane            |
        |------------------------------|
        | Spark Clusters               |
        | Data Processing              |
        | Cloud Storage Access         |
        +------------------------------+
```

---

## 2.3 Cluster Architecture

```
        +------------------+
        |    Driver Node   |
        |------------------|
        | Task Scheduling  |
        | Execution Plan   |
        +------------------+
           /    |     \
          v     v      v
   +---------+ +---------+ +---------+
   | Worker  | | Worker  | | Worker  |
   | Node    | | Node    | | Node    |
   +---------+ +---------+ +---------+
```

### Key Roles

* Driver:

  * Controls execution
  * Sends tasks
* Workers:

  * Execute computations

---

## 2.4 Compute Types

| Type        | Usage                 |
| ----------- | --------------------- |
| All-purpose | Development           |
| Job cluster | Scheduled jobs        |
| Serverless  | Fully managed compute |

---

## 2.5 End-to-End Data Flow

```
  Ingestion → Processing → Storage → Analytics

  Files/API/Streams
          |
          v
   +-------------+
   |   Ingest    |
   +-------------+
          |
          v
   +-------------+
   |  Transform  |
   |  (Spark)    |
   +-------------+
          |
          v
   +-------------+
   |  Delta Lake |
   +-------------+
          |
          v
   +-------------+
   | BI / ML     |
   +-------------+
```

---

# 3. Databricks Workspace & UI

## 3.1 Navigation Overview

```
 Sidebar
 --------
 Workspace
 Data
 Compute
 Jobs
 Recents
```

---

## 3.2 Workspace Structure

```
 Workspace
  |
  +-- Users
  |     +-- your_name/
  |
  +-- Shared
  |
  +-- Repos
```

---

## 3.3 Key UI Concepts

### Workspace

* Organizes notebooks and folders

### Compute

* Where clusters are created

### Data Explorer

* View tables and schemas

### Jobs

* Schedule workflows

---

## 3.4 What You Will Do

* Create folder `day01-uXX` (use your student ID)
* Create notebook **01-Day1-Foundations-PySpark-SQL-Widgets** (see labs)
* Create cluster `day01-cluster-uXX` (use your student ID)
* Attach cluster
* **Upload Day 1 data** from the repo **`data/flight-data/`** to Databricks File Store (Day 1 uses File Store only; mounting is in Day 2)
* Run first command

Refer to labs for steps.

---

# 4. Databricks Notebooks

## 4.1 Notebook Structure

```
 Notebook
   |
   +-- Cell 1 (Python)
   +-- Cell 2 (SQL)
   +-- Cell 3 (Markdown)
```

---

## 4.2 Cell Types

### Code Cell

* Executes logic

### Markdown Cell

* Documentation and explanation

---

## 4.3 Magic Commands

Switch languages inside notebook.

```
%python → Python
%sql    → SQL
%md     → Markdown
```

---

## 4.4 Execution Model

```
 Notebook Command
        |
        v
  Sent to Cluster
        |
        v
  Spark Execution
        |
        v
  Output Returned
```

---

## 4.5 DataFrame Concept

* Distributed table abstraction

```
 DataFrame
   |
   +-- Partition 1
   +-- Partition 2
   +-- Partition 3
```

---

## 4.6 What You Will Do

* Create SQL notebook
* Run queries
* Create DataFrame
* Apply transformations

Refer to labs.

---

# 5. Notebook Widgets

## 5.1 What are Widgets

* Input parameters for notebooks
* Enable dynamic execution

---

## 5.2 Widget Flow

```
 User Input → Widget → Notebook Logic → Output
```

---

## 5.3 Example Flow

```
 category = "A"

        |
        v

 Filter DataFrame

        |
        v

 Show Filtered Data
```

---

## 5.4 Why Widgets Matter

* Reusable pipelines
* Dynamic filtering
* Used in production jobs

---

## 5.5 What You Will Do

* Create widget
* Read value
* Apply filter
* Use in SQL

Refer to labs.

---

# End of Day 01
