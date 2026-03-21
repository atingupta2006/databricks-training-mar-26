# Day 04 — Labs (`labs.md`)

## Theme

**Unity Catalog governance** — personal schema, **views** over shared **Day 3 Delta** paths on **ABFS**, metadata commands, **GRANT** patterns, and **lineage** discovery.

## Duration

**~5 hours** total. Suggested time boxes are indicative; the session may reorder or assign parts as homework.

| Lab | Topic | Suggested time |
|-----|--------|----------------|
| Lab 0 | Setup + mount | 10–15 min |
| Lab 1 | UC schema + views (Notebook 01) | 75–95 min |
| Lab 2 | Metadata + grants (Notebook 03) | 60–80 min |
| Lab 3 | Lineage + audit + challenges | 40–60 min |
| Lab 4 | Cleanup / reflection | 10–15 min |

---

## Shared Databricks Account — Use Your Student ID

This course uses a shared workspace. Each student must set their own suffix to avoid name collisions:

- Workspace folder: `day04-uXX`
- Cluster / warehouse: `day04-cluster-uXX`
- Notebook variable: `STUDENT_ID = "uXX"`

Replace `XX` with assigned ID (u01..u16).

---

## Lab 0 — Setup and mount validation (all users)

### Objective
Confirm `02-Mount-Azure-Data-Lake.ipynb` works and `base_path` is correct.

### Tasks
1. Create `day04-uXX`; attach `day04-cluster-uXX` (UC-compatible).
2. Copy these notebooks to your folder:
   - `02-Mount-Azure-Data-Lake.ipynb`
   - `01-Day4-Unity-Catalog-Fundamentals.ipynb`
   - `03-Day4-Unity-Catalog-Security-Lineage.ipynb`
3. In `01-Day4`, run `%run ./02-Mount-Azure-Data-Lake`.
4. Verify `base_path` is `abfss://.../data` and Day 3 Delta paths exist:
   - `{base_path}/day03/silver/flights_clean`
   - `{base_path}/day03/gold/flights_by_destination`

### Success criteria
- No auth errors.
- `base_path` resolves and the two Day 3 directories are readable.

---

## Lab 1 — Unity Catalog schema + views (Notebook 01)

### Objective
Build the personal schema and UC views, then use SQL and DataFrame queries to verify.

### Tasks
1. Set `STUDENT_ID = "uXX"` in `01-Day4`.
2. Run schema creation:
   - `CREATE SCHEMA IF NOT EXISTS main.day04_uXX_lab`.
3. Create the views:
   - `flights_silver_v` (Silver Delta path)
   - `flights_gold_v` (Gold Delta path)
   - `flights_silver_dest_only_v` (projection; low-sensitivity example)
   - `flights_silver_tagged_v` (enrichment example)
4. Validate data:
   - `SELECT COUNT(*)` from each view and direct Delta path parity.
   - Simple analytics: top destinations, aggregates, join Silver+Gold.
5. Explore metadata:
   - `SHOW TABLES IN main.day04_uXX_lab`
   - `DESCRIBE EXTENDED` view/table
   - `SHOW CREATE VIEW` (when supported)

### Success criteria
- All views exist and return rows.
- Schema/query outputs match Day 3 source row counts.
- Metadata commands run cleanly (or produce documented permission fallback).

---

## Lab 2 — Security and grants (Notebook 03)

### Objective
Practice UC RBAC patterns, check grants, inspect `information_schema`, and review catalog lineage/audit.

### Tasks
1. Re-run `02-Mount` in `03-Day4` and set paths:
   - `CATALOG = "main"`, `STUDENT_ID = "uXX"`, `FULL_SCHEMA = main.day04_uXX_lab`.
2. Current identity check:
   - `SELECT current_user(), current_catalog(), current_schema()`.
3. Inspect grants:
   - `SHOW GRANTS ON VIEW` for your views.
   - `SHOW GRANTS ON SCHEMA {FULL_SCHEMA}`.
4. Use `information_schema` queries:
   - `tables`, `columns`, `views`, `schemata`.
5. Optional lineage queries:
   - `system.information_schema.table_lineage`, `column_lineage` with try/except.
6. Masked & projection validation:
   - Compare results from `flights_silver_v` and `flights_silver_masked_v` (if created).

### Success criteria
- Grant checks and info schema queries complete or show safe fallback.
- Security / governance pattern names align with Notebook 01 objects.

---

## Lab 3 — Lineage, audit, and challenge tasks

### Objective
Finalize Day 4 with lineage review, audit concepts, and mini challenge answers.

### Tasks
1. Catalog Explorer lineage tab:
   - `flights_silver_v` and `flights_gold_v` upstream paths.
2. Audit review:
   - `system.access.audit` with try/except.
3. Answer / complete Notebook 01 part L challenges and Notebook 03 security drills.
4. Optional: create an extra view for edge-case security (e.g. US-only or masked row).

### Success criteria
- At least one lineage view is inspected and notes recorded.
- Challenge answers are attempted in notebook cells.

---

## Lab 4 — Cleanup

### Tasks
1. Optionally drop schema if instructed:
   - `spark.sql(f"DROP SCHEMA IF EXISTS {FULL_SCHEMA} CASCADE")`
2. Document issues experienced and any environment limits (e.g. `SHOW GRANTS` not available).

---

## Notes
- If your workspace is not UC-enabled, document it and skip UC-specific commands.
- Keep `staging` and repeatable run practice in the same notebook path for reproducibility.
