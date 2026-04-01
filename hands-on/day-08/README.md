# Day 08 — Workflows & Production Pipelines

## Duration

4 hours (items **21** and **22** in the course root `README.md`).

## Outline

| Item | Subject | Time (guide) | Focus |
|------|---------|--------------|--------|
| 21 | Databricks Workflows | ~2 h | Tasks, runs, compute; create a job |
| 22 | Workflow orchestration | ~2 h | Dependencies, errors, scheduling; Bronze → Silver → Gold |

Do item **21** before item **22** (or skim 21 then build the multi-task job from 22).

## Suggested order (student flow)

1. **`01`** — interactive run top to bottom, then create a **single-task** job on **`01`**.  
2. **`02`** — read prerequisites; follow the numbered **Student flow** table (interactive `03`→`04`→`05`, then job wiring).  
3. **`03`, `04`, `05`** — one notebook per medallion stage; used as **three job tasks** with **Depends on**.  
4. **`06`** — optional validation after a successful job (not added as a fourth task unless the instructor asks).

## Where syllabus items appear

| Outline item | Where it is covered |
|---------------|---------------------|
| **21** Tasks / runs / clusters | Notebook `01` + `labs.md` Part A |
| **21** Hands-on: create job pipeline | `01`: single-task job against smoke Delta write |
| **22** Multi-task jobs, dependencies | `02` (student flow) + `labs.md` Part B: **three tasks**, **three notebooks** (`03`–`05`) |
| **22** Error handling, scheduling | `labs.md` (UI: retries, notifications, schedule/trigger) |
| **22** Hands-on: Bronze → Silver → Gold | `03`–`05`: Delta under `day08-{STUDENT_ID}/medallion/`; `06` optional post-run checks |

## Materials here

- [labs.md](labs.md)
- Notebooks under `hands-on/day-08/notebooks/` (same **`BASE_PATH` / `DAY5` / `P_BASIC` / `STUDENT_ID`** as Days 5–7; writes under **`day08-{STUDENT_ID}/`** only):
  - [01-Day8-Databricks-Workflows-Jobs.ipynb](notebooks/01-Day8-Databricks-Workflows-Jobs.ipynb) — item **21** (student flow, single-task job, smoke Delta + audit)
  - [02-Day8-Medallion-Guide-and-Student-Flow.ipynb](notebooks/02-Day8-Medallion-Guide-and-Student-Flow.ipynb) — item **22** guide (prerequisites, job wiring table, one DAG figure, troubleshooting)
  - [03-Day8-Medallion-Bronze-Task.ipynb](notebooks/03-Day8-Medallion-Bronze-Task.ipynb) — item **22** bronze task (job library 1)
  - [04-Day8-Medallion-Silver-Task.ipynb](notebooks/04-Day8-Medallion-Silver-Task.ipynb) — item **22** silver task (job library 2)
  - [05-Day8-Medallion-Gold-Task.ipynb](notebooks/05-Day8-Medallion-Gold-Task.ipynb) — item **22** gold task + metrics append (job library 3)
  - [06-Day8-Medallion-PostRun-Checks.ipynb](notebooks/06-Day8-Medallion-PostRun-Checks.ipynb) — optional counts / history / compare (not a job task)

**Run `01` top to bottom** on a cluster before attaching it to a job so variables like `JOB_CORRELATION` stay in scope. For item **22**, create **one job** with **three notebook tasks** pointing to **`03`, `04`, `05`** and **Depends on** as in `02`.

## Prerequisites

- Days 1–5 complete enough that **`P_BASIC`** and **`2010-summary.csv`** exist on the training storage account (same `BASE_PATH` pattern as other days).
- Permission to create **Jobs** and attach **compute** in the workspace.

## Outcomes

- Create and run a **single-task** notebook job and read its **run** details.
- Create a **multi-task** job with **linear dependencies** across **three notebook tasks** (`03` → `04` → `05`) for bronze → silver → gold.
- Know where to configure **retries**, **notifications**, and **schedules** in the Jobs UI.

## Extra reference material (local)

Optional deeper labs and CI/CD overview:  
`C:\25-Trainings\2-Confirmed\260317-Vinsys-Databricks\databricks` — e.g. `**/M-5/**/13-Building-n-Managing-Workflows-with-Databricks*`, `**/15-Automating-Jobs-with-CI-CD-Pipelines*`, `aws-databricks-training-main/.../Job_Scheduling_and_Monitoring.md`.
