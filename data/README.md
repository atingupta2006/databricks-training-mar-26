# Course data

Use this data for **Day 1–3** hands-on. All days use **Azure Data Lake Gen2** via **ABFS** (`abfss://...`) and **`02-Mount-Azure-Data-Lake`** (OAuth on `spark.conf`) — **not** DBFS mount or File Store for primary lab paths.

## Day 1 — Flight data

- **`flight-data/csv/`** — `2010-summary.csv`, `2015-summary.csv`
- **`flight-data/json/`** — `2015-summary.json`

**How to use:** Upload into your ADLS container so paths match the notebooks, e.g. **`data/2010-summary.csv`** and **`data/json/2015-summary.json`** under the same `data/` prefix as **`base_path`** in **`02-Mount-Azure-Data-Lake`**. See **`hands-on/day-01/labs.md`** and the Day 1 notebook intro.
