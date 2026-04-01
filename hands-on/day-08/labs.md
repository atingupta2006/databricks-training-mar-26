# Day 08 — Workflows & Production Pipelines — Labs

Follows items **21** and **22** in the course outline.

**Notebooks:** [01-Day8-Databricks-Workflows-Jobs.ipynb](notebooks/01-Day8-Databricks-Workflows-Jobs.ipynb), [02-Day8-Medallion-MultiTask-Workflow.ipynb](notebooks/02-Day8-Medallion-MultiTask-Workflow.ipynb). Figures are Mermaid and ASCII; Mermaid needs to be enabled in the workspace to render.

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

1. Run `02` interactively with widget **`pipeline_stage` = `all`**; verify bronze, silver, gold Delta paths under `day08-{STUDENT_ID}/medallion/`.
2. Create a **new job** with **three** notebook tasks on the **same** notebook:
   - `bronze` — parameter `pipeline_stage` = `bronze`
   - `silver` — depends on `bronze` — `pipeline_stage` = `silver`
   - `gold` — depends on `silver` — `pipeline_stage` = `gold`
3. **Run now**; confirm order in the DAG.
4. **Error handling:** in Job settings, set **Max retries** (e.g. 1–2) on a task; discuss **timeout** and **notifications**.
5. **Scheduling:** add a **schedule** (e.g. daily cron) or describe **file arrival** / **trigger** if your workspace exposes it — then **pause** the schedule for the training tenant.

---

## Optional (extra bundle)

- **CI/CD:** skim `databricks/**/15-Automating-Jobs-with-CI-CD-Pipelines*` — outline only for this course day.
- **JSON job definition:** export job **API JSON** from the UI (or REST) for version control discussion.

---

## References

- [Databricks Jobs](https://docs.databricks.com/jobs/index.html)
- [Create and run Databricks Jobs](https://docs.databricks.com/workflows/jobs/jobs.html)
- [Task parameterization (widgets)](https://docs.databricks.com/notebooks/widgets.html)
