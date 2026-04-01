# Day 08 — Workflows & Production Pipelines

## Duration

4 hours (items **21** and **22** in the course root `README.md`).

## Outline

| Item | Subject | Time (guide) | Focus |
|------|---------|--------------|--------|
| 21 | Databricks Workflows | ~2 h | Tasks, runs, compute; create a job |
| 22 | Workflow orchestration | ~2 h | Dependencies, errors, scheduling; Bronze → Silver → Gold |

Do item **21** before item **22** (or skim 21 then build the multi-task job from 22).

## Where syllabus items appear

| Outline item | Where it is covered |
|---------------|---------------------|
| **21** Tasks / runs / clusters | Notebook `01` + `labs.md` Part A |
| **21** Hands-on: create job pipeline | `01`: single-task job against smoke Delta write |
| **22** Multi-task jobs, dependencies | `02` + `labs.md` Part B: three tasks, same notebook + widget |
| **22** Error handling, scheduling | `labs.md` (UI: retries, notifications, schedule/trigger) |
| **22** Hands-on: Bronze → Silver → Gold | `02`: Delta paths under `day08-{STUDENT_ID}/medallion/` |

## Materials here

- [labs.md](labs.md)
- Notebooks under `hands-on/day-08/notebooks/` (multi-cell lessons, same **`BASE_PATH` / `DAY5` / `P_BASIC` / `STUDENT_ID`** pattern as Days 5–7; outputs under **`day08-{STUDENT_ID}/`** only):
  - [01-Day8-Databricks-Workflows-Jobs.ipynb](notebooks/01-Day8-Databricks-Workflows-Jobs.ipynb) — item **21** (jobs vs interactive runs, task/run model, Mermaid and ASCII figures, short exercises near the smoke write and run history)
  - [02-Day8-Medallion-MultiTask-Workflow.ipynb](notebooks/02-Day8-Medallion-MultiTask-Workflow.ipynb) — item **22** (multi-task job and medallion flow diagrams; cells for schema preview, stage plan, post-run samples)

**Run jobs on the full notebook** (top to bottom) so variables like `JOB_CORRELATION` stay in scope for later cells in `01`. **Mermaid** diagrams render in Databricks notebook markdown when Mermaid is enabled in the workspace; if not, the **ASCII** blocks still carry the same ideas.

## Prerequisites

- Days 1–5 complete enough that **`P_BASIC`** and **`2010-summary.csv`** exist on the training storage account (same `BASE_PATH` pattern as other days).
- Permission to create **Jobs** and attach **compute** in the workspace.

## Outcomes

- Create and run a **single-task** notebook job and read its **run** details.
- Create a **multi-task** job with **linear dependencies** driving a **medallion** flow (bronze → silver → gold).
- Know where to configure **retries**, **notifications**, and **schedules** in the Jobs UI.

## Extra reference material (local)

Optional deeper labs and CI/CD overview:  
`C:\25-Trainings\2-Confirmed\260317-Vinsys-Databricks\databricks` — e.g. `**/M-5/**/13-Building-n-Managing-Workflows-with-Databricks*`, `**/15-Automating-Jobs-with-CI-CD-Pipelines*`, `aws-databricks-training-main/.../Job_Scheduling_and_Monitoring.md`.
