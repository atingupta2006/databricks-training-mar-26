# Day 09 — Monitoring, SQL & Platform Integration

## Duration

4 hours (items **23** and **24** in the course root `README.md`), plus extra time for the supplement notebook if the class schedule allows.

## Outline

| Item | Subject | Time (guide) | Focus |
|------|---------|--------------|--------|
| 23 | Monitoring & Automation | ~1.5 h | Job monitoring, system tables, alerts, Jobs API, CI/CD overview |
| 24 | Databricks SQL | ~1.5 h | SQL warehouses (Serverless / Pro), auto-stop, dashboards & alerts |
| — | Supplement | as time allows | **`03-*-Extras-*`**: full-course recap (many cells) |

## Suggested order (student flow)

1. **`01`** on a cluster (item 23) — run top to bottom; use the **Workflows** UI when markdown directs you there.  
2. **`02`** on a cluster (item 24) — run cluster cells, then complete **SQL** / **warehouse** / **dashboard** steps in the browser in the order given in the notebook.  
3. **`03`** only if time remains — read its **Student flow** intro, then run top to bottom or by day section.

## Path convention (same as Days 5–8)

- `BASE_PATH`, `DAY5`, `P_BASIC`, `STUDENT_ID` — identical pattern.  
- **`DAY9_ROOT`** = `abfss://.../data/day09-{STUDENT_ID}` (no trailing slash on root).  
- References **`DAY8_ROOT`** for optional reads of Day 8 **Gold** Delta (if you ran that pipeline).

## Materials here

- [labs.md](labs.md)
- Notebooks under `hands-on/day-09/notebooks/`:
  - [01-Day9-Monitoring-Automation-System-Tables.ipynb](notebooks/01-Day9-Monitoring-Automation-System-Tables.ipynb) — item **23** (figures, sample SQL on the cluster, and UI/API steps in markdown)
  - [02-Day9-Databricks-SQL-Warehouses-Dashboards.ipynb](notebooks/02-Day9-Databricks-SQL-Warehouses-Dashboards.ipynb) — item **24** (warehouses, dashboard steps in the SQL UI, SQL you can run from the cluster editor)
  - [03-Day9-Extras-Course-Review-and-Extensions.ipynb](notebooks/03-Day9-Extras-Course-Review-and-Extensions.ipynb) — supplement only; long recap across the course when time allows

## Prerequisites

- **Day 5** data on ABFS (`P_BASIC`, `2010-summary.csv` as in earlier notebooks).  
- **Day 8** optional: medallion **Gold** path (`day08-.../medallion/gold_by_destination`) after job **`03`–`05`** for cross-reads in **01** and **03**.  
- Entitlements for **`system.*`** queries vary; notebooks use **try/except** like Day 4.

## Outcomes

- Explain what to check on **Job runs** and where **logs** live.  
- Run sample **`system`** / **`information_schema`** SQL when permitted.  
- Describe **Serverless vs Pro** warehouses and **auto-stop**.  
- Follow **in-notebook** steps to build a **SQL dashboard** in the Databricks SQL UI.  
- Use **03** when the schedule allows to **review the full course**.

## Extra reference material (local)

`C:\25-Trainings\2-Confirmed\260317-Vinsys-Databricks\databricks` — e.g. **`Job_Scheduling_and_Monitoring.md`**, **`Monitoring_Optimizing_Pipeline_Performance.md`**, **`06-Spark-SQL.ipynb`**, **`M4-Spark-SQL.ipynb`**.

## Mermaid in markdown

If Mermaid does not render, rely on **ASCII** blocks in the same cells.
