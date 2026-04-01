# Day 08 — Workflows & Production Pipelines — Labs

Follows items **21** and **22** in the course outline.

**Notebooks:** [01-Day8-Databricks-Workflows-Jobs.ipynb](notebooks/01-Day8-Databricks-Workflows-Jobs.ipynb); item 22: [02-Day8-Medallion-Guide-and-Student-Flow.ipynb](notebooks/02-Day8-Medallion-Guide-and-Student-Flow.ipynb), [03-Day8-Medallion-Bronze-Task.ipynb](notebooks/03-Day8-Medallion-Bronze-Task.ipynb), [04-Day8-Medallion-Silver-Task.ipynb](notebooks/04-Day8-Medallion-Silver-Task.ipynb), [05-Day8-Medallion-Gold-Task.ipynb](notebooks/05-Day8-Medallion-Gold-Task.ipynb), optional [06-Day8-Medallion-PostRun-Checks.ipynb](notebooks/06-Day8-Medallion-PostRun-Checks.ipynb). Each notebook’s **Student flow** section states the order to follow.

---

## Part A — Databricks Workflows (item 21)

### Objective

Understand **tasks**, **runs**, and **compute**; create a **job** that runs notebook `01`.

### Tasks

1. Open `01-Day8-Databricks-Workflows-Jobs.ipynb` on a cluster and run it **from the top** (many cells: smoke write, history, audit log, checklists). Confirm `workflow_smoke/run_proof` and append rows under `workflow_smoke/job_audit_runs`.
2. **Workflows** → **Jobs** → **Create job** → add **one** notebook task pointing at `01`.
3. **Run now**; open the **Run** page and note **duration**, **cluster**, **task result**.
4. (Optional) Add **email on failure** or a second task (e.g. SQL or duplicate notebook) to see the graph.

---

## Part B — Orchestration & medallion job (item 22)

### Objective

**Multi-task** job with **dependencies**, basic **error-handling** options, and **scheduling** awareness; hands-on **Bronze → Silver → Gold**.

### Tasks

1. Open **`02-Day8-Medallion-Guide-and-Student-Flow.ipynb`**; run the prerequisite cell; read the **Student flow** table.
2. On a cluster, run **`03`**, then **`04`**, then **`05`** top to bottom once (sanity check). Confirm Delta paths under `day08-{STUDENT_ID}/medallion/`.
3. Create a **new job** with **three** notebook tasks on **three different** notebooks:
   - Task **`bronze`** → file **`03-Day8-Medallion-Bronze-Task.ipynb`** (no dependency)
   - Task **`silver`** → **`04-Day8-Medallion-Silver-Task.ipynb`** — **Depends on** `bronze`
   - Task **`gold`** → **`05-Day8-Medallion-Gold-Task.ipynb`** — **Depends on** `silver`
4. **Run now**; confirm order in the DAG matches bronze → silver → gold.
5. Optionally run **`06-Day8-Medallion-PostRun-Checks.ipynb`** after a successful job.
6. **Error handling:** in Job settings, set **Max retries** (e.g. 1–2); discuss **timeout** and **notifications**.
7. **Scheduling:** add a **schedule** if the instructor asks — then **pause** it for shared training workspaces.

---

## Optional (extra bundle)

- **CI/CD:** skim `databricks/**/15-Automating-Jobs-with-CI-CD-Pipelines*` — outline only for this course day.
- **JSON job definition:** export job **API JSON** from the UI (or REST) for version control discussion.

---

## References

- [Databricks Jobs](https://docs.databricks.com/jobs/index.html)
- [Create and run Databricks Jobs](https://docs.databricks.com/workflows/jobs/jobs.html)
- [Task parameterization (widgets)](https://docs.databricks.com/notebooks/widgets.html)
