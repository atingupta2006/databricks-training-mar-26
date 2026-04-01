# Day 04 — Unity Catalog Governance

## Duration

**5 hours** (lecture + labs). Notebook **01** is the longest; **03** assumes you have completed schema + views in **01**.

---

## Learning outcomes

By the end of Day 4 you should be able to:

- Explain the three-part name `catalog.schema.object` and use Catalog Explorer.
- Create a personal schema such as `main.day04_uXX_lab` using your assigned student ID.
- Create views that read Day 3 Silver and Gold data via `delta.` ABFS paths.
- Use `SHOW`, `DESCRIBE`, and `DESCRIBE EXTENDED` on schemas and views.
- Name common privileges (`USAGE`, `SELECT`, …), interpret `SHOW GRANTS` when visible, and read example `GRANT` / `REVOKE` statements.
- Open the Lineage tab for an object and describe what it shows, including limits you might see.
- Build a projection view (fewer columns) over the same Delta path for stricter consumer access.
- Use `information_schema` views where your permissions allow, in addition to `SHOW TABLES`.

The hands-on notebooks follow the same ideas as standard Databricks governance training (RBAC, lineage, workspace permissions), adapted to this course’s ABFS paths and naming.

---

## Prerequisites

* **Day 3 completed** (or at least Silver + Gold Delta paths exist under your shared **`base_path`**, e.g. `.../data/day03/silver/...`, `.../data/day03/gold/...`).
* **Unity Catalog** enabled on the workspace and your user can **`CREATE SCHEMA`** (or an admin provisions a catalog/schema for the class).
* **Compute:** UC-compatible cluster or SQL warehouse, per your workspace standard.
* **ADLS:** **`%run ./02-Mount-Azure-Data-Lake`** still defines **`base_path`**; Day 4 views **point at** those paths — they do not replace OAuth setup.

---

## Notebooks (`notebooks/`)

Run in this order:

1. `02-Mount-Azure-Data-Lake.ipynb` — OAuth on `spark.conf` and `base_path` (ABFS), same as earlier days.
2. `01-Day4-Unity-Catalog-Fundamentals.ipynb` — UC namespace, personal schema, Silver and Gold views, projection and other view patterns, metadata commands, brief notes on external locations and volumes.
3. `03-Day4-Unity-Catalog-Security-Lineage.ipynb` — RBAC layers, grant chain, `current_user()`, `SHOW GRANTS`, `information_schema`, lineage and audit topics.

Notebook 01 starts with `%run ./02-Mount-Azure-Data-Lake` (you do not have to open 02 separately first). Notebook 03 expects the views from 01 to exist unless you re-run the setup cells.

After a cluster restart, run `%run` again, then your paths and `STUDENT_ID` cell.

ADLS access for the whole course: see `hands-on/README.md`. UC platform setup for admins: `docs/unity-catalog-enabled-workspace-setup.md`.

Step-by-step lab tasks: `labs.md`.

Maintainers rebuilding notebooks from source: `python internal/build_day04_notebooks.py`

---

## Databricks workspace — Student ID

Use a **unique** suffix so schemas and folders do not collide in a shared account:

| Item | Convention | Example |
|------|------------|---------|
| **Workspace folder** | `day04-uXX` | `day04-u07` |
| **Cluster / warehouse** | UC-compatible | `day04-cluster-u07` or class SQL warehouse |
| **Notebook variable** | **`STUDENT_ID = "uXX"`** | **`"u07"`** → schema **`main.day04_u07_lab`** |

Use the student IDs assigned for your class (for example `u01`–`u16`). Do not all use the same ID in a shared workspace or schemas will collide.

---

## Mental model: Day 3 data vs Day 4 governance

```text
ADLS (abfss://.../data/day03/...)
        │
        │  physical Delta files (Bronze / Silver / Gold)
        │
        ▼
   delta.`abfss://.../path`   ◄── SQL / notebooks read this URI
        │
        │  Day 4: CREATE VIEW ... AS SELECT * FROM delta.`...`
        ▼
   main.day04_uXX_lab.flights_silver_v   ◄── governed UC object (GRANT target)
```

* **Day 4 does not copy** Day 3 data. Views are **metadata** in UC that reference the **same** storage path.
* **Why views?** In shared training accounts, many students **cannot** each register a separate **EXTERNAL TABLE** on the **identical** `LOCATION`. **Views** over **`delta.\`path\``** give each student a **personal** securable object.

---

# 11. Unity Catalog Fundamentals

## 11.1 What is Unity Catalog?

**Unity Catalog (UC)** is Databricks’ unified **governance layer** for data and AI assets across workspaces (within a metastore region). It provides:

* A single **three-level namespace**: **`catalog.schema.table`** (or view, volume, function, model, etc.).
* **Centralized access control** with **`GRANT`** / **`REVOKE`** on **securable** objects.
* **Auditability** and **lineage** integration with the **Catalog** / **Explorer** UI.
* A path away from ad-hoc **Hive metastore**–only patterns (**`hive_metastore`**) where UC is enabled.

### UC vs legacy Hive metastore (conceptual)

| Aspect | Unity Catalog | Hive metastore (legacy) |
|--------|----------------|---------------------------|
| **Identity & audit** | Stronger integration with account / cloud identity | Often workspace-local |
| **Cross-workspace** | Same metastore can govern multiple workspaces (region) | Typically per-workspace |
| **Securables** | Catalogs, schemas, tables, views, volumes, external locations, … | Tables, mostly |
| **External data** | **External locations** + credentials as first-class objects | Mounts / loose paths |

Exact behavior depends on your Databricks account and runtime version; follow what is demonstrated in your workspace.

---

## 11.2 Benefits

| Benefit | Meaning |
|---------|---------|
| **Central governance** | One place to reason about who can use which data. |
| **Discovery** | **Catalog Explorer** lists catalogs, schemas, tables, columns. |
| **Lineage** | Upstream/downstream relationships for impact analysis. |
| **Compliance** | Aligns with enterprise identity (e.g. **Entra ID** groups) and policies. |

---

## 11.3 Three-level namespace

```text
catalog_name.schema_name.object_name
```

**Examples**

* `main.day04_u01_lab.flights_silver_v` — personal lab schema + view (this course).
* `finance_prod.reporting.monthly_kpis` — typical prod-style name.

**Meaning**

* **Catalog** — often environment or org boundary (e.g. `main`, `sandbox`, `prod`).
* **Schema** — like a **database**: grouping of tables, views, functions.
* **Object** — table, **view**, volume, etc.

---

## 11.4 Managed vs external vs views (important for this lab)

| Asset type | Storage | Typical in class |
|------------|---------|------------------|
| **Managed table** | Default storage for catalog/schema | Less common in *this* day’s notebook path |
| **External table** | Explicit **`LOCATION`** on cloud storage | Admin setup; **duplicate LOCATION** often blocked for students |
| **View** | No data of its own; saved **query text** | **Primary pattern** — `CREATE VIEW … AS SELECT … FROM delta.\`abfss://...\`` |

**Views** can reference **`delta.\`abfss://container@account.dfs.core.windows.net/data/...\``** directly. That matches how **Days 1–3** already wrote **Delta** to ADLS.

---

# 12. Security & Access Control

## 12.1 Privileges (typical)

You will see names like:

* **`USAGE`** — on **catalog** and **schema**; usually **required before** using objects inside that schema.
* **`SELECT`** — read table or view.
* **`MODIFY`** — change data (tables).
* **`CREATE TABLE`**, **`CREATE VIEW`**, **`CREATE FUNCTION`** — schema-level (often restricted).
* **`READ FILES`** / **`WRITE FILES`** — on **external locations** (ingest/export scenarios).

**Rule of thumb:** If something “should work” but errors with *permission denied*, check **`USAGE`** on the **parent catalog/schema** first, then object-level grants.

---

## 12.2 GRANT / REVOKE

Grant **least privilege** — prefer **groups**, not long lists of users.

```sql
-- Example: grant read on a student's view to an analysts group
GRANT SELECT ON VIEW main.day04_u01_lab.flights_silver_v TO `analysts-group`;

-- Remove access
REVOKE SELECT ON VIEW main.day04_u01_lab.flights_silver_v FROM `analysts-group`;
```

**Notes**

* Principal names (users / groups / SPs) depend on your **identity provider**; backticks often used for special characters.
* **`SHOW GRANTS`** output varies by **DBR** and **your role** — you may see empty or partial results unless you are owner/admin.

---

## 12.3 Roles (conceptual)

| Role | Typical responsibilities |
|------|---------------------------|
| **Metastore / account admin** | Metastore, external locations, storage credentials |
| **Catalog / schema owner** | Create schemas, grant on owned objects |
| **Data engineer** | Pipelines, tables, views |
| **Analyst** | `SELECT` on curated views |

---

# 13. Storage & External Locations

## 13.1 Storage credentials

Link UC to **Azure** (or AWS/GCP) identity that can read/write **ADLS** (or S3/GCS) **without** embedding long-lived secrets in every notebook. Students still use **`02-Mount`** for **Spark** OAuth in compute; **UC** credentials are a **parallel** governance story for **registered** locations.

## 13.2 External locations

Map a **URL prefix** (e.g. `abfss://container@account.dfs.core.windows.net/data/`) to a **storage credential** so governed operations (**`EXTERNAL TABLE`**, **`COPY INTO`**, some volume patterns) are **auditable**.

**This course:** You often **skip** registering your own external location and instead use **views** that reference **`delta.\`abfss://...\``**, as long as **Spark** can reach ADLS via the mount helper.

## 13.3 Volumes

**Volumes** store **non-tabular** files under UC with the same privilege model as tables — useful for ML assets, documents, and unstructured data. Day 4 notebooks introduce them at a **concept** level.

---

# 14. Data Lineage

* **Automatic lineage** for many Databricks operations (jobs, notebooks writing Delta, ETL pipelines).
* **Catalog Explorer** → select an object → **Lineage** tab.
* **Column lineage** — where supported, helps when renaming or dropping columns.

**Set expectations**

* Views over `delta.` paths may show limited lineage until pipelines consistently publish through governed objects; compare what you see in Catalog Explorer with what the training environment supports.

---

# 15. Relation to Days 1–3 (and Day 5)

| Day | Focus |
|-----|--------|
| **1–2** | PySpark / SQL, **`base_path`**, first reads/writes. |
| **3** | **Medallion** Delta under **`.../data/day03/...`**. |
| **4** | **UC** names (**`main.day04_uXX_lab.*`**) and **privileges** over the **same** ADLS data. |
| **5** | Deeper **Delta** mechanics (optional overlap with Day 3 Delta topics — complementary, not a repeat of UC). |

---

## Success criteria (self-check)

* [ ] **`STUDENT_ID`** set correctly; schema **`main.day04_uXX_lab`** exists.
* [ ] At least **two views** (Silver + Gold pattern) run **`SELECT COUNT(*)`** without error.
* [ ] **Catalog Explorer** shows your schema and views.
* [ ] You can explain **one** difference between a **view** and an **external table**.
* [ ] You have opened **Lineage** (or noted why it is empty) for a lab object.

---

## Common pitfalls

| Issue | What to do |
|-------|------------|
| **Day 3 paths missing** | Views return **0 rows** or fail — confirm **`base_path`** and Day 3 notebook outputs on ADLS. |
| **Everyone uses `u01`** | Schema collisions — use **your** assigned ID. |
| **`CREATE SCHEMA` fails** | You may need a different catalog or higher privilege — ask the person running the lab or your workspace admin. |
| **`SHOW GRANTS` empty** | Normal if you are not the object owner; full grant listings often need owner or admin access. |
| **Hive-only workspace** | UC notebooks will not match this lab — confirm metastore assignment (see setup doc). |

---

## Quick reference (SQL snippets)

```sql
-- List schemas you can see
SHOW SCHEMAS IN main;

-- Objects in your lab schema
SHOW TABLES IN main.day04_u01_lab;

-- Replace u01 with your STUDENT_ID
DESCRIBE EXTENDED VIEW main.day04_u01_lab.flights_silver_v;
```

---

# End of Day 04

Next hands-on track: Day 5 — `hands-on/day-05/` (Delta Lake on ABFS).
