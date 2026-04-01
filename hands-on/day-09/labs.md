# Day 09 — Monitoring, SQL & Platform Integration — Labs

Follows items **23** and **24**; use notebook **03** only if time remains. Each notebook **`01`–`03`** includes a **Student flow** section at the top — follow that order to avoid UI/cluster mix-ups.

**Notebooks:**  
[01-Day9-Monitoring-Automation-System-Tables.ipynb](notebooks/01-Day9-Monitoring-Automation-System-Tables.ipynb),  
[02-Day9-Databricks-SQL-Warehouses-Dashboards.ipynb](notebooks/02-Day9-Databricks-SQL-Warehouses-Dashboards.ipynb),  
[03-Day9-Extras-Course-Review-and-Extensions.ipynb](notebooks/03-Day9-Extras-Course-Review-and-Extensions.ipynb) (supplement; long notebook).

---

## Part A — Monitoring & automation (item 23)

All **concept** and **manual** steps are in notebook **01** (diagrams, checklists, API template text).

### Tasks

1. Run **01** on a cluster top-to-bottom.  
2. Open **Workflows** → pick a **Day 8** job → inspect **Runs** (duration, outcome, logs).  
3. If entitled: confirm **`system.access.audit`** or **`system.information_schema.catalogs`** cells succeed.  
4. Read the **CI/CD** and **Jobs API** markdown (no secrets in repo).  
5. **Optional:** Azure **Diagnostic logs** / **Log Analytics** — follow admin-provided links.

---

## Part B — Databricks SQL (item 24)

Notebook **02** holds **UI instructions**; cluster cells **prototype SQL** to copy into **SQL Editor**.

### Tasks

1. Run **02** cluster cells; copy the **GROUP BY** query into **Databricks SQL**.  
2. Create or start a **SQL warehouse** (**Serverless** or **Pro** per region).  
3. Follow the **12-step dashboard** section in **02**.  
4. Configure **auto-stop** on the warehouse.  
5. **Optional:** create one **alert** on a saved query.

---

## Part C — Supplement notebook (03)

Use when Parts A and B are done and time remains.

1. Run **03** from the top or jump to a **Day N** header.  
2. Most sections include a short code cell you can run for a quick check.  
3. Near the end, one cell can write a small Delta marker under `day09-{STUDENT_ID}/extras/` if you choose to run it.

---

## References

- [Databricks Jobs](https://docs.databricks.com/jobs/index.html)  
- [System tables](https://docs.databricks.com/sql/admin/system-tables/index.html)  
- [Databricks SQL](https://docs.databricks.com/sql/index.html)  
- [SQL warehouses](https://docs.databricks.com/sql/admin/sql-endpoints.html)
