# Hands-on labs — Databricks course

Each **day** folder has `README.md` (student theory), `labs.md` (tasks), optional `instructor-README.md`, and `notebooks/`.

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

`02-Mount-Azure-Data-Lake.ipynb` itself is the **configuration** notebook; it does not `%run` anything else.

---

## Maintainer notes

See **`docs/content-validation.md`** for JSON checks and ABFS consistency rules.
