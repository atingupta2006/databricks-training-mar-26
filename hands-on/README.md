# Hands-on labs — Databricks course

Each **day** folder has `README.md`, `labs.md`, and `notebooks/`. Some days also include extra facilitator-only notes in the same folder for people running the class.

---

## Connecting to Azure Data Lake (every day)

All lesson notebooks that read or write **ADLS Gen2** use the **same pattern**:

1. **`%run ./02-Mount-Azure-Data-Lake`** — first code cell (or immediately after intro). This sets **OAuth** on `spark.conf` and defines **`base_path`** (`abfss://.../data`).
2. **Paths cell** — assigns `BASE_PATH = base_path` (and day-specific paths such as `OUTPUT_PATH`, `DAY03_ROOT`, etc.).

**Required file:** `02-Mount-Azure-Data-Lake.ipynb` must live in the **same Databricks folder** as the lesson notebook (e.g. `day01-uXX/` contains both `01-Day1-...` and `02-Mount-...`). If you use a different layout, change the `%run` path, for example:

```python
%run ./notebooks/02-Mount-Azure-Data-Lake
# or a workspace absolute path if your admin standardizes one location
```

**New cluster or cluster restart:** Run **`%run ./02-Mount-Azure-Data-Lake`** again, then the **paths** cell, before any reads from `abfss://`.

**Notebooks that call the mount helper in this repo:**

| Day | Notebook | `%run` |
|-----|----------|--------|
| 1 | `day-01/notebooks/01-Day1-Foundations-PySpark-SQL-Widgets.ipynb` | Yes |
| 2 | `day-02/notebooks/01-Day2-Spark-DataFrames-Transformations.ipynb` | Yes |
| 3 | `day-03/notebooks/01-Day3-Medallion-Bronze-Silver-Gold.ipynb` | Yes |
| 3 | `day-03/notebooks/03-Day3-Delta-Lake-Advanced.ipynb` | Yes |
| 4 | `day-04/notebooks/01-Day4-Unity-Catalog-Fundamentals.ipynb` | Yes |
| 4 | `day-04/notebooks/03-Day4-Unity-Catalog-Security-Lineage.ipynb` | Yes |
| 5 | `day-05/notebooks/01-Day5-Delta-Lake-Architecture-and-Basics.ipynb` | Yes |
| 5 | `day-05/notebooks/03-Day5-Delta-History-Optimize-Advanced.ipynb` | Yes |
| 5 | `day-05/notebooks/04-Day5-Delta-DML-MERGE-SCD.ipynb` | Yes |

`02-Mount-Azure-Data-Lake.ipynb` itself is the **configuration** notebook; it does not `%run` anything else.

**Day 4** hands-on folder: **`hands-on/day-04/`** (Unity Catalog — requires UC-enabled workspace; see **`docs/unity-catalog-enabled-workspace-setup.md`**).

**Day 5** hands-on folder: **`hands-on/day-05/`** (extended Delta Lake on ABFS; regenerate: **`python internal/build_day05_notebooks.py`**).

---

Course maintainers: see **`docs/README.md`** (optional local workflows are not committed; `.local-maintainer/` is gitignored).
