# Day 7 — Structured streaming & Lakeflow ETL

## Duration

Four hours (course outline items **19** and **20**). Complete item **19** before **20**.

## What this day covers

**Item 19 — Streaming on Delta**  
You use a single notebook to practice streaming reads and writes, checkpoints, and change data feed patterns against the shared lab storage layout.

**Item 20 — Lakeflow ETL Pipelines**  
You deploy a small medallion flow (bronze → silver → gold) as Python pipeline libraries. In the workspace you use the **Lakeflow Pipelines Editor** flow (**Add existing assets** to point at the repo files). Tables are published to **Unity Catalog** from the pipeline settings—not by hardcoding catalog or schema names in the files. Step-by-step UI options are in [pipelines/DEPLOY.md](pipelines/DEPLOY.md) (with a screenshot of the **Next step for your pipeline** screen).

## Materials

| Piece | Location |
|-------|-----------|
| Labs checklist | [labs.md](labs.md) |
| Item 19 notebook | [notebooks/01-Day7-Structured-Streaming-Delta.ipynb](notebooks/01-Day7-Structured-Streaming-Delta.ipynb) |
| Item 20 pipeline code | [pipelines/lakeflow_bronze_flights.py](pipelines/lakeflow_bronze_flights.py), [pipelines/lakeflow_silver_flights.py](pipelines/lakeflow_silver_flights.py), [pipelines/lakeflow_gold_flights.py](pipelines/lakeflow_gold_flights.py) |
| Optional file ingest | [pipelines/lakeflow_bronze_cloudfiles_ingestion.py](pipelines/lakeflow_bronze_cloudfiles_ingestion.py) |
| How to create & run the pipeline | [pipelines/DEPLOY.md](pipelines/DEPLOY.md) |

## Prerequisites

- Working Delta data from earlier days (same `BASE_PATH` / Day 5 flight summary path used elsewhere in the course).
- Workspace permission to create an **ETL Pipeline** and write to a UC schema your instructor assigns.

## Outcomes

After this day you should be able to run the streaming lab end-to-end, attach the three default pipeline libraries, set **Triggered** mode and a UC target, and confirm **lineage** and **expectations** for the sample medallion tables.

## Optional local references

Extra notebooks or markdown under a separate `databricks` bundle, if your instructor points you there.

## Related hands-on days

- **Day 8** — Jobs and multi-task workflows.  
- **Day 9** — Monitoring and SQL warehouses.
